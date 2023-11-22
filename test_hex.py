def speed_to_byte_command(speed):
    # print("Current speed : ", str(speed))
    hex_speed = to_hex(speed, 16)
    # print("Hex speed = ", hex_speed)
    value = hex_speed
    return int.to_bytes(speed, 2, 'big', signed=True)

def to_hex(val, nbits):
    if val == 0:
        return 0
    else:
        return hex((val + (1 << nbits)) % (1 << nbits)).lstrip('0x')
    



initial_array = [0x01, 0x06, 0x07, 0x01, 0x00, 0x04, 0x08]
speed = list(speed_to_byte_command(-160))
final_array = initial_array + speed
print(speed)
print(final_array)
print(f"Combined Data (Hex): {', '.join(hex(byte) for byte in speed)}")
