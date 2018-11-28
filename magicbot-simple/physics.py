#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#


from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units
import math
import threading
from os.path import exists, join
import logging
import imp

from hal_impl.data import hal_data

logger = logging.getLogger('pyfrc.physics')


class PhysicsInitException(Exception):
    pass


class PhysicsEngine(object):
    '''
        Simulates a motor moving something that strikes two limit switches,
        one on each end of the track. Obviously, this is not particularly
        realistic, but it's good enough to illustrate the point
    '''
    
    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                       to communicate simulation effects to
        '''
        
        self.physics_controller = physics_controller
        self.position = 0
        
        # Change these parameters to fit your robot!
        bumper_width = 3.25*units.inch
        
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,       # motor configuration
            110*units.lbs,                  # robot mass
            10.71,                          # drivetrain gear ratio
            2,                              # motors per side
            22*units.inch,                  # robot wheelbase
            23*units.inch + bumper_width*2, # robot width
            32*units.inch + bumper_width*2, # robot length
            6*units.inch                    # wheel diameter
        )
            
    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''
        
        # Simulate the drivetrain
        l_motor = hal_data['pwm'][1]['value']
        r_motor = hal_data['pwm'][2]['value']
        
        x, y, angle = self.drivetrain.get_distance(l_motor, r_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)
        
        # update position (use tm_diff so the rate is constant)
        self.position += hal_data['pwm'][4]['value'] * tm_diff * 3
        
        # update limit switches based on position
        if self.position <= 0:
            switch1 = True
            switch2 = False
            
        elif self.position > 10:
            switch1 = False
            switch2 = True
            
        else:
            switch1 = False
            switch2 = False
        
        # set values here
        hal_data['dio'][1]['value'] = switch1
        hal_data['dio'][2]['value'] = switch2
        hal_data['analog_in'][2]['voltage'] = self.position


class PhysicsInterface:
    '''
        An instance of this is passed to the constructor of your
        :class:`PhysicsEngine` object. This instance is used to communicate
        information to the simulation, such as moving the robot on the
        field displayed to the user.
    '''

    def __init__(self, robot_path, fake_time, config_obj):
        self.last_tm = None
        self._lock = threading.Lock()

        # These are in units of feet relative to the field
        self.x = config_obj['pyfrc']['robot']['starting_x']
        self.y = config_obj['pyfrc']['robot']['starting_y']
        self.angle = math.radians(config_obj['pyfrc']['robot']['starting_angle'])

        self.robot_w = config_obj['pyfrc']['robot']['w']
        self.robot_l = config_obj['pyfrc']['robot']['l']

        # HACK: Used for drawing
        self.vx = 0
        self.vy = 0

        self.fake_time = fake_time
        self.robot_enabled = False

        self.config_obj = config_obj
        self.engine = None
        self.device_gyro_channels = []

        self.hal_data = hal_data

        physics_module_path = join(robot_path, 'physics.py')
        if exists(physics_module_path):

            # Load the user's physics module if it exists
            try:
                physics_module = imp.load_source('physics', physics_module_path)
            except:
                logger.exception("Error loading user physics module")
                raise PhysicsInitException()

            if not hasattr(physics_module, 'PhysicsEngine'):
                logger.error("User physics module does not have a PhysicsEngine object")
                raise PhysicsInitException()

            # for now, look for a class called PhysicsEngine
            try:
                self.engine = physics_module.PhysicsEngine(self)

                if hasattr(self.engine, 'initialize'):
                    self.engine.initialize(self.hal_data)

            except:
                logger.exception("Error creating user's PhysicsEngine object")
                raise PhysicsInitException()

            logger.info("Physics support successfully enabled")

        else:
            logger.warning("Cannot enable physics support, %s not found", physics_module_path)


    def setup_main_thread(self):
        if self.engine is not None:
            self.fake_time.set_physics_fn(self._on_increment_time)

    def __repr__(self):
        return 'Physics'

    def _on_increment_time(self, now):

        last_tm = self.last_tm

        if last_tm is None:
            self.last_tm = now
        else:

            # When using time, always do it based on a differential! You may
            # not always be called at a constant rate
            tm_diff = now - last_tm

            # Don't run physics calculations more than 100hz
            if tm_diff > 0.010:
                try:
                    self.engine.update_sim(self.hal_data, now, tm_diff)
                except Exception as e:
                    raise Exception("User physics code raised an exception (see above)") from e
                self.last_tm = now

    def _set_robot_enabled(self, enabled):
        self.robot_enabled = enabled

    def _has_engine(self):
        return self.engine is not None

    #######################################################
    #
    # Public API
    #
    #######################################################


def add_analog_gyro_channel(self, ch):
    '''
        This function is no longer needed
    '''


# deprecated alias
add_gyro_channel = add_analog_gyro_channel


def add_device_gyro_channel(self, angle_key):
    '''
        :param angle_key: The name of the angle key in ``hal_data['robot']``
    '''

    # TODO: use hal_data to detect gyros
    hal_data['robot'][angle_key] = 0
    self.device_gyro_channels.append(angle_key)


def drive(self, speed, rotation_speed, tm_diff):
    '''Call this from your :func:`PhysicsEngine.update_sim` function.
       Will update the robot's position on the simulation field.

       You can either calculate the speed & rotation manually, or you
       can use the predefined functions in :mod:`pyfrc.physics.drivetrains`.

       The outputs of the `drivetrains.*` functions should be passed
       to this function.

       .. note:: The simulator currently only allows 2D motion

       :param speed:           Speed of robot in ft/s
       :param rotation_speed:  Clockwise rotational speed in radians/s
       :param tm_diff:         Amount of time speed was traveled (this is the
                               same value that was passed to update_sim)
    '''

    # if the robot is disabled, don't do anything
    if not self.robot_enabled:
        return

    distance = speed * tm_diff
    angle = rotation_speed * tm_diff

    x = distance * math.cos(angle)
    y = distance * math.sin(angle)

    self.distance_drive(x, y, angle)


def vector_drive(self, vx, vy, vw, tm_diff):
    '''Call this from your :func:`PhysicsEngine.update_sim` function.
       Will update the robot's position on the simulation field.

       This moves the robot using a velocity vector relative to the robot
       instead of by speed/rotation speed.

       :param vx: Speed in x direction relative to robot in ft/s
       :param vy: Speed in y direction relative to robot in ft/s
       :param vw: Clockwise rotational speed in rad/s
       :param tm_diff:         Amount of time speed was traveled
    '''

    # if the robot is disabled, don't do anything
    if not self.robot_enabled:
        return

    angle = vw * tm_diff
    vx = (vx * tm_diff)
    vy = (vy * tm_diff)

    x = vx * math.sin(angle) + vy * math.cos(angle)
    y = vx * math.cos(angle) + vy * math.sin(angle)

    self.distance_drive(x, y, angle)


def distance_drive(self, x, y, angle):
    '''Call this from your :func:`PhysicsEngine.update_sim` function.
       Will update the robot's position on the simulation field.

       This moves the robot some relative distance and angle from
       its current position.

       :param x:     Feet to move the robot in the x direction
       :param y:     Feet to move the robot in the y direction
       :param angle: Radians to turn the robot
    '''
    with self._lock:
        self.vx += x
        self.vy += y
        self.angle += angle

        c = math.cos(self.angle)
        s = math.sin(self.angle)

        self.x += (x * c - y * s)
        self.y += (x * s + y * c)

        self._update_gyros(angle)


def _update_gyros(self, angle):
    angle = math.degrees(angle)

    for k in self.device_gyro_channels:
        self.hal_data['robot'][k] += angle

    for gyro in self.hal_data['analog_gyro']:
        gyro['angle'] += angle


def get_position(self):
    '''
        :returns: Robot's current position on the field as `(x,y,angle)`.
                  `x` and `y` are specified in feet, `angle` is in radians
    '''
    with self._lock:
        return self.x, self.y, self.angle


def get_offset(self, x, y):
    '''
        Computes how far away and at what angle a coordinate is
        located.

        Distance is returned in feet, angle is returned in degrees

        :returns: distance,angle offset of the given x,y coordinate

        .. versionadded:: 2018.1.7
    '''
    with self._lock:
        dx = self.x - x
        dy = self.y - y

    distance = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    return distance, math.degrees(angle)


def _get_vector(self):
    '''
        :returns: The sum of all movement vectors, not very useful
                  except for getting the difference of them
    '''
    return self.vx, self.vy, self.angle
