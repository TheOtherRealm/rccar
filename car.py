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
breadboard =import_step('64HalfsizeBreadboard.step')
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
#%% Front Motor Holder
mHolder=Cylinder(12,25,align=(Align.CENTER, Align.CENTER, Align.MIN)).transformed((0,0,0),(0,0,10))-makeMotor()\
    +(Box(30,12,25,align=(Align.CENTER, Align.CENTER, Align.MIN)).transformed((0,0,0),(0,0,10))\
    -Box(20,12,25,align=(Align.CENTER, Align.CENTER, Align.MIN)).transformed((0,0,0),(0,0,10)))\
    -Box(30,3,25,align=(Align.CENTER, Align.CENTER, Align.MIN)).transformed((0,0,0),(0,0,10))\
    +Box(10,5,5,align=(Align.CENTER, Align.CENTER, Align.MIN)).transformed((0,0,-45),(-10,10,10))\
    -Cylinder(1.2,12,align=(Align.CENTER, Align.CENTER, Align.CENTER)).transformed((90,0,0),(12.5,0,30))\
    -Cylinder(1.2,12,align=(Align.CENTER, Align.CENTER, Align.CENTER)).transformed((90,0,0),(-12.5,0,30))\
    -Cylinder(1.2,12,align=(Align.CENTER, Align.CENTER, Align.CENTER)).transformed((90,0,0),(12.5,0,20))\
    -Cylinder(1.2,12,align=(Align.CENTER, Align.CENTER, Align.CENTER)).transformed((90,0,0),(-12.5,0,20))\
    -Cylinder(1.2,12,align=(Align.CENTER,Align.CENTER, Align.MIN)).transformed((0,0,-45),(-11.5,11.5,10))
mHolder
mHolderHoll=Cylinder(1.2,4,align=(Align.CENTER,Align.CENTER, Align.MIN)).transformed((0,0,-45),(-11.5,11.5,6))
    # -Cylinder(1.2,12,align=(Align.CENTER, Align.CENTER, Align.MIN)).transformed((0,0,45),(11.5,11.5,10))\
    # +Box(10,5,5,align=(Align.CENTER, Align.CENTER, Align.MIN)).transformed((0,0,45),(10,10,10))\
#%% ### Bolts to hold the motor###
boltM1612 = SocketHeadCapScrew(size='M1.6-0.35', length=12,
                          fastener_type='iso4762', simple=False)
boltM1612 = cq2b3d(boltM1612)
# %% ## Gear Stuff##
### Larger gear for changing rotation speed###
ratioGear = SpurGear(module=.5, teeth_number=43, width=2, bore_d=1.8)
rg_pitchR = ratioGear.r0  # pitch radius
ratioGear = cq2b3d(ratioGear.build())
### Smaller Gear inside larger gear###
smallGear = SpurGear(module=.5, teeth_number=17,width=4, bore_d=1.8)
sg_pitchR=smallGear.r0
smallGear=cq2b3d(smallGear.build())
### Front Motor Gear###
motorGear = SpurGear(module=.5, teeth_number=13, width=4, bore_d=1.6)
mg_pitchR = motorGear.r0  # pitch radius
motorGear = cq2b3d(motorGear.build())
### Back Motor Gear###
bMotorGear = SpurGear(module=.5, teeth_number=67, width=4, bore_d=2.5)
bg_pitchR = bMotorGear.r0  # pitch radius
bMotorGear = cq2b3d(bMotorGear.build())
### Back Wheel Gear###
bWMotorGear = SpurGear(module=.5, teeth_number=13, width=4, bore_d=1.5)
bWg_pitchR = bWMotorGear.r0  # pitch radius
bWg_Width = bWMotorGear.ra
bWMotorGear = cq2b3d(bWMotorGear.build())
bWMotorGear
bMotorGear
difference_btwn_M_W_Gears=(bg_pitchR+bWg_pitchR)
rearBGearRadAtAngleX=70+difference_btwn_M_W_Gears*np.cos(np.deg2rad(-50))
rearBGearRadAtAngleY=11.5+difference_btwn_M_W_Gears*np.sin(np.deg2rad(-50))
# %% ### Gear connected to turning rod ###
turnGear=SpurGear(module=.5,teeth_number=61,width=4,bore_d=4,missing_teeth=(4,56))
tg_pitchR=turnGear.r0
difference_between_farther_gears=sg_pitchR+tg_pitchR
turnGear=cq2b3d(turnGear.build()).transformed((0,0,0),(0,0,0))
turnGear=Part()+turnGear-Cylinder(radius=tg_pitchR,height=8,arc_size=295
                                  ).transformed((0,0,32),(0,0,0))\
    +Box(length=5.5+tg_pitchR/2,width=6,height=4,align=(Align.MAX,Align.CENTER, Align.MIN)).transformed((0,0,0),(difference_between_farther_gears/2,0, 0))\
    - Box(length=4.5,width=2.5,height=8,align=(Align.MAX, Align.CENTER, Align.MIN)).transformed((0,0,0),((difference_between_farther_gears/2)-2,0, 0))\
    -Cylinder(1.2,4).transformed((0,0,0),(0,0, 0))
