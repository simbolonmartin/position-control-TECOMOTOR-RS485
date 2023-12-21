def degree_to_revolution(degree):
    #the angle accuracy will be 1 revolution = 2.25 degree
    #use the absolute positioning, so it will be accurate
    #if using the relative/inceremental positioning, the error will accumulate
    #can be improved by sending the pulse, we have 2500 ppr encoder
    number_of_revolution =  int(4 * degree // 9)
    return number_of_revolution

def revolution_to_byte_command(revolution):
    return int.to_bytes(revolution, 2, 'big', signed=True)

def pulse_to_byte_command(pulse):
    return int.to_bytes(pulse, 4, 'little', signed=True)

def calculate_modbus_crc(data):
    crc = 0xFFFF  # Initial value for Modbus CRC

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001  # Polynomial: 0x8005
            else:
                crc >>= 1

    # Swap bytes to get little-endian result
    crc = ((crc & 0xFF) << 8) | ((crc >> 8) & 0xFF)
    return crc.to_bytes(2, byteorder='big')

def degree_to_pulse(degree: float) -> int:
    """
    This function is used to increase the accuracy of the positioning control.    

    Args:
        degree (float): the angle input

    Returns:
        int: number of pulse
    """
    number_of_pulse = int(4 * degree % 9 / 9 * 2500)
    return number_of_pulse      

def degree_to_hex_with_CRC(degree):
    initial_array = [0x01, 0x06, 0x07, 0x01]
    revolution = degree_to_revolution(degree)
    revolution_byte = list(revolution_to_byte_command(revolution))
    pre_CRC = initial_array + revolution_byte
    CRC_two_bytes = calculate_modbus_crc(pre_CRC)
    final_message = pre_CRC + list(CRC_two_bytes)
    return final_message

def accurate_degree_to_hex_with_CRC(degree: float):
    initial_array = [0x01, 0x10, 0x07, 0x01, 0x00, 0x03]
    revolution = degree_to_revolution(degree)
    revolution_byte = list(revolution_to_byte_command(revolution))
    pulse = degree_to_pulse(degree)
    pulse_byte = list(pulse_to_byte_command(pulse))
    pre_CRC = initial_array + revolution_byte + pulse_byte
    CRC_two_bytes = calculate_modbus_crc(pre_CRC)
    final_message = pre_CRC + list(CRC_two_bytes)
    return final_message

def print_hex_as_list(hex_data):
    print(f"Combined Data (Hex): {', '.join(hex(byte) for byte in hex_data)}")


if __name__ == "__main__":
    #convert degree to hex with revolution only
    # final_message = degree_to_hex_with_CRC(360)
    # print_hex_as_list(final_message)

    # #convert degree to pulse to hex
    # number_of_pulse = degree_to_pulse(1)
    # hex_pulse = pulse_to_byte_command(number_of_pulse)
    # print(f"Combined Data (Hex): {', '.join(hex(byte) for byte in hex_pulse)}")

    #convert degree to hex with revolution and pulse
    final_message = accurate_degree_to_hex_with_CRC(1)
    print_hex_as_list(final_message)
