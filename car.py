"""
 Copyright (C) 2023 Aaron E-J

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as
 published by the Free Software Foundation, either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.
 """
# %%
from cProfile import label
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
os.add_dll_directory("C:\\Users\\Someone\\micromamba\\envs\\oshoe\\Lib\\site-packages\\win32\\")
os.add_dll_directory("c:/Users/Someone/micromamba/envs/oshoe/lib/site-packages/cadquery/")
# from scipy.optimize import fsolve
# from latex2sympy2 import latex2sympy
from sympy.physics.units.quantities import Quantity
from IPython.display import Image
from IPython.display import display
from IPython.core.interactiveshell import InteractiveShell
from nbconvert.preprocessors import ExecutePreprocessor
import matplotlib.pyplot as plt
import numpy as np
# import scipy as sc
# import scipy.linalg as li
# import sympy as sy
# from scipy.integrate import odeint
# from sympy.parsing.latex import parse_latex
from re import T
import cadquery as cq
from cq_warehouse.sprocket import Sprocket
import cq_warehouse as cqw
from cq_warehouse.fastener import *
import cq_warehouse.extensions
from cadquery import exporters
# import matplotlib
import matplotlib.pyplot as plt
from IPython.display import Image
from IPython.display import display
from IPython.core.interactiveshell import InteractiveShell
from nbconvert.preprocessors import ExecutePreprocessor
from IPython.core.display import HTML
import numpy as np
from typing import Union
from build123d import *
from cq_gears import (SpurGear, HerringboneGear, RackGear, HerringboneRackGear,
                      PlanetaryGearset, HerringbonePlanetaryGearset,
                      BevelGearPair, Worm, CrossedGearPair, HyperbolicGearPair,
                      RingGear, HerringboneRingGear, BevelGear)
from cq_gears import SpurGear, HerringboneGear, RackGear, HerringboneRackGear
from math import pi
import copy
# from jupyter_cadquery import Part, PartGroup, show, open_viewer
plt.rcParams['figure.figsize'] = [9, 9]
InteractiveShell.ast_node_interactivity = "all"
np.random.default_rng()
np.set_printoptions(suppress=True)
def scaleMe(self: T, howMuch) -> T:
    return self.scale(howMuch)
def cq2b3d(cq_obj):
    """Convert a CADQuery solid to a Build123d solid
    
    Args:
        cq_obj (solid): The CADQuery solid to be converted to Build123d
    Returns:
        solid: a Build 123d solid
    """
    solid = Solid.make_box(1, 1, 1)
    solid.wrapped = cq_obj.wrapped or cq_obj.val().wrapped
    return solid
breadboard =import_step('../../rccar/64HalfsizeBreadboard.step')
type(breadboard)
# %% ###Motor###
def makeMotor():
    """Make a motor
    
    Returns:
        Part: a generic motor part object for placement in robots
    """
    alignMotor = (Align.CENTER, Align.CENTER, Align.MIN)
    motor = Pos(0, 0, 0) * Cylinder(radius=.75, height=40, align=alignMotor)\
        + Pos(0, 0, 10) * Cylinder(3.475, 2, align=alignMotor)\
        + Pos(0, 0, 12) * Cylinder(8.5, 3, align=alignMotor)\
        + ((Pos(0, 0, 15) * Cylinder(radius=10, height=26, align=alignMotor)
            + Pos(0, 0, 41) * Cylinder(radius=4, height=1, align=alignMotor))
           - Pos(0, 0, 0) * Cylinder(radius=.75, height=44, align=alignMotor))\
        # - Pos(5, 0, 0) * Cylinder(radius=.75, height=30, align=alignMotor)\
        # - Pos(-5, 0, 0) * Cylinder(radius=.75, height=30, align=alignMotor)
    return motor
frontMotor = makeMotor()
rearMotor=makeMotor()
### Bolts to hold the motor###
boltM1612 = SocketHeadCapScrew(size='M1.6-0.35', length=12,
                          fastener_type='iso4762', simple=False)