turnGear
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
holes = [
         Cylinder(1.2, 4).transformed(
             (0, 0, 0), (-70, difference_between_closer_gears, 0)),
         Cylinder(1.2,40).transformed((0,0,0), (82.5,-23,1.5)),
         Cylinder(1.2,40).transformed((0,0,0), (57.5,-23,1.5)),
         Cylinder(1.2,40).transformed((0,0,0), (82.5,-10,1.5)),
         Cylinder(1.2,40).transformed((0,0,0), (57.5,-10,1.5))]
# Cylinder(1.2, 4).transformed((0, 0, 0), (0, -20, 0)),
#          Cylinder(1.2, 4).transformed((0, 0, 0), (0, 20, 0)),
#          Cylinder(1.2, 4).transformed((0, 0, 0), (-70,0,  0)),
#          Cylinder(1.2, 4).transformed((0, 0, 0), (70,0,  0)),
alignBox = (Align.CENTER, Align.CENTER, Align.MIN)
# %% ###Turning Rod###
turningConnectorDim=[(4,43),(0,43),(0,20),(8,10),(8,-10),(0,-20),(0,-43),(4,-43),(4,-20),(12,-10),(12,10),(4,20)]
rubberBandHolderDim=[(0,0,0),(0,0,-2),(0,2,-2),(0,3,0)]
rubberBandHolder=extrude(Polygon(*rubberBandHolderDim),4)
turningConnector=extrude(Polygon(*turningConnectorDim),4
                         ).transformed((0,0,0),(-68-difference_between_farther_gears,0, 0))\
    -Box(10,15,4,align=(Align.MIN, Align.CENTER, Align.CENTER)).transformed((0,0,0),(-66-difference_between_farther_gears,0, 0))\
    -Box(4,7,1.5,align=(Align.MAX, Align.MAX, Align.MIN)).transformed((0,0,0),(-70-difference_between_farther_gears,43, 0))\
    -Box(4,7,1.5,align=(Align.MAX, Align.MIN, Align.MIN)).transformed((0,0,0),(-70-difference_between_farther_gears,-43, 0))\
    -Cylinder(1.2,8).transformed((0,0,0),(-72-difference_between_farther_gears,40, 0))\
    -Cylinder(1.2,8).transformed((0,0,0),(-72-difference_between_farther_gears,-40, 0))\
    -rubberBandHolder.mirror(Plane.XZ).transformed((0,0,0),(-74-difference_between_farther_gears,28, 2))\
    -rubberBandHolder.transformed((0,0,0),(-74-difference_between_farther_gears,-28,2))
turningRoom=turningConnector.scale(1.5)
turningConnector=turningConnector+Cylinder(1,2,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0),(-64-difference_between_farther_gears,0, 0))
turningConnector
#%% ###The Rear Motor Assembly###
rMotorAssemb=Box(30,4,23,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (0,-10,1.5))\
    + Box(30,4,23,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (0,-23,1.5))\
    -Cylinder(1.2,40,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (12.5,-23,1.5))\
    -Cylinder(1.2,40,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (-12.5,-23,1.5))\
    -Cylinder(1.2,40,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (12.5,-10,1.5))\
    -Cylinder(1.2,40,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0), (-12.5,-10,1.5))\
    - rearMotor.transformed((90,0,0),(0,10,11.5))\
    -Box(30,40,12.5,align=(Align.CENTER,Align.CENTER,Align.MAX)).transformed((0,0,0),(0,-22,11.5))\
    + rearMotor.transformed((90,0,0),(0,10,11.5))
#%% ###Front Axle Attachment###
frontAxleDim=[(0,0),(10,25),(10,0)]
frontAxle=extrude(Polygon(*frontAxleDim,align=(Align.MIN,Align.MIN)),2)
frontAxle=fillet(frontAxle.edges().filter_by(Axis.Z)[1],2.6)\
    -Cylinder(1.2,6).transformed((0,0,0),(7.5,10,-1.5))
