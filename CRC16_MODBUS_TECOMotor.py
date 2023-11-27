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



def change_positioning_mode(positioningMode="absolute") -> None:
    """ This only effective after power restart on the driver.
    """
    initial_array = [0x01, 0x06, 0x03, 0x26]
    if positioningMode == "absolute":
        register_value = [0x00, 0x00]
    elif positioningMode == "relative":
        register_value = [0x00, 0x01]
    else:
        print("Invalid positioning method, see the documentation on page 5-45")
    pre_CRC = initial_array + register_value
    CRC_two_bytes = calculate_modbus_crc(pre_CRC)
    final_message_positioning_mode = pre_CRC + list(CRC_two_bytes)
    print(f"Combined Data (Hex): {', '.join(hex(byte) for byte in final_message_positioning_mode)}")

    # res =  self.ser.write(final_message_positioning_mode)


if __name__ == "__main__":
    # Example usage
    #oriental_motor
    # input_data = [0x01, 0x06, 0x07, 0x04, 0x03, 0xE8]
    # result = calculate_modbus_crc(input_data)
    # send_data = input_data + list(result)
    # print(f"Combined Data (Hex): {', '.join(hex(byte) for byte in send_data)}")

    change_positioning_mode()

