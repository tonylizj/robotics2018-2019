from wpilib.command import Command

class FollowJoystick(Command):
    '''
    This command will read the joystick's y axis and use that value to control
    the speed of the SingleMotor subsystem.
    '''

    def __init__(self):
        super().__init__('Follow Joystick')

        self.requires(self.getRobot().rMotor)
        self.requires(self.getRobot().lMotor)


    def execute(self):
        self.getRobot().rMotor.setSpeed(-self.getRobot().joystick.getY()-(0.3*self.getRobot().joystick.getX()))
        self.getRobot().lMotor.setSpeed(self.getRobot().joystick.getY()-(0.3*self.getRobot().joystick.getX()))