boltM1612 = cq2b3d(boltM1612)
# %% ## Gear Stuff##
### Larger gear for changing rotation speed###
ratioGear = SpurGear(module=.5, teeth_number=43, width=2, bore_d=1.6)
rg_pitchR = ratioGear.r0  # pitch radius
ratioGear = cq2b3d(ratioGear.build())
### Smaller Gear inside larger gear###
smallGear = SpurGear(module=.5, teeth_number=17,width=2, bore_d=1.6)
sg_pitchR=smallGear.r0
smallGear=cq2b3d(smallGear.build())
### Front Motor Gear###
motorGear = SpurGear(module=.5, teeth_number=13, width=4, bore_d=1.6)
mg_pitchR = motorGear.r0  # pitch radius
motorGear = cq2b3d(motorGear.build())
### Back Motor Gear###
bMotorGear = SpurGear(module=.5, teeth_number=67, width=2, bore_d=1.5)
bg_pitchR = bMotorGear.r0  # pitch radius
bMotorGear = cq2b3d(bMotorGear.build())
### Back Wheel Gear###
bWMotorGear = SpurGear(module=.5, teeth_number=13, width=2, bore_d=2)
bWg_pitchR = bWMotorGear.r0  # pitch radius
bWg_Width = bWMotorGear.ra
bWMotorGear = cq2b3d(bWMotorGear.build())
difference_btwn_M_W_Gears=(bg_pitchR+bWg_pitchR)
rearBGearRadAtAngleX=40+difference_btwn_M_W_Gears*np.cos(np.deg2rad(-47))
rearBGearRadAtAngleY=11.5+difference_btwn_M_W_Gears*np.sin(np.deg2rad(-47))
# %% ### Gear connected to turning rod ###
turnGear=SpurGear(module=.5,teeth_number=61,width=2,bore_d=2,missing_teeth=(4,56))
tg_pitchR=turnGear.r0
difference_between_farther_gears=sg_pitchR+tg_pitchR
turnGear=cq2b3d(turnGear.build()).transformed((0,0,0),(0,0,0))
turnGear=Part()+turnGear-Cylinder(radius=tg_pitchR,height=4,arc_size=295
                                  ).transformed((0,0,32),(0,0,0))\
    +Box(length=4.5+tg_pitchR/2,width=6,height=2,align=(Align.MAX,Align.CENTER, Align.MIN)).transformed((0,0,0),(difference_between_farther_gears/2,0, 0))\
    - Box(length=4.5,width=2.5,height=8,align=(Align.MAX, Align.CENTER, Align.MIN)).transformed((0,0,0),((difference_between_farther_gears/2)-2,0, 0))

# turnGear
#%% ###Initiate Bolts###
difference_between_closer_gears = ((rg_pitchR) + (mg_pitchR))
# SocketHeadCapScrew.sizes('iso4762')
boltM1620 = SocketHeadCapScrew(size='M1.6-0.35', length=20,
                          fastener_type='iso4762', simple=False)
boltM1620=cq2b3d(boltM1620)
boltM235 = SocketHeadCapScrew(size='M2-0.4', length=25,
                          fastener_type='iso4762', simple=False)
boltM235=cq2b3d(boltM235)
bolts = [boltM1612.transformed((180, 0, 0), (-35, difference_between_closer_gears, 0)),
         boltM1612.transformed((180, 0, 0), (-45, difference_between_closer_gears, 0)),
         boltM235.transformed((0,0,0), (52.5,-23,24.5)),]
#%% ###Various holes in the chassis###
holes = [Cylinder(2, 4).transformed((0, 0, 0), (0, -20, 0)),
         Cylinder(2, 4).transformed((0, 0, 0), (0, 20, 0)),
         Cylinder(2, 4).transformed(
             (0, 0, 0), (-40, difference_between_closer_gears, 0)),
         Cylinder(.75, 4).transformed(
             (0, 0, 0), (-45, difference_between_closer_gears, 0)),
         Cylinder(.75, 4).transformed(
             (0, 0, 0), (-35, difference_between_closer_gears, 0)),
         Cylinder(1,40).transformed((0,0,0), (52.5,-23,1.5)),
         Cylinder(1,40).transformed((0,0,0), (27.5,-23,1.5)),
         Cylinder(1,40).transformed((0,0,0), (52.5,-10,1.5)),
         Cylinder(1,40).transformed((0,0,0), (27.5,-10,1.5)),
         Box(35,4,10).transformed((0,0,0), (40,1.25,1.5))]
