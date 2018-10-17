
import wpilib
from .component1 import Component1

from magicbot import will_reset_to

class Component2:
    
    component1 = Component1
    lMotor = wpilib.Talon
    rMotor = wpilib.Talon
    
    # This is changed to the value in robot.py
    SOME_CONSTANT = int
    
    # This gets reset after each invocation of execute()
    did_something = will_reset_to(False)
    
    def on_enable(self):
        '''Called when the robot enters teleop or autonomous mode'''
        self.logger.info("Robot is enabled: I have SOME_CONSTANT=%s", self.SOME_CONSTANT)

    def do_something(self):
        self.did_something = True

    def execute(self):
        if self.did_something:
            self.lMotor.set(1)
            self.rMotor.set(1)
        else:
            self.lMotor.set(0)
            self.rMotor.set(0)
