
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from matplotlib.patches import Wedge, Polygon
from matplotlib.collections import PatchCollection
import gpxpy 
import mplleaflet

from .flogger_tasks import tasks

def draw_tp(figure, type, centre, theta1, radius):
    # figure:    the existing figure the turning point is to be added to
    # type:      the type of turning point, FAI sector, BGA Start Line, BGA Finish Cylinder
    # centre:    the centre coordinates of the turning point
    # theta1:    the lowest value in degrees of the first line of the TP, theta2 is clockwise from theta1, angle depends on type
    # radius:    size from centre to extremity of symbol type
    
    #fig1 = plt.figure()
    #ax1 = figure.add_subplot(111, aspect='equal')
    #ax1.add_patch(
    #figure.add_patch(
    #figure.add_patch(
    print("Draw: ", type)
    '''
    wedge = Wedge(
        #(0, 0),         # (x,y)
        #(1, 1),         # (x,y)
        #centre,          # (x,y)
        #200,            # radius
        #60,             # theta1 (in degrees)
        #120,            # theta2
        #color="g", alpha=0.2
        
        
        centre,         # (x,y)
        radius,         # radius
        theta1,         # theta1 (in degrees)
        theta1 + 90,    # theta2
        color="g", alpha=0.2
    )
    '''
    #
    wedge = Wedge(
        (0, 0),         # (x,y)
        200,            # radius
        60,             # theta1 (in degrees)
        120,            # theta2
        color="g", alpha=0.2)
    figure.append(wedge)
    
    #plt.plot(lon, lat, color = 'yellow', lw = 1.0, alpha = 0.8)
    
    #plt.show()

#
# Test of sector displays
# 

print("Start Test")                
task = tasks("https://www.navboys.com/user/UK2019MAR.zip") 
task.make_subset_tp_list([["SU2", "S"],["NRT", "F"],["HAN", "F"],["SOF", "F"],["SU2", "E"] ])

print("End Test")
track_file = "/home/pjr/Development/tracks/2019-08-24_flight71_track_ds2.gpx"    
gpx_file = open(track_file, 'r')
gpx = gpxpy.parse(gpx_file)       
lat = []
lon = []   
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            lat.append(point.latitude)
            lon.append(point.longitude)
 
'''
Test Wedge code
'''
import numpy as np
import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)


fig, ax = plt.subplots()

resolution = 50  # the number of vertices
N = 3
x = np.random.rand(N)
y = np.random.rand(N)
radii = 0.1*np.random.rand(N)
patches = []
#for x1, y1, r in zip(x, y, radii):
#    circle = Circle((x1, y1), r)
#    patches.append(circle)

#x = np.random.rand(N)
#y = np.random.rand(N)
#radii = 0.1*np.random.rand(N)
#theta1 = 360.0*np.random.rand(N)
#theta2 = 360.0*np.random.rand(N)
#for x1, y1, r, t1, t2 in zip(x, y, radii, theta1, theta2):
#    wedge = Wedge((x1, y1), r, t1, t2)
    #patches.append(wedge)
    
wedge1 = Wedge(
        (0.5, 0.5),         # (x,y)
        .5,            # radius
        60,             # theta1 (in degrees)
        120,            # theta2
        color="g", alpha=0.2)
patches.append(wedge1)

# Some limiting conditions on Wedge
#patches += [
#    Wedge((.3, .7), .1, 0, 360),             # Full circle
#    Wedge((.7, .8), .2, 0, 360, width=0.05),  # Full ring
#    Wedge((.8, .3), .2, 0, 45),              # Full sector
#    Wedge((.8, .3), .2, 45, 90, width=0.10),  # Ring sector
#]

#for i in range(N):
#    polygon = Polygon(np.random.rand(N, 2), True)
#    patches.append(polygon)

colors = 100*np.random.rand(len(patches))
p = PatchCollection(patches, alpha=0.4)
p.set_array(np.array(colors))
ax.add_collection(p)
#fig.colorbar(p, ax=ax)

plt.show()            

exit()
'''
Test Wedge code end
'''            
            
#
# Wedge test
#            
#fig1 = plt.figure()
#ax1 = fig1.add_subplot(111, aspect='equal')
#ax1.add_patch(
#    patches.Wedge(
#        (0, 0),         # (x,y)
#        200,            # radius
#        60,             # theta1 (in degrees)
#        120,            # theta2
#        color="g", alpha=0.2
#    )
#)

#plt.axis([-150, 150, 0, 250])

#plt.show()
#exit()
#fig1 = plt.figure()
#fig, ax = plt.subplots()
patches = []
pos =  (task.subset_tp_list[0][2], task.subset_tp_list[0][3])
draw_tp(patches, "FAI_Sector", pos, 1, task.subset_tp_list[0][6])
#fig1 = plt.figure(facecolor = '0.05')
fig1 = plt.figure(facecolor = 'w')
ax = plt.Axes(fig1, [0., 0., 1., 1.], )
#ax.set_aspect('equal')
#ax.set_axis_off()
#print "TP-1: ", task.subset_tp_list
print("TP-1. Lat: ", task.subset_tp_list[0][2], " Lng: ", task.subset_tp_list[0][3])
#pos = (0,0)
#pos =  (task.subset_tp_list[0][2], task.subset_tp_list[0][3])
#draw_tp(patches, pos, )
print("Plot track")
#track = plt.plot(lon, lat, color = 'black', lw = 1.0, alpha = 0.8)
#patches.append(track)
plt.show()
#mplleaflet.show()
print("Exit")
exit()
#
# Wedge test end
#

#
# Working plot start
#
fig = plt.figure(facecolor = '0.05')
fig = plt.figure(facecolor = 'w')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()


plt.plot(lon, lat, color = 'black', lw = 1.0, alpha = 0.8)
try:
    mplleaflet.show()
except :
    print("Display track failed")
    