alignBox = (Align.CENTER, Align.CENTER, Align.MIN)
# %% ###Turning Rod###
turningConnectorDim=[(4,43),(0,43),(0,20),(8,10),(8,-10),(0,-20),(0,-43),(4,-43),(4,-20),(12,-10),(12,10),(4,20)]
turningConnector=extrude(Polygon(*turningConnectorDim),4
                         ).transformed((0,0,0),(-38-difference_between_farther_gears,0, 0))\
    -Box(10,15,4,align=(Align.MIN, Align.CENTER, Align.CENTER)).transformed((0,0,0),(-36-difference_between_farther_gears,0, 0))\
    -Box(4,7,1.5,align=(Align.MAX, Align.MAX, Align.MIN)).transformed((0,0,0),(-40-difference_between_farther_gears,43, 0))\
    -Box(4,7,1.5,align=(Align.MAX, Align.MIN, Align.MIN)).transformed((0,0,0),(-40-difference_between_farther_gears,-43, 0))\
    -Cylinder(1.05,8).transformed((0,0,0),(-42-difference_between_farther_gears,40, 0))\
    -Cylinder(1.05,8).transformed((0,0,0),(-42-difference_between_farther_gears,-40, 0))\
    +Cylinder(1,4.0).transformed((0,0,0),(-34-difference_between_farther_gears,0, 0))\
    +Cylinder(1,8.0).transformed((45,0,0),(-42-difference_between_farther_gears,28, 0))\
    +Cylinder(1,8.0).transformed((-45,0,0),(-42-difference_between_farther_gears,-28, 0))
# turningConnector
#%% ###The Rear Motor Assembly###
rMotorAssemb=Box(30,4,23,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (0,-10,1.5))\
    + Box(30,4,23,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (0,-23,1.5))\
    -Cylinder(1,40,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (12.5,-23,1.5))\
    -Cylinder(1,40,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (-12.5,-23,1.5))\
    -Cylinder(1,40,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (12.5,-10,1.5))\
    -Cylinder(1,40,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (-12.5,-10,1.5))\
    - rearMotor.transformed((90,0,0),(0,10,11.5))\
    -Box(30,40,12.5,align=(Align.CENTER,Align.CENTER,Align.MAX)).transformed((0,0,0),(0,-22,11.5))\
    + rearMotor.transformed((90,0,0),(0,10,11.5))
# rMotorAssemb
#%% ###Front Axle Attachment###
frontAxleDim=[(0,0),(10,20),(10,0)]
frontAxle=extrude(Polygon(*frontAxleDim,align=(Align.MIN,Align.MIN)),2)
frontAxle=fillet(frontAxle.edges().filter_by(Axis.Z)[1],2.6)\
    -Cylinder(1,6).transformed((0,0,0),(7.5,10,-1.5))
###Actual Front Axle and other turning thing###
actualAxle=Box(4,4,5,(Align.CENTER, Align.CENTER, Align.CENTER)).transformed((0,0,0,),(0,0,0))\
    +Box(8.5,4,3,align=(Align.MAX, Align.CENTER, Align.MAX)).transformed((0,0,0),(0,0,.5))\
    -Cylinder(1.2,10,align=(Align.MIN, Align.CENTER, Align.CENTER)).transformed((0,0,0),((-difference_between_farther_gears/2)+2.25,0,0))\
    +Cylinder(1,14).transformed((90,0,0),(0,-8,0))\
    -Cylinder(1.2,9).transformed((0,0,0),(0,0,0))
# actualAxle
    # +loft([Circle(1).transformed((0,0,0),((-difference_between_farther_gears/2)+3.25,0,4)),Circle(1).transformed((0,0,0),((-difference_between_farther_gears/2)+3.25,-3,7))])\    # +loft([Circle(.75).transformed((0,0,0),(0,0,4.5)),Circle(.75).transformed((0,0,0),(3,0,7.5))])\
    # +loft([Circle(.75).transformed((0,0,0),(0,0,-4.5)),Circle(.75).transformed((0,0,0),(3,0,-7.5))])\
