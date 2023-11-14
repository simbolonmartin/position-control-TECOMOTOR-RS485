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


if __name__ == "__main__":
    # Example usage
    input_data = [0x01, 0x10, 0x07, 0x01, 0x00, 0x04, 0x08, 0x00, 0x00, 0x03, 0xE8, 0x00, 0x00, 0x00, 0x0A]
    
    result = calculate_modbus_crc(input_data)
    send_data = input_data + list(result)
    print(f"Combined Data (Hex): {', '.join(hex(byte) for byte in send_data)}")
