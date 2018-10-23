from magicbot import AutonomousStateMachine, tunable, timed_state

from components.drive import Drive


class TwoSteps(AutonomousStateMachine):
    MODE_NAME = 'Two Steps'
    DEFAULT = True
    
    drive = Drive
    
    drive_speed = tunable(-1)

    @timed_state(duration=0.5, next_state='turn_left', first=True)
    def drive_forward(self):
        self.drive.start_driving(-1, 0)

    @timed_state(duration=0.5, next_state='turn_right')
    def turn_left(self):
        self.drive.start_driving(-1, 0.3)

    @timed_state(duration=0.5, next_state='drive_forward')
    def turn_right(self):
        self.drive.start_driving(-1, -0.3)