#%% ###Rear Axel Attachment###
rAxle=Cylinder(1,90)
###Wheel###
hubCutout=Cylinder(20,5,arc_size=35,align=(Align.MIN,Align.MIN,Align.MIN))
wheel=Cylinder(25,5,align=(Align.CENTER,Align.CENTER,Align.MIN))
wheel=wheel-Cylinder(22,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0),(0,0,1))-copy.copy(hubCutout).transformed((0,0,0),(0,0,0))-copy.copy(hubCutout).transformed((0,0,90),(0,0,0))-copy.copy(hubCutout).transformed((0,0,180),(0,0,0))-copy.copy(hubCutout).transformed((0,0,270),(0,0,0))+Cylinder(2.5,5,align=(Align.CENTER,Align.CENTER,Align.MIN))+Box(2,22,5,align=(Align.CENTER,Align.MIN,Align.MIN))+Box(2,22,5,align=(Align.CENTER,Align.MIN,Align.MIN)).transformed((0,0,90),(0,0,0))+Box(2,22,5,align=(Align.CENTER,Align.MIN,Align.MIN)).transformed((0,0,180),(0,0,0))+Box(2,22,5,align=(Align.CENTER,Align.MIN,Align.MIN)).transformed((0,0,270),(0,0,0))-Cylinder(1,5,align=(Align.CENTER,Align.CENTER,Align.MIN))
###Connecting Cylinders###
rod=Cylinder(1.5,4.5,align=(Align.CENTER,Align.CENTER,Align.MAX))- Cylinder(.75,4.5,align=(Align.CENTER,Align.CENTER,Align.MAX))
botRod=Cylinder(1.5,3,align=(Align.CENTER,Align.CENTER,Align.MAX))+Cylinder(.749,4.5,align=(Align.CENTER,Align.CENTER,Align.MIN))
#%% ###Chassis Assembly###
turningRoom=turningConnector.scale(1.5)
chassis =Box(length=153, width=63, height=4.5, align=alignBox).transformed((180,0,0),(0,0,1.5))
chassis=fillet(chassis.edges().filter_by(Axis.Z),15)
bb=Box(length=150,width=60,height=3,align=alignBox).transformed((180,0,0),(0,0,0))
chassis=chassis-fillet(bb.edges().filter_by(Axis.Z),15)
chassis=chassis\
    - holes\
    + Cylinder(1, 9.5).transformed((0, 0, 0), (-40, 0, -3.5))\
    - Cylinder(1.25,4).transformed((0,0,0),(-40-difference_between_farther_gears,0, -4))\
    - turningRoom.transformed((0,0,0),(30.75,0,-6))\
    -rAxle.transformed((90,0,0),(rearBGearRadAtAngleX,2.5,rearBGearRadAtAngleY))\
    + Cylinder(1,10).transformed((0,0,0),(-40-difference_between_farther_gears,0, -4))\
    + copy.copy(rod).transformed((0,0,0),(0,27.5,0))\
    + copy.copy(rod).transformed((0,0,0),(0,-27.5,0))\
    + copy.copy(rod).transformed((0,0,0),(67,22.5,0))\
    + copy.copy(rod).transformed((0,0,0),(67,-22.5,0))\
    + copy.copy(rod).transformed((0,0,0),(-67,22.5,0))\
    + copy.copy(rod).transformed((0,0,0),(-67,-22.5,0))\
    + frontMotor.transformed((0, 0, 0), (-40, difference_between_closer_gears, -8))\
    + rMotorAssemb.transformed((0,0,0), (40,0,0))\
    + motorGear.transformed((0,0,0),(-40, difference_between_closer_gears, -4))\
    + Pos(-40, 0, -2) * ratioGear\
    + smallGear.transformed((0,0,0),(-40, 0, -4))\
    + turnGear.transformed((0, 0, 0), (-40-difference_between_farther_gears,0, -4))\
    +turningConnector.transformed((0,0,0),(0,0,-4))\
    +frontAxle.transformed((0,0,180),(-28-difference_between_farther_gears,-30,1.5))\
    +frontAxle.mirror(Plane.XZ).transformed((0,0,180),(-28-difference_between_farther_gears,30,1.5))\
    +actualAxle.transformed((0,0,0),(-35.5-difference_between_farther_gears,-40,-3))\
    +actualAxle.mirror(Plane.XZ).transformed((0,0,0),(-35.5-difference_between_farther_gears,40,-3))\
    +bMotorGear.transformed((90,0,0),(40,2.5,11.5))\
    +bWMotorGear.transformed((90,0,0),(rearBGearRadAtAngleX,2.5,rearBGearRadAtAngleY))\
    +rAxle.transformed((90,0,0),(rearBGearRadAtAngleX,0,rearBGearRadAtAngleY))\
    +copy.copy(wheel).transformed((90,0,0),(rearBGearRadAtAngleX,45,rearBGearRadAtAngleY))\
    +copy.copy(wheel).transformed((-90,0,0),(rearBGearRadAtAngleX,-45,rearBGearRadAtAngleY))\
    +copy.copy(wheel).transformed((90,0,0),(-35.5-difference_between_farther_gears,50,-3))\
    +copy.copy(wheel).transformed((-90,0,0),(-35.5-difference_between_farther_gears,-50,-3))

    # + boltM235.transformed((0,0,0), (52.5,-23,24.5))
