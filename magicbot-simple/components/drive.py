
import wpilib

from magicbot import will_reset_to


class Drive:

    lMotor = wpilib.Talon
    rMotor = wpilib.Talon
    
    # This is changed to the value in robot.py
    SOME_CONSTANT = int
    
    # This gets reset after each invocation of execute()
    started_driving = will_reset_to(False)
    
    def on_enable(self):
        '''Called when the robot enters teleop or autonomous mode'''
        self.logger.info("Robot is enabled: I have SOME_CONSTANT=%s", self.SOME_CONSTANT)

    def start_driving(self, speed, lTurn):
        self.started_driving = True
        self.driving_speed = speed
        self.turning_speed = lTurn

    def execute(self):
        if self.started_driving:
            self.lMotor.setSpeed(-self.driving_speed + self.turning_speed * 0.2)
            self.rMotor.setSpeed(self.driving_speed + self.turning_speed * 0.2)

        else:
            self.lMotor.setSpeed(0)
            self.rMotor.setSpeed(0)
