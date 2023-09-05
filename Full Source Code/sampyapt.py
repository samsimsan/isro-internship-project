# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 09:29:13 2021

@author: Library04
"""

# -*- coding: utf-8 -*-
"""
APT Motor Controller for Thorlabs
Adopted from
https://github.com/HaeffnerLab/Haeffner-Lab-LabRAD-Tools/blob/master/cdllservers/APTMotor/APTMotorServer.py
With thanks to SeanTanner@ThorLabs for providing APT.dll and APT.lib


V1.1
20141125 V1.0    First working version
20141201 V1.0a   Use short notation for moving (movRelative -> mRel)
20150417 V1.1    Implementation of simple QT GUI

Michael Leung
mcleung@stanford.edu
"""

from ctypes import c_long, c_buffer, c_float, windll, pointer
import _APTAPI
import _error_codes

import ctypes
import ctypes.util
import os
print (os.getcwd())
from core import *
# ########################################################################
# import _APTAPI
# import _error_codes

# import ctypes
# import ctypes.util
# import os
# import sys

# # constants
# # Home direction
# HOME_FWD = 1
# """Home in the forward direction"""
# HOME_REV = 2
# """Home in the reverse direction"""

# # Home limit switch
# HOMELIMSW_FWD = 4
# """Use forward limit switch for home datum"""
# HOMELIMSW_REV = 1
# """Use reverse limit switch for home datum"""

# # Stage units
# STAGE_UNITS_MM = 1
# """Stage units in mm"""
# STAGE_UNITS_DEG = 2
# """Stage units in degrees"""

# # Hardware limit switch settings
# HWLIMSWITCH_IGNORE = 1
# """Ignore limit switch (e.g. for stages with only one or no limit
#    switches)."""
# HWLIMSWITCH_MAKES = 2
# """Limit switch is activated when electrical continuity is detected."""
# HWLIMSWITCH_BREAKS = 3
# """Limit switch is activated when electrical continuity is broken."""
# HWLIMSWITCH_MAKES_HOMEONLY = 4
# """As per HWLIMSWITCH_MAKES except switch is ignored other than when homing
#    (e.g. to support rotation stages)."""
# HWLIMSWITCH_BREAKS_HOMEONLY = 5
# """As per HWLIMSWITCH_BREAKS except switch is ignored other than when homing
#    (e.g. to support rotation stages)."""

# # Move direction (used with move_velocity)
# MOVE_FWD = 1
# """Move forward."""
# MOVE_REV = 2
# """Move reverse."""

# # Profile mode settings : set(get)_dc_profile_mode_params
# DC_PROFILEMODE_TRAPEZOIDAL = 0
# """Trapezoidal profile mode"""
# DC_PROFILEMODE_SCURVE = 2
# """s-curve profile mode"""

# # Joystick direction sense settings - set(get)_dc_joystick_params
# DC_JS_DIRSENSE_POS = 1
# """positive dc joystick direction sense"""
# DC_JS_DIRSENSE_NEG = 2
# """negative dc joystick direction sense"""

# def _get_error_text(error_code):
#     """
#     Returns an error text for the specified error code.

#     Returns
#     -------
#     out : str
#         error message
#     """
#     if (error_code == 0):
#         return "Command successful."
#     else:
#         try:
#             return _error_codes.error_message[error_code]
#         except:
#             return "Invalid error code."


# def list_available_devices():
#     """
#     Lists all devices connected to the computer.

#     Returns
#     -------
#     out : list
#         list of available devices. Each device is described by a tuple
#         (hardware type, serial number)
#     """
#     # we have to check for all possible hardware types.
#     # Unfortunately I couldn't find a list of all existing hardware types,
#     # the list in the C header file is incomplete. Therefore we just check
#     # the first 100 type values
#     devices = []
#     count = ctypes.c_long()
#     for hwtype in range(100):
#         if (_lib.GetNumHWUnitsEx(hwtype, ctypes.byref(count)) == 0):
#             # found an existing hardware type
#             if (count.value > 0):
#                 # devices are available!!
#                 # get their serial number
#                 serial_number = ctypes.c_long()
#                 for ii in range(count.value):
#                     if (_lib.GetHWSerialNumEx(hwtype, ii,
#                         ctypes.byref(serial_number)) == 0):
#                         devices.append((hwtype, serial_number.value))
#     return devices

# def hardware_info(serial_number):
#     """
#     Retrieves hardware information about the devices identified by its
#     serial number.

#     Parameters
#     ----------
#     serial_number : int
#         Serial number identifying the device

#     Returns
#     -------
#     out : tuple
#         hardware information: (model, software version, hardware notes)
#     """
#     model = ctypes.c_buffer(255)
#     swver = ctypes.c_buffer(255)
#     hwnotes = ctypes.c_buffer(255)
#     err_code = _lib.GetHWInfo(serial_number, model, len(model),
#         swver, len(swver), hwnotes, len(hwnotes))
#     if (err_code != 0):
#         raise Exception("Getting hardware info failed: %s" %
#                 _get_error_text(err_code))
#     return (model.value, swver.value, hwnotes.value)



# class Motor(object):
#     """
#     Object used to control a Thorlabs motor.

#     Parameters
#     ----------
#     serial_number : int
#         Serial number identifying device
#     """
#     def __init__(self, serial_number):
#         self._serial_number = serial_number
#         self._active_channel = 0
#         # initialize device
#         err_code = _lib.InitHWDevice(serial_number)
#         if (err_code != 0):
#             raise Exception("Could not initialize device: %s" %
#                     _get_error_text(err_code))

#     def __property_from_index(index, get_func, set_func):
#         def setter(self, value):
#             params = list(get_func(self))
#             params[index] = value
#             set_func(self, *params)

#         def getter(self):
#             return get_func(self)[index]

#         setter.get_func = get_func
#         setter.index = index
#         getter.index = index

#         return property(getter, setter)

#     @property
#     def serial_number(self):
#         """
#         Returns the serial number of the motor.

#         Returns
#         -------
#         out : int
#             serial number
#         """
#         return self._serial_number

#     @property
#     def hardware_info(self):
#         """
#         Returns hardware information about the motor.

#         Returns
#         -------
#         out : tuple
#             (model, software version, hardware notes)

#         See also
#         --------
#         hardware_info
#         """
#         return hardware_info(self._serial_number)

#     @property
#     def _status_bits(self):
#         """
#         Returns status bits of motor

#         Returns
#         -------
#         out : int
#             status bits
#         """
#         status_bits = ctypes.c_long()
#         err_code = _lib.MOT_GetStatusBits(self._serial_number,
#                 ctypes.byref(status_bits))
#         if (err_code != 0):
#             raise Exception("Getting status failed: %s" %
#                     _get_error_text(err_code))
#         return status_bits.value

#     @property
#     def is_forward_hardware_limit_switch_active(self):
#         """
#         Returns whether forward hardware limit switch is active.
#         """
#         status_bits = self._status_bits
#         mask = 0x00000001
#         return bool(status_bits & mask)

#     @property
#     def is_reverse_hardware_limit_switch_active(self):
#         """
#         Returns whether reverse hardware limit switch is active.
#         """
#         status_bits = self._status_bits
#         mask = 0x00000002
#         return bool(status_bits & mask)

#     @property
#     def is_in_motion(self):
#         """
#         Returns whether motor is in motion.
#         """
#         status_bits = self._status_bits
#         mask = 0x00000010 | 0x00000020 | 0x00000040 | 0x00000080 | 0x00000200
#         return bool(status_bits & mask)

#     @property
#     def has_homing_been_completed(self):
#         """
#         Returns whether homing has been completed at some point.
#         """
#         status_bits = self._status_bits
#         mask = 0x00000400
#         return bool(status_bits & mask)

#     @property
#     def is_tracking(self):
#         """
#         Returns whether motor is tracking.
#         """
#         status_bits = self._status_bits
#         mask = 0x00001000
#         return bool(status_bits & mask)

#     @property
#     def is_settled(self):
#         """
#         Returns whether motor is settled.
#         """
#         status_bits = self._status_bits
#         mask = 0x00002000
#         return bool(status_bits & mask)

#     @property
#     def motor_current_limit_reached(self):
#         """
#         Return whether current limit of motor has been reached.
#         """
#         status_bits = self._status_bits
#         mask = 0x01000000
#         return bool(status_bits & mask)

#     @property
#     def motion_error(self):
#         """
#         Returns whether there is a motion error (= excessing position error).
#         """
#         status_bits = self._status_bits
#         mask = 0x00004000
#         return bool(status_bits & mask)

#     @property
#     def is_channel_enabled(self):
#         """
#         Return whether active channel is enabled.

#         See also
#         --------
#         active_channel
#         """
#         status_bits = self._status_bits
#         mask = 0x80000000
#         return bool(status_bits & mask)

#     @property
#     def active_channel(self):
#         """
#         Active channel number. Used with motors having more than 1 channel.

#         CHAN1_INDEX = 0 : channel 1
#         CHAN2_INDEX = 1 : channel 2
#         """
#         return self._active_channel

#     @active_channel.setter
#     def active_channel(self, channel):
#         err_code = _lib.MOT_SetChannel(self._serial_number, channel)
#         if (err_code != 0):
#             raise Exception("Setting channel %d failed: %s" %
#                     (channel, _get_error_text(err_code)))
#         self._active_channel = channel

#     def enable(self):
#         """
#         Enables the motor (the active channel).
#         """
#         err_code = _lib.MOT_EnableHWChannel(self._serial_number)
#         if (err_code != 0):
#             raise Exception("Enabling channel failed: %s" %
#                     _get_error_text(err_code))

#     def disable(self):
#         """
#         Disables the motor (the active channel).
#         """
#         err_code = _lib.MOT_DisableHWChannel(self._serial_number)
#         if (err_code != 0):
#             raise Exception("Disabling channel failed: %s" %
#                     _get_error_text(err_code))

#     def identify(self):
#         """
#         Flashes the 'Active' LED at the motor to identify it.
#         """
#         err_code = _lib.MOT_Identify(self._serial_number)
#         if (err_code != 0):
#             raise Exception("Identifing device failed: %s" %
#                     _get_error_text(err_code))

#     def get_velocity_parameters(self):
#         """
#         Returns current velocity parameters.

#         Returns
#         -------
#         out : tuple
#             (minimum velocity, acceleration, maximum velocity)
#         """
#         min_vel = ctypes.c_float()
#         accn = ctypes.c_float()
#         max_vel = ctypes.c_float()
#         err_code = _lib.MOT_GetVelParams(self._serial_number,
#                 ctypes.byref(min_vel),
#                 ctypes.byref(accn),
#                 ctypes.byref(max_vel))
#         if (err_code != 0):
#             raise Exception("Getting velocity parameters failed: %s" %
#                     _get_error_text(err_code))
#         return (min_vel.value, accn.value, max_vel.value)

#     def set_velocity_parameters(self, min_vel, accn, max_vel):
#         """
#         Sets velocity parameters. According to the Thorlabs documentation
#         minimum velocity is always 0 and hence is ignored.

#         Parameters
#         ----------
#         min_vel : float
#             minimum velocity
#         accn : float
#             acceleration
#         max_vel : float
#             maximum velocity
#         """
#         err_code = _lib.MOT_SetVelParams(self._serial_number,
#                 min_vel, accn, max_vel)
#         if (err_code != 0):
#             raise Exception("Setting velocity parameters failed: %s" %
#                     _get_error_text(err_code))

#     minimum_velocity = __property_from_index(0, get_velocity_parameters,
#             set_velocity_parameters)
#     """Returns the minimum velocity."""
#     acceleration = __property_from_index(1, get_velocity_parameters,
#             set_velocity_parameters)
#     """Returns the acceleration"""
#     maximum_velocity = __property_from_index(2, get_velocity_parameters,
#             set_velocity_parameters)
#     """Returns the maximum velocity"""

#     def get_velocity_parameter_limits(self):
#         """
#         Returns the maximum acceleration and the maximum velocity of
#         the motor.

#         Returns
#         -------
#         out : tuple
#             (maximum acceleration, maximum velocity)

#         See also
#         --------
#         get_velocity_parameters
#         set_velocity_parameters
#         """
#         max_accn = ctypes.c_float()
#         max_vel = ctypes.c_float()
#         err_code = _lib.MOT_GetVelParamLimits(self._serial_number,
#             ctypes.byref(max_accn), ctypes.byref(max_vel))
#         if (err_code != 0):
#             raise Exception("Getting velocity parameter limits failed: %s" %
#                     _get_error_text(err_code))
#         return (max_accn.value, max_vel.value)

#     @property
#     def acceleration_upper_limit(self):
#         """
#         Returns motor's upper limit of acceleration.

#         Returns
#         -------
#         out : float
#             upper limit
#         """
#         return self.get_velocity_parameter_limits()[0]

#     @property
#     def velocity_upper_limit(self):
#         """
#         Returns motor's upper limit of velocity.

#         Returns
#         -------
#         out : float
#             upper limit
#         """
#         return self.get_velocity_parameter_limits()[1]


#     def get_move_home_parameters(self):
#         """
#         Returns parameters used when homing.

#         Returns
#         -------
#         out : tuple
#             (direction, limiting switch, velocity, zero offset)
#         """
#         direction = ctypes.c_long()
#         lim_switch = ctypes.c_long()
#         velocity = ctypes.c_float()
#         zero_offset = ctypes.c_float()
#         err_code = _lib.MOT_GetHomeParams(self._serial_number,
#                 ctypes.byref(direction),
#                 ctypes.byref(lim_switch),
#                 ctypes.byref(velocity),
#                 ctypes.byref(zero_offset))
#         if (err_code != 0):
#             raise Exception("Getting move home parameters failed: %s" %
#                     _get_error_text(err_code))
#         return (direction.value, lim_switch.value, velocity.value,
#                 zero_offset.value)

#     def set_move_home_parameters(self, direction, lim_switch, velocity,
#             zero_offset):
#         """
#         Sets parameters used when homing.

#         Parameters
#         ----------
#         direction : int
#             home in forward or reverse direction:
#             - HOME_FWD = 1 : Home in the forward direction.
#             - HOME_REV = 2 : Home in the reverse direction.
#         lim_switch : int
#             forward limit switch or reverse limit switch:
#             - HOMELIMSW_FWD = 4 : Use forward limit switch for home datum.
#             - HOMELIMSW_REV = 1 : Use reverse limit switch for home datum.
#         velocity : float
#             velocity of the motor
#         zero_offset : float
#             zero offset
#         """
#         err_code = _lib.MOT_SetHomeParams(self._serial_number, direction,
#                 lim_switch, velocity, zero_offset)
#         if (err_code != 0):
#             raise Exception("Setting move home parameters failed: %s" %
#                     _get_error_text(err_code))

#     move_home_direction = __property_from_index(0,
#             get_move_home_parameters, set_move_home_parameters)
#     """Homing direction (Forward 1, Reverse 2)."""
#     move_home_lim_switch = __property_from_index(1,
#             get_move_home_parameters, set_move_home_parameters)
#     """Home limit switch (forward 4, reverse 1)."""
#     move_home_velocity = __property_from_index(2,
#             get_move_home_parameters, set_move_home_parameters)
#     """Homing velocity."""
#     move_home_zero_offset = __property_from_index(3,
#             get_move_home_parameters, set_move_home_parameters)
#     """Homing zero offset"""

#     def get_motor_parameters(self):
#         """
#         Returns motor parameters.

#         Returns
#         -------
#         out : tuple
#             (steps per revolution, gear box ratio)
#         """
#         steps_per_rev = ctypes.c_long()
#         gear_box_ratio = ctypes.c_long()
#         err_code = _lib.MOT_GetMotorParams(self._serial_number,
#                 ctypes.byref(steps_per_rev),
#                 ctypes.byref(gear_box_ratio))
#         if (err_code != 0):
#             raise Exception("Failed getting motor parameters: %s" %
#                     _get_error_text(err_code))
#         else:
#             return (steps_per_rev.value, gear_box_ratio.value)

#     def set_motor_parameters(self, steps_per_rev, gear_box_ratio):
#         """
#         Sets motor parameters. Note that this is not possible with all motors,
#         see documentation from Thorlabs.

#         Parameters
#         ----------
#         steps_per_rev : int
#             steps per revolution
#         gear_box_ratio : int
#             gear box ratio
#         """
#         err_code = _lib.MOT_SetMotorParams(self._serial_number, steps_per_rev,
#                 gear_box_ratio)
#         if (err_code != 0):
#             raise Exception("Setting motor parameters failed: %s" %
#                     _get_error_text(err_code))

#     steps_per_revolution = __property_from_index(0, get_motor_parameters,
#             set_motor_parameters)
#     """Motor parameter: Steps per revolution"""
#     gear_box_ratio = __property_from_index(1, get_motor_parameters,
#             set_motor_parameters)
#     """Motor parameter: Gear box ratio"""
# #-------------------------------------------------------------------
#     def setVel(self,maxvel):
#         minVel, acc, oldVel = self.get_velocity_parameters()
#         self.set_velocity_parameters(minVel, acc, maxvel)
        
#     def mcAbs(self, absPosition, moveVel=0.5):
#         minVel, acc, oldVel = self.get_velocity_parameters()
#         self.setVel(moveVel)
#         self.move_to(absPosition)
#         self.setVel(oldVel)
        
# #-------------------------------------------------------------------
#     @property
#     def backlash_distance(self):
#         """
#         Backlash distance.
#         """
#         backlash = ctypes.c_float()
#         err_code = _lib.MOT_GetBLashDist(self._serial_number,
#             ctypes.byref(backlash))
#         if (err_code != 0):
#             raise Exception("Failed getting backlash distance: %s" %
#                     _get_error_text(err_code))
#         else:
#             return backlash.value

#     @backlash_distance.setter
#     def backlash_distance(self, value):
#         err_code = _lib.MOT_SetBLashDist(self._serial_number, value)
#         if (err_code != 0):
#             raise Exception("Setting backlash distance failed: %s" %
#                     _get_error_text(err_code))


#     def get_stage_axis_info(self):
#         """
#         Returns axis information of stage.

#         Returns
#         -------
#         out : tuple
#             (minimum position, maximum position, stage units, pitch)
#             - STAGE_UNITS_MM = 1 : Stage units in mm
#             - STAGE_UNITS_DEG = 2 : Stage units in degrees
#         """
#         min_pos = ctypes.c_float()
#         max_pos = ctypes.c_float()
#         units = ctypes.c_long()
#         pitch = ctypes.c_float()
#         err_code = _lib.MOT_GetStageAxisInfo(self._serial_number,
#                 ctypes.byref(min_pos),
#                 ctypes.byref(max_pos),
#                 ctypes.byref(units),
#                 ctypes.byref(pitch))
#         if (err_code != 0):
#             raise Exception("Failed getting stage axis information: %s" %
#                     _get_error_text(err_code))
#         return (min_pos.value, max_pos.value, units.value, pitch.value)

#     def set_stage_axis_info(self, min_pos, max_pos, units, pitch):
#         """
#         Sets axis information of stage.


#         Parameters
#         ----------
#         min_pos : float
#             minimum position
#         max_pos : float
#             maximum position
#         units : int
#             stage units:
#             - STAGE_UNITS_MM = 1 : Stage units in mm
#             - STAGE_UNITS_DEG = 2 : Stage units in degrees
#         pitch : float
#             pitch
#         """
#         err_code = _lib.MOT_SetStageAxisInfo(self._serial_number,
#                 min_pos, max_pos, units, pitch)
#         if (err_code != 0):
#             raise Exception("Setting stage axis info failed: %s" %
#                     _get_error_text(err_code))

#     minimum_position = __property_from_index(0, get_stage_axis_info,
#             set_stage_axis_info)
#     """Stage's minimum position"""
#     maximum_position = __property_from_index(1, get_stage_axis_info,
#             set_stage_axis_info)
#     """Stage's maximum position"""
#     units = __property_from_index(2, get_stage_axis_info,
#             set_stage_axis_info)
#     """Stage's units"""
#     pitch = __property_from_index(3, get_stage_axis_info,
#             set_stage_axis_info)
#     """Stage's pitch"""

#     def get_hardware_limit_switches(self):
#         """
#         Returns hardware limit switch modes for reverse and forward direction.

#         Returns
#         -------
#         out : tuple
#             (reverse limit switch, forward limit switch)
#             HWLIMSWITCH_IGNORE = 1 : Ignore limit switch (e.g. for stages
#                 with only one or no limit switches).
#             HWLIMSWITCH_MAKES = 2	: Limit switch is activated when electrical
#                 continuity is detected.
#             HWLIMSWITCH_BREAKS = 3 : Limit switch is activated when electrical
#                 continuity is broken.
#             HWLIMSWITCH_MAKES_HOMEONLY = 4 : As per HWLIMSWITCH_MAKES except
#                 switch is ignored other than when homing (e.g. to support
#                 rotation stages).
#             HWLIMSWITCH_BREAKS_HOMEONLY = 5 : As per HWLIMSWITCH_BREAKS except
#                 switch is ignored other than when homing (e.g. to support
#                 rotation stages).

#         See also
#         --------
#         set_hardware_limit_switches
#         """
#         rev = ctypes.c_long()
#         fwd = ctypes.c_long()
#         err_code = _lib.MOT_GetHWLimSwitches(self._serial_number,
#                 ctypes.byref(rev), ctypes.byref(fwd))
#         if (err_code != 0):
#             raise Exception("Getting hardware limit switches failed: %s" %
#                     _get_error_text(err_code))
#         return (rev.value, fwd.value)

#     def set_hardware_limit_switches(self, rev, fwd):
#         """
#         Sets hardware limit switches for reverse and forward direction.

#         HWLIMSWITCH_IGNORE = 1 : Ignore limit switch (e.g. for stages
#             with only one or no limit switches).
#         HWLIMSWITCH_MAKES = 2	: Limit switch is activated when electrical
#             continuity is detected.
#         HWLIMSWITCH_BREAKS = 3 : Limit switch is activated when electrical
#             continuity is broken.
#         HWLIMSWITCH_MAKES_HOMEONLY = 4 : As per HWLIMSWITCH_MAKES except
#             switch is ignored other than when homing (e.g. to support
#             rotation stages).
#         HWLIMSWITCH_BREAKS_HOMEONLY = 5 : As per HWLIMSWITCH_BREAKS except
#             switch is ignored other than when homing (e.g. to support
#             rotation stages).

#         Parameters
#         ----------
#         rev : int
#             reverse limit switch
#         fwd : int
#             forward limit switch
#         """
#         err_code = _lib.MOT_SetHWLimSwitches(self._serial_number, rev, fwd)
#         if (err_code != 0):
#             raise Exception("Setting hardware limit switches failed: %s" %
#                     _get_error_text(err_code))

#     reverse_limit_switch = __property_from_index(0,
#             get_hardware_limit_switches,
#             set_hardware_limit_switches)
#     """Reverse limit switch"""
#     forward_limit_switch = __property_from_index(1,
#             get_hardware_limit_switches,
#             set_hardware_limit_switches)
#     """Forward limit switch"""

#     def get_pid_parameters(self):
#         """
#         Returns PID parameters.

#         Returns
#         -------
#         out : tuple
#             (proportional, integrator, differentiator, integrator limit)
#         """
#         proportional = ctypes.c_long()
#         integrator = ctypes.c_long()
#         differentiator = ctypes.c_long()
#         integrator_limit = ctypes.c_long()
#         err_code = _lib.MOT_GetPIDParams(self._serial_number,
#             ctypes.byref(proportional),
#             ctypes.byref(integrator),
#             ctypes.byref(differentiator),
#             ctypes.byref(integrator_limit))
#         if (err_code != 0):
#             raise Exception("Getting PID parameters failed: %s" %
#                     _get_error_text(err_code))
#         return (proportional.value, integrator.value, differentiator.value,
#                 integrator_limit.value)

#     def set_pid_parameters(self, proportional, integrator, differentiator,
#             integrator_limit):
#         """
#         Sets PID parameters.

#         Parameters
#         ----------
#         proportional : int
#         integrator : int
#         differentiator : int
#         integrator_limit : int
#         """
#         err_code = _lib.MOT_SetPIDParams(self._serial_number, proportional,
#             integrator, differentiator, integrator_limit)
#         if (err_code != 0):
#             raise Exception("Setting PID parameters failed: %s" %
#                     _get_error_text(err_code))

#     pid_proportional = __property_from_index(0, get_pid_parameters,
#             set_pid_parameters)
#     """PID controller: Proportional"""
#     pid_integrator = __property_from_index(1, get_pid_parameters,
#             set_pid_parameters)
#     """PID controller: integrator"""
#     pid_differentiator = __property_from_index(2, get_pid_parameters,
#             set_pid_parameters)
#     """PID controller: Differentiator term"""
#     pid_integrator_limit = __property_from_index(3, get_pid_parameters,
#             set_pid_parameters)
#     """PID controller: Integrator limit"""

#     def move_to(self, value, blocking = False):
#         """
#         Move to absolute position.

#         Parameters
#         ----------
#         value : float
#             absolute position of the motor
#         blocking : bool
#             wait until moving is finished.
#             Default: False
#         """
#         err_code = _lib.MOT_MoveAbsoluteEx(self._serial_number, value,
#                 blocking)
#         if (err_code != 0):
#             raise Exception("Setting absolute position failed: %s" %
#                     _get_error_text(err_code))
#         return True
        
        
#     def move_by(self, value, blocking = False):
#         """
#         Move relative to current position.

#         Parameters
#         ----------
#         value : float
#             relative distance
#         blocking : bool
#             wait until moving is finished
#             Default: False
#         """
#         err_code = _lib.MOT_MoveRelativeEx(self._serial_number, value,
#                 blocking)
#         if (err_code != 0):
#             raise Exception("Setting relative position failed: %s" %
#                     _get_error_text(err_code))

#     @property
#     def position(self):
#         """
#         Position of motor. Setting the position is absolute and non-blocking.
#         """
#         pos = ctypes.c_float()
#         err_code = _lib.MOT_GetPosition(self._serial_number,
#                 ctypes.byref(pos))
#         if (err_code != 0):
#             raise Exception("Getting position failed: %s" %
#                     _get_error_text(err_code))
#         return pos.value

#     @position.setter
#     def position(self, value):
#         self.move_to(value, False)


#     def move_home(self, blocking = False):
#         """
#         Move to home position.

#         Parameters
#         ----------
#         blocking : bool
#             wait until homed
#             Default: False
#         """
#         err_code = _lib.MOT_MoveHome(self._serial_number, blocking)
#         if (err_code != 0):
#             raise Exception("Moving velocity failed: %s" %
#                     _get_error_text(err_code))

#     def move_velocity(self, direction):
#         """
#         Parameters
#         ----------
#         direction : int
#             MOVE_FWD = 1 : Move forward
#             MOVE_REV = 2 : Move reverse
#         """
#         err_code = _lib.MOT_MoveVelocity(self._serial_number, direction)
#         if (err_code != 0):
#             raise Exception("Moving velocity failed: %s" %
#                     _get_error_text(err_code))

#     def stop_profiled(self):
#         """
#         Stop motor but turn down velocity slowly (profiled).
#         """
#         err_code = _lib.MOT_StopProfiled(self._serial_number)
#         if (err_code != 0):
#             raise Exception("Stop profiled failed: %s" %
#                     _get_error_text(err_code))

#     def get_dc_current_loop_parameters(self):
#         """
#         Returns DC current loop parameters.

#         Returns
#         -------
#         out : tuple
#             (proportional, integrator, integrator_limit, integrator_dead_band,
#              fast_forward)
#         """
#         proportional = ctypes.c_long()
#         integrator = ctypes.c_long()
#         integrator_limit = ctypes.c_long()
#         integrator_dead_band = ctypes.c_long()
#         fast_forward = ctypes.c_long()
#         err_code = _lib.MOT_GetDCCurrentLoopParams(self._serial_number,
#                 ctypes.byref(proportional),
#                 ctypes.byref(integrator),
#                 ctypes.byref(integrator_limit),
#                 ctypes.byref(integrator_dead_band),
#                 ctypes.byref(fast_forward))
#         if (err_code != 0):
#             raise Exception("Getting DC current loop parameters failed: %s" %
#                     _get_error_text(err_code))
#         return (proportional.value, integrator.value, integrator_limit.value,
#                 integrator_dead_band.value, fast_forward.value)

#     def set_dc_current_loop_parameters(self, proportional, integrator,
#             integrator_limit, integrator_dead_band, fast_forward):
#         """
#         Sets DC current loop parameters.

#         Parameters
#         ----------
#         proportional : int
#         integrator : int
#         integrator_limit : int
#         integrator_dead_band : int
#         fast_forward : int
#         """
#         err_code = _lib.MOT_SetDCCurrentLoopParams(self._serial_number,
#                 proportional, integrator, integrator_limit,
#                 integrator_dead_band, fast_forward)
#         if (err_code != 0):
#             raise Exception("Setting DC current loop parameters failed: %s" %
#                     _get_error_text(err_code))

#     dc_current_loop_proportional = __property_from_index(0,
#             get_dc_current_loop_parameters,
#             set_dc_current_loop_parameters)
#     """DC current loop: proportional term"""
#     dc_current_loop_integrator = __property_from_index(1,
#             get_dc_current_loop_parameters,
#             set_dc_current_loop_parameters)
#     """DC current loop: integrator term"""
#     dc_current_loop_integrator_limit = __property_from_index(2,
#             get_dc_current_loop_parameters,
#             set_dc_current_loop_parameters)
#     """DC current loop: integrator limit"""
#     dc_current_loop_integrator_dead_band = __property_from_index(3,
#             get_dc_current_loop_parameters,
#             set_dc_current_loop_parameters)
#     """DC current loop: integrator dead band"""
#     dc_current_loop_fast_forward = __property_from_index(4,
#             get_dc_current_loop_parameters,
#             set_dc_current_loop_parameters)
#     """DC current loop: fast forward"""

#     def get_dc_position_loop_parameters(self):
#         """
#         Returns DC position loop parameters.

#         Returns
#         -------
#         out : tuple
#             (proportional, integrator, integrator limit, differentiator,
#              differentiator time constant, loop gain, velocity fast forward,
#              acceleration fast forward, position error limit)
#         """
#         proportional = ctypes.c_long()
#         integrator = ctypes.c_long()
#         integrator_limit = ctypes.c_long()
#         differentiator = ctypes.c_long()
#         differentiator_time_constant = ctypes.c_long()
#         loop_gain = ctypes.c_long()
#         velocity_fast_forward = ctypes.c_long()
#         acceleration_fast_forward = ctypes.c_long()
#         position_error_limit = ctypes.c_long()
#         err_code = _lib.MOT_GetDCPositionLoopParams(self._serial_number,
#                 ctypes.byref(proportional),
#                 ctypes.byref(integrator),
#                 ctypes.byref(integrator_limit),
#                 ctypes.byref(differentiator),
#                 ctypes.byref(differentiator_time_constant),
#                 ctypes.byref(loop_gain),
#                 ctypes.byref(velocity_fast_forward),
#                 ctypes.byref(acceleration_fast_forward),
#                 ctypes.byref(position_error_limit))
#         if (err_code != 0):
#             raise Exception("Getting DC position loop parameters failed: %s" %
#                     _get_error_text(err_code))
#         return (proportional.value,
#                 integrator.value,
#                 integrator_limit.value,
#                 differentiator.value,
#                 differentiator_time_constant.value,
#                 loop_gain.value,
#                 velocity_fast_forward.value,
#                 acceleration_fast_forward.value,
#                 position_error_limit.value
#                )

#     def set_dc_position_loop_parameters(self, proportional, integrator,
#             integrator_limit, differentiator, differentiator_time_constant,
#             loop_gain, velocity_fast_forward, acceleration_fast_forward,
#             position_error_limit):
#         """
#         Sets DC position loop parameters.

#         Parameters
#         ----------
#         proportional : int
#         integrator : int
#         integrator_limit : int
#         differentiator : int
#         differentiator_time_constant : int
#         loop_gain : int
#         velocity_fast_forward : int
#         acceleration_fast_forward : int
#         position_error_limit : int
#         """
#         err_code = _lib.MOT_SetDCPositionLoopParams(self._serial_number,
#                 proportional,
#                 integrator,
#                 integrator_limit,
#                 differentiator,
#                 differentiator_time_constant,
#                 loop_gain,
#                 velocity_fast_forward,
#                 acceleration_fast_forward,
#                 position_error_limit)
#         if (err_code != 0):
#             raise Exception("Setting DC position loop parameters failed: %s" %
#                     _get_error_text(err_code))

#     dc_position_loop_proportional = __property_from_index(0,
#             get_dc_position_loop_parameters, set_dc_position_loop_parameters)
#     """DC position loop: proportional term"""
#     dc_position_loop_integrator = __property_from_index(1,
#             get_dc_position_loop_parameters, set_dc_position_loop_parameters)
#     """DC position loop: integrator term"""
#     dc_position_loop_integrator_limit = __property_from_index(2,
#             get_dc_position_loop_parameters, set_dc_position_loop_parameters)
#     """DC position loop: integrator limit"""
#     dc_position_loop_differentiator = __property_from_index(3,
#             get_dc_position_loop_parameters, set_dc_position_loop_parameters)
#     """DC position loop: differentiator"""
#     dc_position_loop_differentiator_time_constant = __property_from_index(4,
#             get_dc_position_loop_parameters, set_dc_position_loop_parameters)
#     """DC position loop: differentiator time constant"""
#     dc_position_loop_gain = __property_from_index(5,
#             get_dc_position_loop_parameters, set_dc_position_loop_parameters)
#     """DC position loop: loop gain"""
#     dc_position_loop_velocity_fast_forward = __property_from_index(6,
#             get_dc_position_loop_parameters, set_dc_position_loop_parameters)
#     """DC position loop: velocity fast forward"""
#     dc_position_loop_acceleration_fast_forward = __property_from_index(7,
#             get_dc_position_loop_parameters, set_dc_position_loop_parameters)
#     """DC position loop: acceleration fast forward"""
#     dc_position_loop_position_error_limit = __property_from_index(8,
#             get_dc_position_loop_parameters, set_dc_position_loop_parameters)
#     """DC position loop: position error limit"""

#     def get_dc_motor_output_parameters(self):
#         """
#         Returns DC motor output parameters.

#         Returns
#         -------
#         out : tuple
#             (continuous current limit, energy limit, motor limit, motor bias)
#         """
#         continuous_current_limit = ctypes.c_float()
#         energy_limit = ctypes.c_float()
#         motor_limit = ctypes.c_float()
#         motor_bias = ctypes.c_float()
#         err_code = _lib.MOT_GetDCMotorOutputParams(self._serial_number,
#                 ctypes.byref(continuous_current_limit),
#                 ctypes.byref(energy_limit),
#                 ctypes.byref(motor_limit),
#                 ctypes.byref(motor_bias))
#         if (err_code != 0):
#             raise Exception("Getting DC motor output parameters failed: %s" %
#                     _get_error_text(err_code))
#         return (continuous_current_limit.value,
#                 energy_limit.value,
#                 motor_limit.value,
#                 motor_bias.value
#                )

#     def set_dc_motor_output_parameters(self, continuous_current_limit,
#             energy_limit, motor_limit, motor_bias):
#         """
#         Sets DC motor output parameters.

#         Parameters
#         ----------
#         continuous_current_limit : float
#         energy_limit : float
#         motor_limit : float
#         motor_bias : float
#         """
#         err_code = _lib.MOT_SetDCMotorOutputParams(self._serial_number,
#                 continuous_current_limit,
#                 energy_limit,
#                 motor_limit,
#                 motor_bias)
#         if (err_code != 0):
#             raise Exception("Setting DC motor output parameters failed: %s" %
#                     _get_error_text(err_code))

#     dc_motor_output_continuous_current_limit = __property_from_index(0,
#             get_dc_motor_output_parameters, set_dc_motor_output_parameters)
#     """DC motor output: continuous current limit"""
#     dc_motor_output_energy_limit = __property_from_index(1,
#             get_dc_motor_output_parameters, set_dc_motor_output_parameters)
#     """DC motor output: energy limit"""
#     dc_motor_output_motor_limit = __property_from_index(2,
#             get_dc_motor_output_parameters, set_dc_motor_output_parameters)
#     """DC motor output: motor limit"""
#     dc_motor_output_motor_bias = __property_from_index(3,
#             get_dc_motor_output_parameters, set_dc_motor_output_parameters)
#     """DC motor output: motor bias"""


#     def get_dc_track_settle_parameters(self):
#         """
#         Returns DC track settle parameters.

#         Returns
#         -------
#         out : tuple
#             (settle time, settle window, track window)
#         """
#         settle_time = ctypes.c_long()
#         settle_window = ctypes.c_long()
#         track_window = ctypes.c_long()
#         err_code = _lib.MOT_GetDCTrackSettleParams(self._serial_number,
#                 ctypes.byref(settle_time),
#                 ctypes.byref(settle_window),
#                 ctypes.byref(track_window))
#         if (err_code != 0):
#             raise Exception("Getting DC track settle parameters failed: %s" %
#                     _get_error_text(err_code))
#         return (settle_time.value,
#                 settle_window.value,
#                 track_window.value
#                )

#     def set_dc_track_settle_parameters(self, settle_time, settle_window,
#             track_window):
#         """
#         Sets track settle parameters.

#         Parameters
#         ----------
#         settle_time : int
#         settle_window : int
#         track_window : int
#         """
#         err_code = _lib.MOT_SetDCTrackSettleParams(self._serial_number,
#                 settle_time,
#                 settle_window,
#                 track_window)
#         if (err_code != 0):
#             raise Exception("Setting DC track settle parameters failed: %s" %
#                     _get_error_text(err_code))

#     dc_track_settle_settle_time = __property_from_index(0,
#             get_dc_track_settle_parameters, set_dc_track_settle_parameters)
#     """DC track settle: settle time"""
#     dc_track_settle_settle_window = __property_from_index(1,
#             get_dc_track_settle_parameters, set_dc_track_settle_parameters)
#     """DC track settle: settle window"""
#     dc_track_settle_track_window = __property_from_index(2,
#             get_dc_track_settle_parameters, set_dc_track_settle_parameters)
#     """DC track settle: track window"""


#     def get_dc_profile_mode_parameters(self):
#         """
#         Returns DC profile mode parameters.


#         Returns
#         -------
#         out : tuple
#             (profile mode, jerk)

#             Profile mode:
#             - DC_PROFILEMODE_TRAPEZOIDAL = 0
#             - DC_PROFILEMODE_SCURVE = 2
#         """
#         profile_mode = ctypes.c_long()
#         jerk = ctypes.c_float()
#         err_code = _lib.MOT_GetDCProfileModeParams(self._serial_number,
#                 ctypes.byref(profile_mode),
#                 ctypes.byref(jerk))
#         if (err_code != 0):
#             raise Exception("Getting DC profile mode parameters failed: %s" %
#                     _get_error_text(err_code))
#         return (profile_mode.value,
#                 jerk.value
#                )

#     def set_dc_profile_mode_parameters(self, profile_mode, jerk):
#         """
#         Sets DC profile mode parameters.

#         Parameters
#         ----------
#         profile_mode : int
#             - DC_PROFILEMODE_TRAPEZOIDAL = 0
#             - DC_PROFILEMODE_SCURVE = 2
#         jerk : float
#         """
#         err_code = _lib.MOT_SetDCTrackSettleParams(self._serial_number,
#                 profile_mode,
#                 jerk)
#         if (err_code != 0):
#             raise Exception("Setting DC profile mode parameters failed: %s" %
#                     _get_error_text(err_code))

#     dc_profile_mode = __property_from_index(0,
#             get_dc_profile_mode_parameters, set_dc_profile_mode_parameters)
#     """DC profile mode: profile mode"""
#     dc_profile_mode_jerk = __property_from_index(1,
#             get_dc_profile_mode_parameters, set_dc_profile_mode_parameters)
#     """DC profile mode: jerk"""

#     def get_dc_joystick_parameters(self):
#         """
#         Returns DC joystick parameters.

#         Returns
#         -------
#         out : tuple
#             (maximum velocity lo, maximum velocity hi, acceleration lo,
#              acceleration hi, direction sense)
#             direction sense:
#             - DC_JS_DIRSENSE_POS = 1
#             - DC_JS_DIRSENSE_NEG = 2
#         """
#         maximum_velocity_lo = ctypes.c_float()
#         maximum_velocity_hi = ctypes.c_float()
#         acceleration_lo = ctypes.c_float()
#         acceleration_hi = ctypes.c_float()
#         direction_sense = ctypes.c_long()
#         err_code = _lib.MOT_GetDCJoystickParams(self._serial_number,
#                 ctypes.byref(maximum_velocity_lo),
#                 ctypes.byref(maximum_velocity_hi),
#                 ctypes.byref(acceleration_lo),
#                 ctypes.byref(acceleration_hi),
#                 ctypes.byref(direction_sense))
#         if (err_code != 0):
#             raise Exception("Getting DC joystick parameters failed: %s" %
#                     _get_error_text(err_code))
#         return (maximum_velocity_lo.value,
#                 maximum_velocity_hi.value,
#                 acceleration_lo.value,
#                 acceleration_hi.value,
#                 direction_sense.value
#                )

#     def set_dc_joystick_parameters(self, maximum_velocity_lo,
#             maximum_velocity_hi, acceleration_lo, acceleration_hi,
#             direction_sense):
#         """
#         Sets DC joystick parameters.

#         Parameters
#         ----------
#         maximum_velocity_lo : float
#         maximum_velocity_hi : float
#         acceleration_lo : float
#         acceleration_hi : float
#         direction_sense : int
#             - DC_JS_DIRSENSE_POS = 1
#             - DC_JS_DIRSENSE_NEG = 2
#         """
#         err_code = _lib.MOT_SetDCJoystickParams(self._serial_number,
#                 maximum_velocity_lo,
#                 maximum_velocity_hi,
#                 acceleration_lo,
#                 acceleration_hi)
#         if (err_code != 0):
#             raise Exception("Setting DC joystick parameters failed: %s" %
#                     _get_error_text(err_code))

#     dc_joystick_maximum_velocity_lo = __property_from_index(0,
#             get_dc_joystick_parameters, set_dc_joystick_parameters)
#     """DC joystick: maximum velocity lo"""
#     dc_joystick_maximum_velocity_hi = __property_from_index(1,
#             get_dc_joystick_parameters, set_dc_joystick_parameters)
#     """DC joystick: maximum velocity hi"""
#     dc_joystick_acceleration_lo = __property_from_index(2,
#             get_dc_joystick_parameters, set_dc_joystick_parameters)
#     """DC joystick: acceleration lo"""
#     dc_joystick_acceleration_hi = __property_from_index(3,
#             get_dc_joystick_parameters, set_dc_joystick_parameters)
#     """DC joystick: acceleration hi"""
#     dc_joystick_direction_sense = __property_from_index(4,
#             get_dc_joystick_parameters, set_dc_joystick_parameters)
#     """DC joystick: direction sense"""

#     def get_dc_settled_current_loop_parameters(self):
#         """
#         Returns DC settled current loop parameters.

#         Returns
#         -------
#         out : tuple
#             (proportional, integrator, integrator_limit, integrator dead band,
#              fast forward)
#         """
#         settled_proportional = ctypes.c_long()
#         settled_integrator = ctypes.c_long()
#         settled_integrator_limit = ctypes.c_long()
#         settled_integrator_dead_band = ctypes.c_long()
#         settled_fast_forward = ctypes.c_long()
#         err_code = _lib.MOT_GetDCSettledCurrentLoopParams(self._serial_number,
#                 ctypes.byref(settled_proportional),
#                 ctypes.byref(settled_integrator),
#                 ctypes.byref(settled_integrator_limit),
#                 ctypes.byref(settled_integrator_dead_band),
#                 ctypes.byref(settled_fast_forward))
#         if (err_code != 0):
#             raise Exception("Getting DC settled current loop parameters " \
#                     "failed: %s" % _get_error_text(err_code))
#         return (settled_proportional.value,
#                 settled_integrator.value,
#                 settled_integrator_limit.value,
#                 settled_integrator_dead_band.value,
#                 settled_fast_forward.value
#                )

#     def set_dc_settled_current_loop_parameters(self, settled_proportional,
#             settled_integrator, settled_integrator_limit,
#             settled_integrator_dead_band, settled_fast_forward):
#         """
#         Sets DC settled current loop parameters.

#         Parameters
#         ----------
#         settled_proportional : int
#         settled_integrator : int
#         settled_integrator_limit : int
#         settled_integrator_dead_band : int
#         settled_fast_forward : int
#         """
#         err_code = _lib.MOT_SetDCJoystickParams(self._serial_number,
#                 settled_proportional,
#                 settled_integrator,
#                 settled_integrator_limit,
#                 settled_integrator_dead_band,
#                 settled_fast_forward)
#         if (err_code != 0):
#             raise Exception("Setting DC settled current loop parameters " \
#                     "failed: %s" % _get_error_text(err_code))

#     dc_settled_current_loop_proportional = __property_from_index(0,
#             get_dc_settled_current_loop_parameters,
#             set_dc_settled_current_loop_parameters)
#     """DC settled current loop: proportional term"""
#     dc_settled_current_loop_integrator = __property_from_index(1,
#             get_dc_settled_current_loop_parameters,
#             set_dc_settled_current_loop_parameters)
#     """DC settled current loop: integrator term"""
#     dc_settled_current_loop_integrator_limit = __property_from_index(2,
#             get_dc_settled_current_loop_parameters,
#             set_dc_settled_current_loop_parameters)
#     """DC settled current loop: integrator limit"""
#     dc_settled_current_loop_integrator_dead_band = __property_from_index(3,
#             get_dc_settled_current_loop_parameters,
#             set_dc_settled_current_loop_parameters)
#     """DC settled current loop: integrator dead band"""
#     dc_settled_current_loop_fast_forward = __property_from_index(4,
#             get_dc_settled_current_loop_parameters,
#             set_dc_settled_current_loop_parameters)
#     """DC settled current loop: fast forward"""


# def _load_library():
#     """
#     Loads the APT.dll shared library. Calls APTInit.
#     """
#     # load library
#     if (os.name != 'nt'):
#         raise Exception("Your operating system is not supported. " \
#                 "Thorlabs' APT API only works on Windows.")
#     lib = None
#     filename = ctypes.util.find_library("APT")
#     if (filename is not None):
#         lib = ctypes.windll.LoadLibrary(filename)
#     else:
#         filename = "%s/APT.dll" % os.path.dirname(__file__)
#         lib = ctypes.windll.LoadLibrary(filename)
#         if (lib is None):
#             filename = "%s/APT.dll" % os.path.dirname(sys.argv[0])
#             lib = ctypes.windll.LoadLibrary(lib)
#             if (lib is None):
#                 raise Exception("Could not find shared library APT.dll.")
#     _APTAPI.set_ctypes_argtypes(lib)
#     err_code = lib.APTInit()
#     if (err_code != 0):
#         raise Exception("Thorlabs APT Initialization failed: " \
#                         "%s" % _get_error_text(err_code))
#     if (lib.EnableEventDlg(False) != 0):
#         raise Exception("Couldn't disable event dialog.")
#     return lib

# _lib = None
# _lib = _load_library()

# import atexit
# @atexit.register
# def _cleanup():
#     """
#     Calls APTCleanUp
#     """
#     if (_lib is not None):
#         _lib.APTCleanUp()





########################################################################

class APTMotor(Motor):
    def __init__(self, SerialNum=None, HWTYPE=31, verbose=False, dllname='APT.dll'):
        '''
        HWTYPE_BSC001		11	// 1 Ch benchtop stepper driver
        HWTYPE_BSC101		12	// 1 Ch benchtop stepper driver
        HWTYPE_BSC002		13	// 2 Ch benchtop stepper driver
        HWTYPE_BDC101		14	// 1 Ch benchtop DC servo driver
        HWTYPE_SCC001		21	// 1 Ch stepper driver card (used within BSC102,103 units)
        HWTYPE_DCC001		22	// 1 Ch DC servo driver card (used within BDC102,103 units)
        HWTYPE_ODC001		24	// 1 Ch DC servo driver cube
        HWTYPE_OST001		25	// 1 Ch stepper driver cube
        HWTYPE_MST601		26	// 2 Ch modular stepper driver module
        HWTYPE_TST001		29	// 1 Ch Stepper driver T-Cube
        HWTYPE_TDC001		31	// 1 Ch DC servo driver T-Cube
        HWTYPE_LTSXXX		42	// LTS300/LTS150 Long Travel Integrated Driver/Stages
        HWTYPE_L490MZ		43	// L490MZ Integrated Driver/Labjack
        HWTYPE_BBD10X		44	// 1/2/3 Ch benchtop brushless DC servo driver
        '''

        self.verbose = verbose
        self.Connected = False
        if not os.path.exists(dllname):
            print ("ERROR: DLL not found")
        self.aptdll = windll.LoadLibrary(dllname)
        self.aptdll.EnableEventDlg(True)
        self.aptdll.APTInit()
        #print 'APT initialized'
        self.HWType = c_long(HWTYPE)
        self.blCorr = 0.10 #100um backlash correction
        if SerialNum is not None:
            if self.verbose: print ("Serial is", SerialNum)
            self.SerialNum = c_long(SerialNum)
            self.initializeHardwareDevice()
        # TODO : Error reporting to know if initialisation went sucessfully or not.

        else:
            if self.verbose: print ("No serial, please setSerialNumber")
            
            
            
            
    def stop_profiled(self):
        
        """
        Stop motor but turn down velocity slowly (profiled).
        """
        err_code = _lib.MOT_StopProfiled(self._serial_number)
        if (err_code != 0):
            raise Exception("Stop profiled failed: %s" %
                    _get_error_text(err_code))
    
    
    
    
    
    
    
    def getNumberOfHardwareUnits(self):
        '''
        Returns the number of HW units connected that are available to be interfaced
        '''
        numUnits = c_long()
        self.aptdll.GetNumHWUnitsEx(self.HWType, pointer(numUnits))
        return numUnits.value


    def getSerialNumberByIdx(self, index):
        '''
        Returns the Serial Number of the specified index
        '''
        HWSerialNum = c_long()
        hardwareIndex = c_long(index)
        self.aptdll.GetHWSerialNumEx(self.HWType, hardwareIndex, pointer(HWSerialNum))
        return HWSerialNum

    def setSerialNumber(self, SerialNum):
        '''
        Sets the Serial Number of the specified index
        '''
        if self.verbose: print ("Serial is", SerialNum)
        self.SerialNum = c_long(SerialNum)
        return self.SerialNum.value

    def initializeHardwareDevice(self):
        '''
        Initialises the motor.
        You can only get the position of the motor and move the motor after it has been initialised.
        Once initiallised, it will not respond to other objects trying to control it, until released.
        '''
        if self.verbose: print ('initializeHardwareDevice serial', self.SerialNum)
        result = self.aptdll.InitHWDevice(self.SerialNum)
        if result == 0:
            self.Connected = True
            if self.verbose: print ('initializeHardwareDevice connection SUCESS')
        # need some kind of error reporting here
        else:
            raise Exception('Connection Failed. Check Serial Number!')
        return True

        ''' Interfacing with the motor settings '''
    def getHardwareInformation(self):
        model = c_buffer(255)
        softwareVersion = c_buffer(255)
        hardwareNotes = c_buffer(255)
        self.aptdll.GetHWInfo(self.SerialNum, model, 255, softwareVersion, 255, hardwareNotes, 255)
        hwinfo = [model.value, softwareVersion.value, hardwareNotes.value]
        return hwinfo

    def getStageAxisInformation(self):
        minimumPosition = c_float()
        maximumPosition = c_float()
        units = c_long()
        pitch = c_float()
        self.aptdll.MOT_GetStageAxisInfo(self.SerialNum, pointer(minimumPosition), pointer(maximumPosition), pointer(units), pointer(pitch))
        stageAxisInformation = [minimumPosition.value, maximumPosition.value, units.value, pitch.value]
        return stageAxisInformation

    def setStageAxisInformation(self, stageAxisInformation):
        minimumPosition = c_float(stageAxisInformation[0])
        maximumPosition = c_float(stageAxisInformation[1])
        units = c_long(stageAxisInformation[2])#2 is degree
        # Get different pitches of lead screw for moving stages for different stages.
        pitch = c_float(stageAxisInformation[3])
        self.aptdll.MOT_SetStageAxisInfo(self.SerialNum, minimumPosition, maximumPosition, units, pitch)
        return True

    def getHardwareLimitSwitches(self):
        reverseLimitSwitch = c_long()
        forwardLimitSwitch = c_long()
        self.aptdll.MOT_GetHWLimSwitches(self.SerialNum, pointer(reverseLimitSwitch), pointer(forwardLimitSwitch))
        hardwareLimitSwitches = [reverseLimitSwitch.value, forwardLimitSwitch.value]
        return hardwareLimitSwitches

    def getVelocityParameters(self):
        minimumVelocity = c_float()
        acceleration = c_float()
        maximumVelocity = c_float()
        self.aptdll.MOT_GetVelParams(self.SerialNum, pointer(minimumVelocity), pointer(acceleration), pointer(maximumVelocity))
        velocityParameters = [minimumVelocity.value, acceleration.value, maximumVelocity.value]
        return velocityParameters

    def getVel(self):
        if self.verbose: print ('getVel probing...')
        minVel, acc, maxVel = self.getVelocityParameters()
        if self.verbose: print ('getVel maxVel')
        return maxVel


    def setVelocityParameters(self, minVel, acc, maxVel):
        minimumVelocity = c_float(minVel)
        acceleration = c_float(acc)
        maximumVelocity = c_float(maxVel)
        self.aptdll.MOT_SetVelParams(self.SerialNum, minimumVelocity, acceleration, maximumVelocity)
        return True

    def setVel(self, maxVel):
        if self.verbose: print ('setVel', maxVel)
        minVel, acc, oldVel = self.getVelocityParameters()
        self.setVelocityParameters(minVel, acc, maxVel)
        return True

    def getVelocityParameterLimits(self):
        maximumAcceleration = c_float()
        maximumVelocity = c_float()
        self.aptdll.MOT_GetVelParamLimits(self.SerialNum, pointer(maximumAcceleration), pointer(maximumVelocity))
        velocityParameterLimits = [maximumAcceleration.value, maximumVelocity.value]
        return velocityParameterLimits

        '''
        Controlling the motors
        m = move
        c = controlled velocity
        b = backlash correction

        Rel = relative distance from current position.
        Abs = absolute position
        '''
    def getPos(self):
        '''
        Obtain the current absolute position of the stage
        '''
        if self.verbose: print ('getPos probing...')
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')

        position = c_float()
        self.aptdll.MOT_GetPosition(self.SerialNum, pointer(position))
        if self.verbose: print ('getPos ', position.value)
        return position.value

    def mRel(self, relDistance):
        '''
        Moves the motor a relative distance specified
        relDistance    float     Relative position desired
        '''
        if self.verbose: print ('mRel ', relDistance, c_float(relDistance))
        if not self.Connected:
            print ('Please connect first! Use initializeHardwareDevice')
            #raise Exception('Please connect first! Use initializeHardwareDevice')
        relativeDistance = c_float(relDistance)
        self.aptdll.MOT_MoveRelativeEx(self.SerialNum, relativeDistance, True)
        if self.verbose: print ('mRel SUCESS')
        return True

    def mAbs(self, absPosition):
        '''
        Moves the motor to the Absolute position specified
        absPosition    float     Position desired
        '''
        if self.verbose: print ('mAbs ', absPosition, c_float(absPosition))
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')
        absolutePosition = c_float(absPosition)
        self.aptdll.MOT_MoveAbsoluteEx(self.SerialNum, absolutePosition, True)
        if self.verbose: print ('mAbs SUCESS')
        return True

    def mcRel(self, relDistance, moveVel=0.5):
        '''
        Moves the motor a relative distance specified at a controlled velocity
        relDistance    float     Relative position desired
        moveVel        float     Motor velocity, mm/sec
        '''
        if self.verbose: print ('mcRel ', relDistance, c_float(relDistance), 'mVel', moveVel)
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')
        # Save velocities to reset after move
        maxVel = self.getVelocityParameterLimits()[1]
        # Set new desired max velocity
        self.setVel(moveVel)
        self.mRel(relDistance)
        self.setVel(maxVel)
        if self.verbose: print ('mcRel SUCESS')
        return True

    def mcAbs(self, absPosition, moveVel=0.5):
        '''
        Moves the motor to the Absolute position specified at a controlled velocity
        absPosition    float     Position desired
        moveVel        float     Motor velocity, mm/sec
        '''
        if self.verbose: print ('mcAbs ', absPosition, c_float(absPosition), 'mVel', moveVel)
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')
        # Save velocities to reset after move
        minVel, acc, maxVel = self.getVelocityParameters()
        # Set new desired max velocity
        self.setVel(moveVel)
        self.mAbs(absPosition)
        self.setVel(maxVel)
        if self.verbose: print ('mcAbs SUCESS')
        return True

    def mbRel(self, relDistance):
        '''
        Moves the motor a relative distance specified
        relDistance    float     Relative position desired
        '''
        if self.verbose: print ('mbRel ', relDistance, c_float(relDistance))
        if not self.Connected:
            print ('Please connect first! Use initializeHardwareDevice')
            #raise Exception('Please connect first! Use initializeHardwareDevice')
        self.mRel(relDistance-self.blCorr)
        self.mRel(self.blCorr)
        if self.verbose: print ('mbRel SUCESS')
        return True

    def mbAbs(self, absPosition):
        '''
        Moves the motor to the Absolute position specified
        absPosition    float     Position desired
        '''
        if self.verbose: print ('mbAbs ', absPosition, c_float(absPosition))
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')
        if (absPosition < self.getPos()):
            if self.verbose: print ('backlash mAbs', absPosition) - self.blCorr
            self.mAbs(absPosition-self.blCorr)
        self.mAbs(absPosition)
        if self.verbose: print ('mbAbs SUCESS')
        return True


    def go_home(self):
        '''
        Move the stage to home position and reset position entry
        '''
        if self.verbose: print ('Going home')
        if not self.Connected:
            raise Exception('Please connect first! Use initializeHardwareDevice')
        if self.verbose: print ('go_home SUCESS')
        self.aptdll.MOT_MoveHome(self.SerialNum)
        return True


        ''' Miscelaneous '''
    def identify(self):
        '''
        Causes the motor to blink the Active LED
        '''
        self.aptdll.MOT_Identify(self.SerialNum)
        return True

    def cleanUpAPT(self):
        '''
        Releases the APT object
        Use when exiting the program
        '''
        self.aptdll.APTCleanUp()
        if self.verbose: print ('APT cleaned up')
        self.Connected = False
