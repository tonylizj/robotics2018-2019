from wpilib.command import TimedCommand

class SetSpeed(TimedCommand):
    '''
    Spins the motor at the given power for a given number of seconds, then
    stops.
    '''

    def __init__(self, power, timeoutInSeconds):
        super().__init__('Set Speed %d' % power, timeoutInSeconds)

        self.power = power
        self.requires(self.getRobot().rMotor)
        self.requires(self.getRobot().lMotor)

    def initialize(self):
        self.getRobot().rMotor.setSpeed(-self.power)
        self.getRobot().lMotor.setSpeed(self.power)

    def end(self):
        self.getRobot().rMotor.setSpeed(0)
        self.getRobot().lMotor.setSpeed(0)