# frontAxle
###Actual Front Axle and other turning thing###
actualAxle=Box(4,4,11,align=(Align.CENTER, Align.CENTER, Align.CENTER)).transformed((0,0,0,),(0,0,-2))\
    +Box(8.5,4,3,align=(Align.MAX, Align.CENTER, Align.CENTER)).transformed((0,0,0),(0,0,0))\
    -Cylinder(1.2,10,align=(Align.MIN, Align.CENTER, Align.CENTER)).transformed((0,0,0),((-difference_between_farther_gears/2)+2.25,0,0))\
    +Cylinder(2,10,align=(Align.MIN, Align.MIN, Align.CENTER)).transformed((90,0,0),(-2,-7,-2))\
    -Cylinder(1.2,20).transformed((0,0,0),(0,0,0))
actualAxle
# actualAxle
    # +loft([Circle(1).transformed((0,0,0),((-difference_between_farther_gears/2)+3.25,0,4)),Circle(1).transformed((0,0,0),((-difference_between_farther_gears/2)+3.25,-3,7))])\    # +loft([Circle(.75).transformed((0,0,0),(0,0,4.5)),Circle(.75).transformed((0,0,0),(3,0,7.5))])\
    # +loft([Circle(.75).transformed((0,0,0),(0,0,-4.5)),Circle(.75).transformed((0,0,0),(3,0,-7.5))])\
#%% ###Rear Axel Attachment###
rAxle=Cylinder(1.4,90)
yHeight=np.abs(rearBGearRadAtAngleY*2-1.5)
yHeight
rAxSupport=Box(13,yHeight,5).transformed((90,0,0),(rearBGearRadAtAngleX,0,rearBGearRadAtAngleY))-Cylinder(1.6,8).transformed((90,0,0),(rearBGearRadAtAngleX,0,rearBGearRadAtAngleY))
rAxSupport=rAxSupport-Cylinder(1.2,18).transformed((0,0,0),(rearBGearRadAtAngleX+4.5,0,rearBGearRadAtAngleY))-Cylinder(1.2,18).transformed((0,0,0),(rearBGearRadAtAngleX-4.5,0,rearBGearRadAtAngleY))
rAxSupportHoles=Cylinder(1.2,12).transformed((0,0,0),(rearBGearRadAtAngleX+4.5,0,rearBGearRadAtAngleY))+Cylinder(1.2,12).transformed((0,0,0),(rearBGearRadAtAngleX-4.5,0,rearBGearRadAtAngleY))
rAxSupport
#%%
###Wheel###
hubCutout=Cylinder(20,5,arc_size=35,align=(Align.MIN,Align.MIN,Align.MIN))
wheel=Cylinder(25,5,align=(Align.CENTER,Align.CENTER,Align.MIN))
wheel=wheel\
    -Cylinder(22,4,align=(Align.CENTER,Align.CENTER,Align.MIN)).transformed((0,0,0),(0,0,1))\
    -copy.copy(hubCutout).transformed((0,0,0),(0,0,0))\
    -copy.copy(hubCutout).transformed((0,0,90),(0,0,0))\
    -copy.copy(hubCutout).transformed((0,0,180),(0,0,0))\
    -copy.copy(hubCutout).transformed((0,0,270),(0,0,0))\
    +Cylinder(2.5,5,align=(Align.CENTER,Align.CENTER,Align.MIN))\
    +Box(2,22,5,align=(Align.CENTER,Align.MIN,Align.MIN))\
    +Box(2,22,5,align=(Align.CENTER,Align.MIN,Align.MIN)).transformed((0,0,90),(0,0,0))\
    +Box(2,22,5,align=(Align.CENTER,Align.MIN,Align.MIN)).transformed((0,0,180),(0,0,0))\
    +Box(2,22,5,align=(Align.CENTER,Align.MIN,Align.MIN)).transformed((0,0,270),(0,0,0))
frontWheel=wheel+Cylinder(3,5,align=(Align.CENTER,Align.CENTER,Align.MIN))\
    -Cylinder(2.2,5,align=(Align.CENTER,Align.CENTER,Align.MIN))
backWheel=wheel+Cylinder(3,5,align=(Align.CENTER,Align.CENTER,Align.MIN))\
    -Cylinder(1.2,5,align=(Align.CENTER,Align.CENTER,Align.MIN))
