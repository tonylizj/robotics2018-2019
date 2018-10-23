#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot
import physics as physics
from components.drive import Drive


class MyRobot(MagicRobot):
    #
    # Define components here
    #

    drive = Drive
    #engine = physics.PhysicsEngine(physics.PhysicsInterface)
    # You can even pass constants to components
    SOME_CONSTANT = 1

    def createObjects(self):
        """Initialize all wpilib motors & sensors"""

        # TODO: create button example here

        # self.component1_motor = wpilib.Talon(1)
        # self.some_motor = wpilib.Talon(2)

        self.lMotor = wpilib.Talon(1)
        self.rMotor = wpilib.Talon(2)

        self.joystick = wpilib.Joystick(0)

    #
    # No autonomous routine boilerplate required here, anything in the
    # autonomous folder will automatically get added to a list
    #

    def teleopPeriodic(self):
        """Place code here that does things as a result of operator
           actions"""

        self.drive.start_driving(self.joystick.getY(), -self.joystick.getX())
        """""
        if self.engine.physics_controller.get_x(self.engine.physics_controller) <= 0 or \
                self.engine.physics_controller.get_x(self.engine.physics_controller) >= 100 or \
                self.engine.physics_controller.get_y(self.engine.physics_controller) <= 0 or \
                self.engine.physics_controller.get_y(self.engine.physics_controller) >= 100:
            self.drive.started_driving(0, 0)
        """""
        if self.joystick.getTrigger():
            self.drive.start_driving(0, 0)


if __name__ == '__main__':
    wpilib.run(MyRobot)
