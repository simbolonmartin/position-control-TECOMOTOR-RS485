import IMU
import Motor

if __name__ == "__main__":
    IMUObject = IMU.IMUCommunication()
    MotorObject = Motor.MotorCommunication()
    MotorObject.check_conn()
    MotorObject.initialize_driver()
    MotorObject.set_speed()
    function_in_IMU = MotorObject.send_message_position
    IMUObject.get_imu(function_in_IMU)