# ###Connecting Cylinders###
# rod=Cylinder(2,4.5,align=(Align.CENTER,Align.CENTER,Align.MAX))- Cylinder(1.5,5,align=(Align.CENTER,Align.CENTER,Align.MAX))
# botRod=Cylinder(1.5,2,align=(Align.CENTER,Align.CENTER,Align.MAX))+Cylinder(1,4,align=(Align.CENTER,Align.CENTER,Align.MIN))
#%% ###Chassis Assembly###
chassis =Box(length=218, width=63, height=7.5, align=alignBox).transformed((180,0,0),(0,0,1.5))
chassis=fillet(chassis.edges().filter_by(Axis.Z),15)
bb=Box(length=215,width=60,height=6,align=alignBox).transformed((180,0,0),(0,0,0))
chassis=chassis-fillet(bb.edges().filter_by(Axis.Z),15)
chassis=chassis\
    - holes\
    - Cylinder(1.2, 20).transformed((0, 0, 0), (-70, 0, -6.5))\
    - Cylinder(1.25,20).transformed((0,0,0),(-70-difference_between_farther_gears,0, -7))\
    - turningRoom.transformed((0,0,0),(45.75,0,-6))\
    -rAxle.transformed((90,0,0),(rearBGearRadAtAngleX,2.5,rearBGearRadAtAngleY))\
    - Cylinder(1.2,20).transformed((0,0,0),(-70-difference_between_farther_gears,0, -7))\
    -rAxSupportHoles.transformed((0,0,0),(0,16.5,0))\
    -rAxSupportHoles.transformed((0,0,0),(0,-16.5,0))\
    -Box(35,6,10).transformed((0,0,0), (rearBGearRadAtAngleX,2,1.5))\
    + extrude(Plane(chassis.faces().sort_by(Axis.Z)[0])*Rot(x=0,z=90)*Text("UMass",font_size=12,align=(Align.CENTER,Align.CENTER,Align.MIN)),.3).transformed((0,0,0),(-15,0,3))\
    + extrude(Plane(chassis.faces().sort_by(Axis.Z)[0])*Rot(x=0,z=90)*Text("SENGI",font_size=10,align=(Align.CENTER,Align.CENTER,Align.MIN)),.3).transformed((0,0,0),(-5,0,3))\
    + extrude(Plane(chassis.faces().sort_by(Axis.Z)[0])*Rot(x=0,z=90)*Text("2023",font_size=10,align=(Align.CENTER,Align.CENTER,Align.MIN)),.6).transformed((0,0,0),(5,0,3))\
    +frontAxle.transformed((0,0,180),(-58-difference_between_farther_gears,-30,1.5))\
    +frontAxle.mirror(Plane.XZ).transformed((0,0,180),(-58-difference_between_farther_gears,30,1.5))\
    - mHolderHoll.transformed((0, 0, -90), (-70, difference_between_closer_gears, -8))\
    # + mHolder.transformed((0, 0, -90), (-70, difference_between_closer_gears, -8))\
    # + frontMotor.transformed((0, 0, 0), (-70, difference_between_closer_gears, -8))\
    # + rMotorAssemb.transformed((0,0,0), (70,0,0))\
    # + motorGear.transformed((0,0,0),(-70, difference_between_closer_gears, -4))\
    # + ratioGear.transformed((0,0,0),(-70, 0, -2))\
    # + smallGear.transformed((0,0,0),(-70, 0, -6))\
    # + turnGear.transformed((0, 0, 0), (-70-difference_between_farther_gears,0, -6))\
    # +turningConnector.transformed((0,0,0),(0,0,-4))\
    # +actualAxle.transformed((0,0,0),(-65.5-difference_between_farther_gears,-40,-3))\
    # +actualAxle.mirror(Plane.XZ).transformed((0,0,0),(-65.5-difference_between_farther_gears,40,-3))\
    # +bWMotorGear.transformed((90,0,0),(70,4,11.5))\
    # +bMotorGear.transformed((90,0,0),(rearBGearRadAtAngleX,4,rearBGearRadAtAngleY))\
    # +rAxle.transformed((90,0,0),(rearBGearRadAtAngleX,0,rearBGearRadAtAngleY))\
    # +rAxSupport.transformed((0,0,0),(0,16.5,0))\
    # +rAxSupport.transformed((0,0,0),(0,-16.5,0))\
    # +copy.copy(backWheel).transformed((90,0,0),(rearBGearRadAtAngleX,45,rearBGearRadAtAngleY))\
    # +copy.copy(backWheel).transformed((-90,0,0),(rearBGearRadAtAngleX,-45,rearBGearRadAtAngleY))\
    # +copy.copy(frontWheel).transformed((90,0,0),(-65.5-difference_between_farther_gears,50,-3))\
    # +copy.copy(frontWheel).transformed((-90,0,0),(-65.5-difference_between_farther_gears,-50,-3))
