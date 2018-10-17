
import wpilib
from .component1 import Component1

from magicbot import will_reset_to

class Drive:
    
    component1 = Component1
    lMotor = wpilib.Talon
    rMotor = wpilib.Talon
    speed = 0
    # This is changed to the value in robot.py
    SOME_CONSTANT = int
    
    # This gets reset after each invocation of execute()
    started_driving = will_reset_to(False)
    
    def on_enable(self):
        '''Called when the robot enters teleop or autonomous mode'''
        self.logger.info("Robot is enabled: I have SOME_CONSTANT=%s", type(self))

    def start_driving(self, speed):
        self.started_driving = True
        self.speed = speed

    def execute(self):
        if self.started_driving:
            self.lMotor.setSpeed(self.speed)
            self.rMotor.setSpeed(-self.speed)
        else:
            self.lMotor.set(0)
            self.rMotor.set(0)
