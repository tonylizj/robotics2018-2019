#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot

from components.component1 import Component1
from components.DriveTrain import DriveTrain
from autonomous.two_steps import TwoSteps

class MyRobot(MagicRobot):
    
    #
    # Define components here
    #
    
    component1 = Component1
    l_drive = DriveTrain
    r_drive = DriveTrain
    auto_r_drive = TwoSteps
    auto_l_drive = TwoSteps
    # You can even pass constants to components
    SOME_CONSTANT = 1
    
    def createObjects(self):
        """Initialize all wpilib motors & sensors"""
        
        # TODO: create button example here
        
        self.r_drive_motor = wpilib.Talon(1)
        self.l_drive_motor = wpilib.Talon(2)
        self.auto_r_drive_motor = wpilib.Talon(1)
        self.auto_l_drive_motor = wpilib.Talon(2)
        self.joystick = wpilib.Joystick(0)
    
    #
    # No autonomous routine boilerplate required here, anything in the
    # autonomous folder will automatically get added to a list
    #

    def teleopPeriodic(self):
        """Place code here that does things as a result of operator
           actions"""
        
        try:
            if self.joystick.getY():
                self.drive.execute(self.joystick.getY())
        except:
            self.onException()

    
if __name__ == '__main__':
    wpilib.run(MyRobot)