chassis
#     # + boltM235.transformed((0,0,0), (52.5,-23,24.5))
bWMotorGear.export_stl('bWMGear2023-06-26-1521.stl')
# rMotorAssemb.export_stl('rMotorAssemb2023-06-07-1405.stl')
# motorGear.export_stl('motorGear2023-06-26-1521.stl')
# (ratioGear.transformed((0,0,0),(0, 0, -2))+smallGear.transformed((0,0,0),(0, 0, -6))).export_stl('ratioGear2023-06-26-1521.stl')
# turnGear.export_stl('turningGear2023-06-26-1521.stl')
# turningConnector.export_stl('turningConnector2023-06-26-1521.stl')
# axel1=actualAxle
# axle2=actualAxle.mirror(Plane.XZ)
# axel1.export_stl('axle1_2023-06-26-1521.stl')
# axle2.export_stl('axle2_2023-06-26-1521.stl')
bMotorGear.export_stl('bMotorGear2023-06-26-1521.stl')
bWMotorGear.export_stl('bWMGear2023-06-26-1521.stl')
# frontWheel.export_stl('frontWheel2023-06-26-1521.stl')
backWheel.export_stl('backWheel2023-06-26-1521.stl')
# mHolder.export_stl('mHolder2023-06-26-1521.stl')
chassis.export_stl('chassis2023-06-26-1521.stl')
# rAxSupport.export_stl('chassis2023-06-26-1521.stl')
    # + copy.copy(rod).transformed((0,0,0),(0,27.5,0))\
    # + copy.copy(rod).transformed((0,0,0),(0,-27.5,0))\
    # + copy.copy(rod).transformed((0,0,0),(67,22.5,0))\
    # + copy.copy(rod).transformed((0,0,0),(67,-22.5,0))\
    # + copy.copy(rod).transformed((0,0,0),(-67,22.5,0))\
    # + copy.copy(rod).transformed((0,0,0),(-67,-22.5,0))\
#%%
bottomCover=Box(153,63,6.5,align=(Align.CENTER, Align.CENTER, Align.MAX)).transformed((0,0,0),(0,0,-6))
bottomCover=fillet(bottomCover.edges().filter_by(Axis.Z),15)
bbb=Box(150,60,5,align=(Align.CENTER, Align.CENTER, Align.MAX)).transformed((0,0,0),(0,0,-6))
bottomCover=bottomCover-fillet(bbb.edges().filter_by(Axis.Z),15)
bottomCover=(bottomCover-chassis-turningRoom.transformed((0,0,0),(30.75,0,-5)))\
    -Cylinder(1.2, 50).transformed((0, 0, 0), (0, -20, 0))\
    -Cylinder(1.2, 50).transformed((0, 0, 0), (0, 20, 0))\
    -Cylinder(1.2, 50).transformed((0, 0, 0), (-70,0,  0))\
    -Cylinder(1.2, 50).transformed((0, 0, 0), (70,0,  0))\
    -Cylinder(bWg_Width+.1,2).transformed((90,0,0),(rearBGearRadAtAngleX,1.5,rearBGearRadAtAngleY))\
    +frontAxle.transformed((0,0,180),(-28-difference_between_farther_gears,-30,-10.5))\
    +frontAxle.mirror(Plane.XZ).transformed((0,0,180),(-28-difference_between_farther_gears,30,-10.5))
# bottomCover.export_stl('bottomCover2023-06-26-1521.stl')
    # + copy.copy(botRod).transformed((0,0,0),(0,27.5,-4))\
    # + copy.copy(botRod).transformed((0,0,0),(0,-27.5,-4))\
    # + copy.copy(botRod).transformed((0,0,0),(67,22.5,-4))\
    # + copy.copy(botRod).transformed((0,0,0),(67,-22.5,-4))\
    # + copy.copy(botRod).transformed((0,0,0),(-67,22.5,-4))\
    # + copy.copy(botRod).transformed((0,0,0),(-67,-22.5,-4))\
bottomCover
#%% ### Export the entire car to look at it in another cad file###
car=chassis+bottomCover
car
# car.export_step('car2023-06-26-1521.step')


# %%
(.5**2*np.pi)*100
# %%
