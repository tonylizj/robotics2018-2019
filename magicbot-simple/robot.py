#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot

from components.drive import Component1
from components.drive import Drive


class MyRobot(MagicRobot):
    
    #
    # Define components here
    #
    
    component1 = Component1
    drive = Drive
    
    # You can even pass constants to components
    SOME_CONSTANT = 1
    
    def createObjects(self):
        """Initialize all wpilib motors & sensors"""
        
        # TODO: create button example here
        
        #self.component1_motor = wpilib.Talon(1)
        #self.some_motor = wpilib.Talon(2)

<<<<<<< HEAD
        self.lMotor = wpilib.Talon(1)
        self.rMotor = wpilib.Talon(2)
=======
        self.lMotor = wpilib.Talon(2)
        self.rMotor = wpilib.Talon(1)
>>>>>>> feb55d562fb5f40bc5a1277ae515f12b81b52f69
        
        self.joystick = wpilib.Joystick(0)
    
    #
    # No autonomous routine boilerplate required here, anything in the
    # autonomous folder will automatically get added to a list
    #
    
    
    def teleopPeriodic(self):
        """Place code here that does things as a result of operator
           actions"""

        if self.joystick.getTrigger():
            self.drive.start_driving()
    

if __name__ == '__main__':
    wpilib.run(MyRobot)
