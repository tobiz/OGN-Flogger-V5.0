
from geopy import distance 
import sqlite3
##from .flogger_settings import *
from flogger_settings import *
from math import *

def release_height(cursor, tug_flight_no, glider_flight_no, settings):
	#
	# Compute the aero tow release height by using the tug and glider track points to find the 2D distance
	# and comparing this against the aero tow rope length. For any pair of coordinates if this distance is less
	# than the tow rope length then still on tow, test the next set in time sequence.  The track points will be 
	# reasonably close in time and are compare in time sequence so should be very similar.  When the first set of
	# coordinates are found where the separation distance is greater than the tow rope length then the altitude of
	# the tug at that point is the release height.
	#
	# It is more efficient to do this for each glider/tug coordinate set as received rather than processing all points
	# once received.  Also best to process each coordinate pair and once a spherical distance is found which is greater
	# than nxtow_rope length
	# then check say next  3 consecutive values and if all greater than defined value then assume first one of set
	# was the release point, hence glider altitude for those coordinates was the release height.
	
	# To correct any error from the 2D assumptions this can be converted to the 3D distance using:
	
	#Assume:
	#polar_point_1 = (long_1, lat_1, alt_1)
	#and
	#polar_point_2 = (long_2, lat_2, alt_2)
	
	#Translate each point to it's Cartesian equivalent by utilizing this formula:
	
	#x = alt * cos(lat) * sin(long)
	#y = alt * sin(lat)
	#z = alt * cos(lat) * cos(long)
	
	#and you will have p_1 = (tug_coord, y_glider, z_glider) and p_2 = (glider_coord, y_tug, z_tug) points respectively.
	
	#Finally use the Euclidean formula:
	
	#dist = sqrt((glider_coord-tug_coord)**2 + (y_tug-y_glider)**2 + (z_tug-z_glider)**2)
	#
	# Or
	# 
	#Once converted into Cartesian coordinates, you can compute the norm with numpy:
	#np.linalg.norm(point_1 - point_2)
	def distance_3D(glider_coord, tug_coord):
		#Translate each point to it's Cartesian equivalent by utilizing this formula:
		alt = 0
		lat = 1
		lng = 2
		x_glider = glider_coord[alt] * cos(glider_coord[lat]) * sin(glider_coord[lng])
		y_glider = glider_coord[alt] * sin(glider_coord[lat])
		z_glider = glider_coord[alt] * cos(glider_coord[lat]) * cos(glider_coord[lng])
		
		x_tug = tug_coord[alt] * cos(tug_coord[lat]) * sin(tug_coord[lng])
		y_tug = tug_coord[alt] * sin(tug_coord[lat])
		z_tug = tug_coord[alt] * cos(tug_coord[lat]) * cos(tug_coord[lng])
		
		return sqrt((x_tug - x_glider)**2 + (y_tug - y_glider)**2 + (z_tug - z_glider)**2)



	try:
		cursor.execute('''SELECT flight_no, timeStamp, longitude, latitude, altitude FROM trackFinal WHERE flight_no=? ORDER by timeStamp''', (tug_flight_no,))
		
	except:
		print("Failed to select tug tracks: ", tug_flight_no)
		return False
	tug_track = cursor.fetchall()
	
	try:
		cursor.execute('''SELECT flight_no, timeStamp, longitude, latitude FROM trackFinal WHERE flight_no=? ORDER by timeStamp''', (glider_flight_no,))
	except:
		print("Failed to select glider tracks: ", glider_flight_no)
	
	if tug_track == []:
		print("No tug track points returned")
		return False
	launch_height = 0
	i = 0
	for tug_point in tug_track: 
		tug_coords = (tug_point[3], tug_point[2])
		glider_point = cursor.fetchone()		# Fetches the next row of the SELECT
		glider_coords = (glider_point[3], glider_point[2])
		separation_2D = distance.distance(tug_coords, glider_coords).meters        # Geodesic distance, better Euclidian as small
		separation_3D = sqrt(separation_2D**2 + (tug_point[4] - glider_point[4])**2)
		separation = separation_3D
		print("Tug id: ", tug_flight_no, " Glider id: ", glider_flight_no, " Tug coords: ", tug_coords, " Glider coords: ", glider_coords, " Separation: ", separation) 
		if separation < 100: # Need to update GUI so this can be user defined, 150ft is ~46 metres
			i = i + 1
			continue
		else:
			# Found the first one in time sequence that has greater separation
			launch_height = tug_point[4]
			print("Launch height is: ", launch_height, " Number of compares is: ", i)
	return launch_height
				
				
				
			
			
	
