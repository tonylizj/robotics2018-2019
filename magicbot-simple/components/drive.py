
import wpilib
from .component1 import Component1

from magicbot import will_reset_to

class Drive:
    
    component1 = Component1
    lMotor = wpilib.Talon
    rMotor = wpilib.Talon
    
    # This is changed to the value in robot.py
    SOME_CONSTANT = int
    
    # This gets reset after each invocation of execute()
    started_driving = will_reset_to(False)
    
    def on_enable(self):
        '''Called when the robot enters teleop or autonomous mode'''
        self.logger.info("Robot is enabled: I have SOME_CONSTANT=%s", self.SOME_CONSTANT)

    def start_driving(self):
        self.started_driving = True

    def execute(self):
<<<<<<< HEAD:magicbot-simple/components/drive.py
        if self.started_driving:
            self.lMotor.set(-1)
            self.rMotor.set(1)
=======
        if self.did_something:
            self.lMotor.set(1)
            self.rMotor.set(-1)
>>>>>>> feb55d562fb5f40bc5a1277ae515f12b81b52f69:magicbot-simple/components/component2.py
        else:
            self.lMotor.set(0)
            self.rMotor.set(0)
