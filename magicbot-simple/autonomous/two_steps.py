
from magicbot import AutonomousStateMachine, tunable, timed_state
             
from components.drive import Drive


class TwoSteps(AutonomousStateMachine):

    MODE_NAME = 'Two Steps'
    DEFAULT = True
    
    drive = Drive
    
    drive_speed = tunable(-1)

    @timed_state(duration=2, next_state='start_driving', first=True)
    def dont_do_something(self):
        '''This happens first'''
        pass

    @timed_state(duration=5)
    def do_something(self):
        '''This happens second'''
        self.drive.start_driving()

