import serial
import struct
import time
import sys

from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


class MotorCommunication():
    def __init__(self) -> None:
        self.modem_device = "/dev/motor_wrist"
        self.baud_rate = 9600
        self.timex = 3
        self.ser = None

    def check_conn(self):
        try:
            self.ser = serial.Serial(self.modem_device, self.baud_rate, timeout=self.timex)
            
            print("Serial details params: ", self.ser)
        except:
            print("Could not connect to usb port")
    
    def initialize_driver(self):
        intialize_servo_ON = [0x01, 0x06, 0x05, 0x12, 0x00, 0x01, 0xE8, 0xC3]
        try:
            res = self.ser.write(intialize_servo_ON)
            print("Initialization complete")
            # print(res)
            response = self.ser.read(10)
            response = response.hex(":")
            # # result = hex(int.from_bytes(res, byteorder='big'))
            print(response)
            print()
        except:
            print("Initialization failed")
            print()
        time.sleep(3)

    def s16(self, value):
        return -(value & 0x8000) | (value & 0x7fff)

    def send_message_position(self, degree):
        if degree < -20:
            print(f"Minimum limit approached: {degree} is less than -20 degree")
        elif degree > 12:
            print(f"Maximum limit approached: {degree} is greater than 12 degree")
        else:
            degree = -degree
        internalJog         = [0x01, 0x06, 0x05, 0x12, 0x00, 0x21, 0xE9, 0x1B]
        setControlSpeed     = [0x01, 0x06, 0x02, 0x01, 0x00, 0XC8, 0xD8, 0x24] #200rpm
        setControlSpeed_500 = [0x01, 0x06, 0x02, 0x01, 0x01, 0XF4, 0xD9, 0xA5] #500rpm
        stopInternalJog     = [0x01, 0x06, 0x05, 0x12, 0x00, 0x01, 0xE8, 0xC3]
        controlHomingStart  = [0x01, 0x06, 0x05, 0x12, 0x02, 0x01, 0xE9, 0xA3]
        monitorHoming       = [0x01, 0x03, 0x06, 0x1E, 0x00, 0x01, 0xE4, 0x84]
        closeHoming         = [0x01, 0x06, 0x05, 0x12, 0x00, 0x01, 0xE8, 0xC3]
        triggerMovement     = [0x01, 0x06, 0x05, 0x12, 0x00, 0x81, 0xE9, 0x63]
        stop_movement       = [0x01, 0x06, 0x05, 0x12, 0x00, 0x01, 0xE8, 0xC3] #must complete the trigger movement first
        #move with target position = 0 rev and 1000 pulse 
        # setPosition         = [0x01, 0x10, 0x07, 0x01, 0x00, 0x04, 0x08, 0x00, 0x00, 0x03, 0xE8, 0x00, 0x00, 0x00, 0x0A, 0xA0, 0xDD]
        # define positive = CW
        # effective after restart
        # setDirectionCW = [0x01, 0x06, 0x03, 0x14, 0x00, 0x00, 0xC9, 0x8A]
        
        # define positive = CCW
        # effective after restart
        # setDirectionCCW = [0x01, 0x06, 0x03, 0x14, 0x00, 0x01, 0x08, 0x4A]
  
        # print("internalJog")
        # res = self.ser.write(internalJog)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(10)

        # print("setControlSpeed")
        # res = self.ser.write(setControlSpeed_500)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(10)

        # print("stopInternalJog")
        # res = self.ser.write(stopInternalJog)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(3)

        # print("controlHomingStart")
        # res = self.ser.write(controlHomingStart)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(10)

        # print("monitorHoming")
        # res = self.ser.write(monitorHoming)
        # self.read_response(7)
        # self.read_current_alarm()
        # time.sleep(1)
    
        # print("closeHoming")
        # res = self.ser.write(closeHoming)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(1)

        # print("setDirectionCW")
        # res = self.ser.write(setDirectionCW)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(0.1)

        # print("setDirectionCCW")
        # res = self.ser.write(setDirectionCCW)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(0.1)

        # print(f"Set Position to {degree} degree.")
        message = self.degree_to_hex_with_CRC(degree)
        res = self.ser.write(message)
        self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(0.1)

        # print("triggerMovement")
        res = self.ser.write(triggerMovement)
        self.read_response(8)
        self.read_current_alarm()
        # time.sleep(0.5)

        # print("stop_movement")
        res = self.ser.write(stop_movement)
        self.read_response(8)
        # time.sleep()
        # self.read_current_alarm()


    def set_speed(self):
        #current speed is 1000 rpm without gear reduction
        setSpeed = [0x01, 0x06, 0x07, 0x04, 0x03, 0xE8, 0xC9, 0xC1]
        print("Set speed")
        res = self.ser.write(setSpeed)
        self.read_response(8)
        self.read_current_alarm()
        time.sleep(0.1)
        
    def test_send_speed(self):
        speed200rpm = [0x01, 0x06, 0x02, 0x01, 0x00, 0xC8, 0xD8, 0x24]
        speed0rpm = [0x01, 0x06, 0x02, 0x01, 0x00, 0x00, 0xD9, 0xB2]
        print("TEST SEND SPEED")
        print("speed200rpm")
        res = self.ser.write(speed200rpm)
        self.read_response(8)
        self.read_current_alarm()
        print("speed0rpm")
        res = self.ser.write(speed0rpm)
        self.read_response(8)
        self.read_current_alarm()

    def read_current_alarm(self):
        readCurrentAlarm    = [0x01, 0x03, 0x06, 0x3F, 0x00, 0x01, 0xB4, 0x8E]
        print("readCurrentAlarm")
        res = self.ser.write(readCurrentAlarm)
        self.read_response(7)
        print("")
        time.sleep(1)

    def read_response(self, numberOfBit=8):
        response = self.ser.read(numberOfBit)
        # # result = hex(int.from_bytes(res, byteorder='big'))
        response = response.hex(":")
        print(response)
        time.sleep(0.1)

    def degree_to_revolution(self, degree):
        #the angle accuracy will be 1 revolution = 2.25 degree
        #use the absolute positioning, so it will be accurate
        #if using the relative/inceremental positioning, the error will accumulate
        #can be improved by sending the pulse, we have 2500 ppr encoder
        number_of_revolution =  int(4 * degree // 9)
        return number_of_revolution

    def change_positioning_mode(self, positioningMode="absolute") -> None:
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
        CRC_two_bytes = self.calculate_modbus_crc(pre_CRC)
        final_message_positioning_mode = pre_CRC + list(CRC_two_bytes)
        res =  self.ser.write(final_message_positioning_mode)
        self.read_response(8)
        print(f"Change the positioning mode to {positioningMode}.")

    def revolution_to_byte_command(self, revolution):
        return int.to_bytes(revolution, 2, 'big', signed=True)

    def calculate_modbus_crc(self, data):
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

    def degree_to_hex_with_CRC(self, degree):
        initial_array = [0x01, 0x06, 0x07, 0x01]
        revolution = self.degree_to_revolution(degree)
        revolution_byte = list(self.revolution_to_byte_command(revolution))
        pre_CRC = initial_array + revolution_byte
        CRC_two_bytes = self.calculate_modbus_crc(pre_CRC)
        final_message = pre_CRC + list(CRC_two_bytes)
        return final_message

if __name__ == "__main__":
    handle = MotorCommunication()
    handle.check_conn()
    handle.initialize_driver()
    handle.set_speed()
    handle.send_message_position(0)
    time.sleep(3)
    # handle.send_message_position(5)
    # time.sleep(3)
    # handle.send_message_position(10)
    # time.sleep(3)
    # handle.send_message_position(0)
    # time.sleep(3)
    # handle.send_message_position(0)



    print("Finished")