chassis
#%%
bottomCover=Box(153,63,4.5,align=(Align.CENTER, Align.CENTER, Align.MAX)).transformed((0,0,0),(0,0,-3))
bottomCover=fillet(bottomCover.edges().filter_by(Axis.Z),15)
bbb=Box(150,60,3,align=(Align.CENTER, Align.CENTER, Align.MAX)).transformed((0,0,0),(0,0,-3))
bottomCover=bottomCover-fillet(bbb.edges().filter_by(Axis.Z),15)
bottomCover=(bottomCover-chassis-turningRoom.transformed((0,0,0),(30.75,0,-5)))\
    -Cylinder(bWg_Width+.1,2).transformed((90,0,0),(rearBGearRadAtAngleX,1.5,rearBGearRadAtAngleY))\
    + copy.copy(botRod).transformed((0,0,0),(0,27.5,-4))\
    + copy.copy(botRod).transformed((0,0,0),(0,-27.5,-4))\
    + copy.copy(botRod).transformed((0,0,0),(67,22.5,-4))\
    + copy.copy(botRod).transformed((0,0,0),(67,-22.5,-4))\
    + copy.copy(botRod).transformed((0,0,0),(-67,22.5,-4))\
    + copy.copy(botRod).transformed((0,0,0),(-67,-22.5,-4))\
    +frontAxle.transformed((0,0,180),(-28-difference_between_farther_gears,-30,-5.5))\
    +frontAxle.mirror(Plane.XZ).transformed((0,0,180),(-28-difference_between_farther_gears,30,-5.5))
bottomCover

# %%
# %%
beaten_spur_gear = SpurGear(module=1.0, teeth_number=20, width=50.0,
                            pressure_angle=20.0, bore_d=5.0,
                            missing_teeth=(0, 10))

wp = cq.Workplane('XY').gear(beaten_spur_gear)
wp
# %%
helical_gear = SpurGear(module=1.0, teeth_number=60, width=8.0,
                        pressure_angle=20.0, helix_angle=45.0,
                        bore_d=10.0, hub_d=16.0, hub_length=10.0,
                        recess_d=52.0, recess=3.0, n_spokes=5,
                        spoke_width=6.0, spoke_fillet=4.0,
                        spokes_id=23.0, spokes_od=48.0)
wp = cq.Workplane('XY').gear(helical_gear)
wp
# %%


spur_gear = SpurGear(module=1.0, teeth_number=13, width=5.0, bore_d=5.0)

wp = (cq.Workplane('XY')
      # Pushing an array of 4 points with spacing equal to the gear's pitch diameter
      .rarray(xSpacing=spur_gear.r0 * 2.0,
              ySpacing=1.0, xCount=4, yCount=1, center=False)
      # Create 4 meshing gears
      .gear(spur_gear)

      .moveTo(spur_gear.r0 * 2 * 4, 0.0)
      # Create an additional gear with the same profile but with different
      # bore diameter and hub
      .addGear(spur_gear, bore_d=3.0, hub_d=8.0, hub_length=4.0))
cq2b3d(wp)
# %%
