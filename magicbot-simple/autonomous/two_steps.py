import wpilib
from magicbot import AutonomousStateMachine, tunable, timed_state
             
from components.DriveTrain import DriveTrain
                    
class TwoSteps(AutonomousStateMachine):

    MODE_NAME = 'Two Steps'
    DEFAULT = True
    
    motor = wpilib.Talon
    
    drive_speed = tunable(-1)

    @timed_state(duration=2, next_state='do_something', first=True)
    def dont_do_something(self):
        '''This happens first'''
        pass

    @timed_state(duration=5)
    def do_something(self):
        '''This happens second'''
        self.drive.do_something()
