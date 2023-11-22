import serial
import struct
import time
import sys

from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


class MotorCommunication():
    modem_device = "/dev/motor_wrist"
    baud_rate = 9600
    timex = 3
    ser = None

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
        except:
            print("Initialization failed")
        time.sleep(3)

    def s16(self, value):
        return -(value & 0x8000) | (value & 0x7fff)

    def test_send_message_position(self):
        internalJog         = [0x01, 0x06, 0x05, 0x12, 0x00, 0x21, 0xE9, 0x1B]
        setControlSpeed     = [0x01, 0x06, 0x02, 0x01, 0x00, 0XC8, 0xD8, 0x24] #200rpm
        setControlSpeed_500 = [0x01, 0x06, 0x02, 0x01, 0x01, 0XF4, 0xD9, 0xA5] #200rpm

        stopInternalJog     = [0x01, 0x06, 0x05, 0x12, 0x00, 0x01, 0xE8, 0xC3]
        controlHomingStart  = [0x01, 0x06, 0x05, 0x12, 0x02, 0x01, 0xE9, 0xA3]
        monitorHoming       = [0x01, 0x03, 0x06, 0x1E, 0x00, 0x01, 0xE4, 0x84]
        closeHoming         = [0x01, 0x06, 0x05, 0x12, 0x00, 0x01, 0xE8, 0xC3]

        #move with target position = 0 rev and 1000 pulse 
        setPosition         = [0x01, 0x10, 0x07, 0x01, 0x00, 0x04, 0x08, 0x00, 0x00, 0x03, 0xE8, 0x00, 0x00, 0x00, 0x0A, 0xA0, 0xDD] 
        #move with target position = 1 rev and 1000 pulse
        setPosition2        = [0x01, 0x10, 0x07, 0x01, 0x00, 0x04, 0x08, 0x00, 0x01, 0x03, 0xE8, 0x00, 0x00, 0x00, 0x64, 0x54, 0xD5]
        #move with target position = 160 rev and 0 pulse with speed 100 rpm
        setPosition3        = [0x01, 0x10, 0x07, 0x01, 0x00, 0x04, 0x08, 0x00, 0xA0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0xE1, 0x1F]

        #move with target position = 160 rev and 0 pulse with speed 1000 rpm
        setPosition3_1000rpm       = [0x01, 0x10, 0x07, 0x01, 0x00, 0x04, 0x08, 0x00, 0xA0, 0x00, 0x00, 0x00, 0x00, 0x03, 0xE8, 0xE0, 0x4A]
        
        #move with target position = -160 rev and 0 pulse with speed 1000 rpm
        setPosition4_1000rpm       = [0x01, 0x10, 0x07, 0x01, 0x00, 0x04, 0x08, 0xFF, 0x60, 0x00, 0x00, 0x00, 0x00, 0x03, 0xE8, 0x6F, 0x42]
        
        #move with target position = -1000 rev and 0 pulse with speed 1000 rpm
        setPosition5_1000rpm       = [0x01, 0x10, 0x07, 0x01, 0x00, 0x04, 0x08, 0xFC, 0x18, 0x00, 0x00, 0x00, 0x00, 0x03, 0xE8, 0xD7, 0x50]
        
        #make +90, -90, 0
        setPosition_360Degree         = [0x01, 0x06, 0x07, 0x01, 0x00, 0xA0, 0xD9, 0x06]

        #define positive = CW
        # effective after restart
        setDirectionCW = [0x01, 0x06, 0x03, 0x14, 0x00, 0x00, 0xC9, 0x8A]
        
        #define positive = CCW
        # effective after restart
        setDirectionCCW = [0x01, 0x06, 0x03, 0x14, 0x00, 0x01, 0x08, 0x4A]
        
        triggerMovement     = [0x01, 0x06, 0x05, 0x12, 0x00, 0x81, 0xE9, 0x63]
        stop_movement       = [0x01, 0x06, 0x05, 0x12, 0x00, 0x01, 0xE8, 0xC3] #must complete the trigger movement first
 
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

        # print("setPosition")
        # res = self.ser.write(setPosition)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(0.1)

        # print("triggerMovement")
        # res = self.ser.write(triggerMovement)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(5)

        # print("stop_movement")
        # res = self.ser.write(stop_movement)
        # self.read_response(8)
        # time.sleep(2)
        # self.read_current_alarm()

        # print("setPosition2")
        # res = self.ser.write(setPosition2)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(0.1)

        # print("triggerMovement")
        # res = self.ser.write(triggerMovement)
        # self.read_response(8)
        # self.read_current_alarm()
        # time.sleep(3)

        # print("stop_movement")
        # res = self.ser.write(stop_movement)
        # self.read_response(8)
        # time.sleep(2)
        # self.read_current_alarm()

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

        print("setPosition_360Degree")
        res = self.ser.write(setPosition_360Degree)

        self.read_response(8)
        self.read_current_alarm()
        time.sleep(0.1)

        print("triggerMovement")
        res = self.ser.write(triggerMovement)
        self.read_response(8)
        self.read_current_alarm()
        time.sleep(13)

        print("stop_movement")
        res = self.ser.write(stop_movement)
        self.read_response(8)
        time.sleep(2)
        self.read_current_alarm()
        
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
        initial_array = [0x01, 0x07, 0x01]
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
    handle.test_send_message_position()
    print("Finished")