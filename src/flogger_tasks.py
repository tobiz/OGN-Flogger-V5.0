import urllib.request, urllib.error, urllib.parse
import zipfile
import csv
import tempfile
import re
#import mpu
import geopy.distance
import math
from wx.lib.agw.aui.aui_constants import pin_bits
from geopy import distance
import sqlite3

class tasks():
	#
	# .cup file format from https://www.navboys.com/user/UK2019MAR.zip is:
	# Title,Code,Country,Latitude,Longitude,Elevation,Style,Direction,Length,Frequency,Description
	#	
	# .cup file format from http://www.newportpeace.co.uk/software/vrp-cup.cup is:
	# name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc,userdata,pics
	# Note NOT SUPPORTED
	#
	#
	tp_list = []
	subset_tp_list = []
	
	def get_type(self, name):
		x = name.split(".cup")
		'''
		with open('employee_file.csv', mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    employee_writer.writerow(['John Smith', 'Accounting', 'November'])
    employee_writer.writerow(['Erica Meyers', 'IT', 'March'])
		'''
		print(x)
		try:
			if x[1] == "":
				print("Cup file")
				tpfile = urllib.request.urlopen(name)		# Get the url
				fs = tpfile.read()
				#print "URL file as string: ", fs					# Get for reading
				f = tempfile.NamedTemporaryFile(suffix=".cup")
				print("Temp file: ", f.name)
				x = 0
				for r in fs:						# Write url file to temp
					x = x + 1
					f.write(r)
					#print "URL char: ", x, " is: ", r
				try:
					x = 0
					with open(f.name, 'rb') as csvfile:
						for line in csvfile:
							x = x + 1
							#print "line: ", x, " is: ", line
						#x = x + 1
						#data = csv.reader(csvfile)
						#print "line: ", x, " is: ", data
					print("tmp file opened")
				except:
					print("Failed to open tmp file")
				csvfile.close()
				return "cup", f.name
		except:
			try:
				x = name.split(".zip")
				print(x)
				if x[1] == "":
					print("Zip file")
					#
					# Read http zip file it into temp file, not a real file
					# 
					urlzf = urllib.request.urlopen(name)
					zfs = urlzf.read()	
					f = tempfile.TemporaryFile()
					for r in zfs:
						f.write(r)
					zf = zipfile.ZipFile(f)
					for fn in zf.namelist():
						if fn.endswith('.cup'):
							print(fn)	
							zf.extract(fn)
							f.close()
							return "zip", fn
				else:
					print("Can't handle it, exit")
					return False
			except:
				return False
			
	
	
	
	def __init__(self, turning_point_source):
		#tp_list = []
		print("Init task class")
			
		res = self.get_type(turning_point_source) # Import and convert turning points db into usable form
		fn = res[1]
		print("csv file is: ", fn)	
		with open(fn, 'rb') as csvfile:
			data = csv.reader(csvfile)
			j = 0	
			for row in data:
				# Ignore first and last rows
				if j == 0 or len(row) <= 2:
					j = 1
					continue
				#print "Row orig: ", row
				row[3] = row[3].replace(" ", "")	# Remove spaces from lat
				row[4] = row[4].replace(" ", "")	# Remove spaces from lng
				lat = re.split("[A-Z]", row[3])		# Get number part
				latL = re.split("[0-9]+", row[3])	# Get single letter part
				lng = re.split("[A-Z]", row[4])		# Repeat for longitude
				lngL = re.split("[0-9]+", row[4])
				#print "Type: ", type(latL)
				#print "Lat/Lng: ", " Length row: ", len(row), " ", row[3], " ,", row[4]
				#print "Latitude: ", lat[0], " Letter: ", latL[2]
				#print "Longitude: ", lng[0], " Letter: ", lngL[2]
				lat_deg = lat[0][0:2]				# Get 2xdecimal degree digits
				lat_min = lat[0][2:]				# Get remainder, minutes
				lng_deg = lng[0][0:3]				# Get 3xdecimal degree digits
				lng_min = lng[0][3:]				# Get remainder, minutes
				#print "Lat Deg: ", lat_deg, " Lat Min: ", lat_min, " lat_min.deg", str(float(lat_min)/60)
				#print "Lng Deg: ", lng_deg, " Lng Min: ", lng_min
				
				lat_final = float(lat_deg) + float(lat_min)/60		# Convert to decimal degrees
				lng_final = float(lng_deg) + float(lng_min)/60		# Convert to decimal degrees
				#print "Lat Final: ", lat_final, " Lng Final: ", lng_final
				
				# Convert NSEW letter to +/-, W|S = -ve, N|E = +ve
				if latL[2] == "S":
					row[3] = -lat_final
				else:
					row[3] = lat_final
				if lngL[2] == "W":
					row[4] = -lng_final
				else:
					row[4] = lng_final
				#print "Row new: ", row
				tasks.tp_list.append(row)
				#if not row[0].find("Sutton Bank"):
				#	print row
					#exit()
				
			#print tp_list
			#f.close()
	
	def compass_bearing(self, pointA, pointB):
		"""
	    Converts GPS latitude, longitude to polar coordinates
	    """

		#print "Point A; ", pointA, " Point B", pointB
		if (type(pointA) != tuple) or (type(pointB) != tuple):
			raise TypeError("Only tuples are supported as arguments")
	
		lat1 = math.radians(pointA[0])
		lat2 = math.radians(pointB[0])
	
		diffLong = math.radians(pointB[1] - pointA[1])
	
		x = math.sin(diffLong) * math.cos(lat2)
		y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))
	
		initial_bearing = math.atan2(x, y)
	
		
		initial_bearing = math.degrees(initial_bearing)
		compass_bearing = (initial_bearing + 360) % 360
		return compass_bearing
		
	def show_tp_list(self):
		return tasks.tp_list
	
	def show_subset_tp_list(self):
		return tasks.subset_tp_list
					
	def make_subset_tp_list(self, tp_sub_codes):
		#
		# Produces a subset of the main turning point list of the tp's
		# with 'codes' in tp_list
		#
		# Track points TP[] has format:
		# TP[0] = Title
		# TP[1] = Code
		# TP[2] = Latitude
		# TP[3] = Longitude
		# TP[4] = Turning point type code: S, F, B, E
		# TP[5] = Track Bearing In 						# Blank if no Bearing in
		# TP[6] = Heading Bearing Out 					# Blank if no Bearing out
		# TP[7] = Track/Heading Bearing In/Out Bisector Bearing # Blank if no Bisector Bearing, ie either no Bearing in or no Bearing out
		# TP[8] = FAI segment bearing 1					# Lowest bearing clockwise
		# TP[9] = FAI segment bearing 2					# Highest bearing clockwise
		# 
		# The task turning point have the format of a list of lists.
		# Each item in the list has the format [3-letter, type] 
		# where type denotes the type of turning point:
		# S: Start, F: FAI Sector, B: Barrel, L: Line, E: End
		# 
		#print "List1: ", tp_sub_codes[0][0], "List2: ", tp_sub_codes[0][1]
		#print 	enumerate(task.tp_list[:-1]		
		for i, j in enumerate(tp_sub_codes):
			#print "Item: ", i, " :", j
			#for k in task.tp_list:
			for k in tasks.tp_list:
				#print "Next compare: ", j, " -: ", k[1]
				#exit()
				if j[0] == k[1]:
					#print j
					#print "Item: ", i, " is :", j
					#print "Task item: ", k
					tasks.subset_tp_list.append([k[0], k[1], k[3], k[4], j[1]])
		# Just for testing Start
		#for i, j in enumerate(tasks.subset_tp_list):
		#print "Task list: ", tasks.subset_tp_list
		#	print "Task list TP", i, " :", j
		# Just for testing End
		
		print("Compute tracks in/out")
		for i, j in enumerate(tasks.subset_tp_list):
			#print "Length sublist: ", len(tasks.subset_tp_list)
			print("i: ", i)
			if i < len(tasks.subset_tp_list) + 1 :
				tasks.subset_tp_list[i].append("") 	# Add for TP[5], Track Bearing In
				tasks.subset_tp_list[i].append("") 	# Add for TP[6], Heading Bearing Out
				tasks.subset_tp_list[i].append("") 	# Add for TP[7], Track/Heading Bearing In/Out Bisector
				tasks.subset_tp_list[i].append("") 	# Add for TP[8], FAI segment bearing 1	
				tasks.subset_tp_list[i].append("") 	# Add for TP[9], FAI segment bearing 2
				#print "Now: ", i, " List: ", tasks.subset_tp_list[i]
				#if tasks.subset_tp_list[i][4] == "S" or tasks.subset_tp_list[i][4] == "E":
				if tasks.subset_tp_list[i][4] == "S" :
					print("Type Start: ", tasks.subset_tp_list[i][4], end=' ') 
						
					#print "Skip"	
					continue		# Out Bearing
				
				if i%2 != 0 :	# i is odd if 1
				#if i%2 <> i%2 :	# i is odd if 1
					# i is odd
					p1 = tasks.subset_tp_list[i-1][2], tasks.subset_tp_list[i-1][3]
					p2 = j[2], j[3]
					print("Point(odd): ", i, " Code: ", tasks.subset_tp_list[i-1][1], " Lat: ", p1[0],  " Lng: ", p1[1], "To point: ", j[1],  " Lat: ", p2[0], " Lng: ", p2[1])

					track = self.compass_bearing(p1, p2) 	
					tasks.subset_tp_list[i][5] = track			# In Bearing
					tasks.subset_tp_list[i-1][6] = track		# Out Bearing
					#print "Point Bearings(odd): ", j[1], " is:", task.subset_tp_list[i]
				
				else:
					# i is even
					p1 = tasks.subset_tp_list[i-1][2], tasks.subset_tp_list[i-1][3]	
					p2 = j[2], j[3]
					print("Point(even): ", i, " Code: ", tasks.subset_tp_list[i][1], " Lat: ", p1[0],  " Lng: ", p1[1], " To point: ", j[1], " Lat: ", p2[0], " Lng: ", p2[1])

					track = self.compass_bearing(p1, p2)
					tasks.subset_tp_list[i][5]= track			# In Bearing
					tasks.subset_tp_list[i-1][6] = track		# Out Bearing
					#print "Point Bearingss(even): ", j[1], " is:", task.subset_tp_list[i]
				
		
		for i, tp in enumerate(tasks.subset_tp_list):
			print()
			#print "Turning Point: ", i, " is:", tp	
			
		#
		# Compute mid point bearing
		#
		for i, tp in enumerate(tasks.subset_tp_list):	
			#print "Bearings", i, " :", tp
			
			if tp[4] == "S":
				print("tp: ", tp[6])
				fai_vector = (int(tp[6]) + 180) % 360					# 180 of bearing out, ie tp[6]
				fai_vector1 = (fai_vector - 45) % 360
				fai_vector2 = (fai_vector + 45) % 360
				vectors = [fai_vector1, fai_vector2]
				vectors.sort()
								
				tasks.subset_tp_list[i][8] = vectors[0]		# Low bearing
				tasks.subset_tp_list[i][9] = vectors[1]		# High bearing
				#print "Final Turning Point: ", i, " Code: ", tasks.subset_tp_list[i][1], " Heading out: ", tp[6], " FAI vector: ", fai_vector, " Vector1: ", fai_vector1, "Vector2: ", fai_vector2

			if tp[4] == "E":
				fai_vector = (tp[5] + 180) % 360					# 180 of bearing in, ie tp[5]
				fai_vector1 = (fai_vector - 45) % 360
				fai_vector2 = (fai_vector + 45) % 360
				vectors = [fai_vector1, fai_vector2]
				vectors.sort()				
				tasks.subset_tp_list[i][8] = vectors[0]		# Low bearing
				tasks.subset_tp_list[i][9] = vectors[1]		# High bearing
				#print "Final Turning Point: ", i, " Code: ", tasks.subset_tp_list[i][1], " Track in: ", tp[5], " FAI vector: ", fai_vector, " Vector1: ", fai_vector1, "Vector2: ", fai_vector2
	
				
			#else:
			
			if tp[5] != "" and tp[6] != "":
				
				#pin = tp[4]
				#pout = tp[5]
				pin = tp[5]
				pout = tp[6]
								
				heading_in = pin
				track_in1 = (heading_in + 180) % 360
				bisector = math.fabs((track_in1 - pout)) / 2
				vectors1 = [track_in1, pout]
				vectors1.sort()
				track_in = vectors1[0]
				
				fai_vector = (track_in + 180 + bisector) % 360
				fai_vector1 = (fai_vector - 45) % 360
				fai_vector2 = (fai_vector + 45) % 360
				vectors = [fai_vector1, fai_vector2]
				vectors.sort()
								
				tasks.subset_tp_list[i][8] = vectors[0]		# Low bearing
				tasks.subset_tp_list[i][9] = vectors[1]		# High bearing
					
				#print "Final Turning Point: ", i, " Code: ", tasks.subset_tp_list[i][1], " Track in: ", track_in, " Heading out: ", pout, " Bisector: ", bisector, " FAI vector: ", fai_vector, " Vector1: ", fai_vector1, "Vector2: ", fai_vector2
				#print "Turning Point: %i, Code: %s, Track in: %i, Heading out: %i, Bisector: %i, FAI vector: %i, Vector1: %i, Vector2: %i" % (i, tasks.subset_tp_list[i][1], track_in1, pout, bisector, fai_vector, vectors[0], vectors[1])
		# Just for testing Start
		for i, j in enumerate(tasks.subset_tp_list):
		#print "Task list: ", tasks.subset_tp_list
			print("Final TP", i, " :", j)
		# Just for testing End		
		return
				
	#def check_point (self, radius, p1, p2, endAngle, startAngle):
	def check_point (self, radius, tp_nos, p2):
		def delta_angle(firstAngle, secondAngle): 
			#print "Type a1:", type(firstAngle), " Type a2: ", secondAngle, " secondAngle: ", secondAngle
			difference = (secondAngle) - (firstAngle)
			if (difference < -180):
				difference += 360
			if (difference > 180):
				difference -= 360
			return abs(difference)
		#print "check_point P1: ", [tp_nos[1], tp_nos[2], tp_nos[3]], " P2: ", p2
		#
		# tp_nos is the number of the turning point in the turning point list to be checked against.
		# This gives the centre of the turning point as a tuple, p1.
		# P2 is the point (tuple)  from the track to be checked.
		# P1 is a tuple [lat, lng]
		# endAngle and startAngle are the directional angles of the FAI sector in which the x,y point
		# is to be checked.
		#
		#p1 = tp_nos
		#print "check_point Test if point:", p2, " is inside: ", tp_nos
		p1 = [tp_nos[2], tp_nos[3]] # Makes the supplied turning point index into lat,lng tuple
		
		polarradius = geopy.distance.distance(p1, p2).km
		# Check whether polarradius is less 
		# then radius of circle or not 
		#print "Radius: ", polarradius
		#print "Radius: ", polarradius, " P1: ", p1, " P2: ", p2
		if tp_nos[4] == "B" or tp_nos[4] == "S" or tp_nos[4] == "E": # Test for Barrel type turning point.  THIS WORKS ASSUMING S|E TREATED AS BARRELS
		#if tp_nos[4] == "B": # Test for Barrel type turning point
			if polarradius <= 0.5 : # Test for Barrel type turning point 
				#print "Point: ", p2, "does exist in sector type:", tp_nos[4], " For TP: ", tp_nos[1]
				return True
			else:
				#print "Radius: ", polarradius, " P1: ", p1, " P2: ", p2
				return False
		if polarradius == 0 :
			#print "Point: ", p2, "must exist in the FAI sector "
			return True
		if polarradius > radius :
			#print "Point: ", p2, "does not exist in the FAI sector for: ", tp_nos[1], " Radius: ", polarradius, " too far away"
			return False
		if polarradius <= radius:
			#print "Point: ", p2, "does exist in the FAI sector for: ", tp_nos[1], " Radius: ", polarradius
			
			#startAngle = tp_nos[7]
			#endAngle = tp_nos[8]
			startAngle = tp_nos[8]
			endAngle = tp_nos[9]
			#print type(p1) , type(p2) 
			bearing = self.compass_bearing((tp_nos[2], tp_nos[3]),(p2[0], p2[1])) # Compute bearing from TP to track point
			
			#print "TP1: ", (tp_nos[1], tp_nos[2], tp_nos[3]), " TP2: ", (p2[0], p2[1]), " Bearing to TP: ", bearing, " FAI Strt Angle: ", startAngle, " FAI End Angle: ", endAngle
			bearing_sum = ((delta_angle(bearing, startAngle)) + (delta_angle(bearing, endAngle)))
			#if (((delta_angle(bearing, startAngle)) + (delta_angle(bearing, endAngle))) <= 90):
			if bearing_sum <= 90:
				#print "Point: ", p2, "does exist in the FAI sector for:", tp_nos[1]
				return True
			else: 
				#print "Point: ", p2, "does not exist in the FAI sector for:", tp_nos[1], " Radius: ", polarradius, " Bearing: ", bearing, " Sum: ", bearing_sum
				return False
		
	def check_task_point(self, index, flt_lat, flt_lng):
		#
		# This needs to be thought about since once a segment of a track to a turning point has been reached there's
		# no need to check those track points for any other segment
		#
		# Checks each track point flt_lat, flt_lng against the list of turning points for the task
		#
		#print " Type Lat", type(flt_lat), " Type Lng: ", type(flt_lng)
		radius = 1 # For now. Make it a configurable variable
		
		#for i, tp in enumerate(tasks.subset_tp_list):
			#if i >= 10:
				#exit()
		for tp in tasks.subset_tp_list:
			#print "tp: ", tp
			#if tp[0] == 0 or tp[0] == len(tasks.subset_tp_list) - 1:
			#	continue
			#print "Test if point:", [flt_lat, flt_lng], " is inside: ", tp
			if not self.check_point(radius, tp, [flt_lat, flt_lng]):
				# If the track point is outside the FAI sector then continue to next turning point
				#print "Track point : ", index, " Lat: ", flt_lat, " Lng: ", flt_lng, " Outside TP: ", tp[1]
				#print "Outside sector type", tp[4], " Turning Point: ", tp[1], " Track Point: ", index
				continue
			else:
				if tp[4]!="S":
					if tp[4] == "E":
						if tp[4] == "E":
							if len(tasks.subset_tp_list) == 1:
								#print "Length tasks.subset_tp_list: 1"
								print("Inside sector type", tp[4], " Turning Point: ", tp[1], " Track Point: ", index)
								tasks.subset_tp_list.pop(0)
								return True
							return False
				#if tp[4] == "S" or tp[4] == "E":
				#	if tp[4] == "E":
				#		if len(tasks.subset_tp_list) == 1:
				#			#print "Length tasks.subset_tp_list: 1"
				#			print "Inside sector type", tp[4], " Turning Point: ", tp[1], " Track Point: ", index
				#			tasks.subset_tp_list.pop(0)
				#			return True
				#		print "Inside sector type", tp[4], " Turning Point: ", tp[1], " Track Point: ", index
				#		return False
				
					
					
				
				print("Inside sector type", tp[4], " Turning Point: ", tp[1], " Track Point: ", index)
				#if tp[4] == "S":
				#	print "Start point achieved"
				#print "Task tp list was: ", tasks.subset_tp_list
				for i, j in enumerate(tasks.subset_tp_list):
					#print "Search item", j, " At: ", i
					if j[1] == tp[1] and tp[4] == j[4] :					# Is 3-letter code of TP in list same a one for sector just found
						#print "Found at: ", i, " j[1]: ",j[1], " tp[1]: ", tp[1], " tp[4]: ", tp[4], " j[4]: ", j[4]
						tasks.subset_tp_list.pop(i)
						#print "Task tp list now: ", tasks.subset_tp_list
						return True
						#break
						
				#del tasks.subset_tp_list[0]	# Remove the first element in the turning point list since it's been achieved
				#print "Task tp list now: ", tasks.subset_tp_list
				return True
		return False
			
						
	def compute_tp_data(self, tp_codes):
		print()
		
	def check_barrel(self, lat, lng, rad):
		#
		# Scans through the turning point list and checks whether, lat/lng
		# is within the barrel, radius defined by rad
		#
		for self.row in tasks.subset_tp_list:
			self.dist = geopy.distance.vincenty((lat, lng), (self.row[2], self.row[3])).km
			print("Distance is: ", self.dist)
			if self.dist <= rad:
				return True
		return False
	
'''	
# Python3 program to check if a point  
# lies inside a circle sector. 
import math 
  
def checkPoint(radius, x, y, percent, startAngle): 
  
    # calculate endAngle 
    endAngle = 360 / percent + startAngle 
  
    # Calculate polar co-ordinates 
    polarradius = math.sqrt(x * x + y * y) 
    Angle = math.atan(y / x) 
  
    # Check whether polarradius is less 
    # then radius of circle or not and  
    # Angle is between startAngle and  
    # endAngle or not 
    if (Angle >= startAngle and Angle <= endAngle 
                        and polarradius < radius): 
        print("Point (", x, ",", y, ") "
              "exist in the circle sector") 
    else: 
        print("Point (", x, ",", y, ") " 
              "does not exist in the circle sector") 
  
# Driver code 
radius, x, y = 8, 3, 4
percent, startAngle = 12, 0
  
checkPoint(radius, x, y, percent, startAngle) 
  
# This code is contributed by 
# Smitha Dinesh Semwal 
'''	
		


#
# Either	https://www.navboys.com/user/UK2019MAR.zip, 
#        or http://www.newportpeace.co.uk/software/vrp-cup.cup
# need to make to work
# 
def main():
	def run_check_track(csv_file):
		print("run_check_track: ", csv_file)
		try:
			with open(csv_file, 'rb') as csvfile:
					try:
						data = csv.reader(csvfile)
					except:
						print("Read csv failed")
					print("CSV read")
					j = 0	
					for row in data:
						# Ignore first and last rows
						if j == 0 :
							j = 1
							continue
						index = row[0]
						#print "Track file row: ", row
						lat = float(row[5])
						lng = float(row[7])
						#print "Index: ", index, " Lat: ", lat, " Lng: ", lng
						#, lng, " Type Lat", type(lat), " Type Lng: ", type(lng)
						if task.check_task_point(index, lat, lng):
							if len(tasks.subset_tp_list) == 0:
								print("Finished")
								#exit()
							x = 1
							print("Time: ", row[3])
		except:
			print("Open csv failed")
	
	#run_check_track("/home/pjr/Downloads/969G5NR1.CSV")					
	#task = tasks("https://www.navboys.com/user/UK2019MAR.zip")
	#task = tasks("http://www.newportpeace.co.uk/software/vrp-cup.cup")
	#print tp.show_tp_list()	
	
	#
	# Test 1
	#
	#task.make_subset_tp_list(["RUF",  'MAL', 'POC', 'MAW', 'KEX', 'BRN', 'RU1', 'RUF'])
	
	#
	# Test 2
	#	
	#task.make_subset_tp_list([["GRL", "S"],  ['OXF', "F"], ['NWK', "F"], ['BSE', "F"], ['GRL', "E"]])
	#run_check_track("/home/pjr/Downloads/969G5NR1.CSV")
	
	#
	# Test 3
	#		
	#task.make_subset_tp_list([["GRL", "S"],  ['OXF', 'B'], ['NWK', 'B'], ['BSE', 'B'], ['GRL', 'E']])
	#run_check_track("/home/pjr/Downloads/969G5NR1.CSV")
	
	#
	# Test 4
	#
	#task.make_subset_tp_list([["LA6", "S"], ['ALT', "B"], ['RUG', "B"], ['FWL', "B"], ['THA', "B"], ['LAS', "E"]])	
	#run_check_track("/home/pjr/Downloads/969V87W1.csv")
	
	#
	# Test 5
	#
	#task.make_subset_tp_list([["CLK", "S"],["HAW", "F"],["CAE", "F"], ["CLK", "E"] ])
	#run_check_track("/home/pjr/Downloads/96FV1L11.csv")
	
	#
	# Test 6
	#
	#task.make_subset_tp_list([["SU2", "S"],["NRT", "F"],["HAN", "F"],["SOF", "F"],["SU2", "E"] ])
	#run_check_track("/home/pjr/Downloads/2019-06-18-XCS-388-01.csv")
	
	#
	# Test 7
	#
	#task.make_subset_tp_list([["SU2", "S"],["NRT", "F"],["HAN", "F"],["SOF", "F"],["SU2", "E"] ])
	#run_check_track("/home/pjr/Downloads/96ILHRT1.csv")
	
	
	
	#task.check_task_point(53.9516666667,  -1.18886666667)
	
	#task.check_task_point(54.134980, -0.79116867)		# RUF task
	#task.check_task_point(52.182383, -0.1128)		# BGA task
	
	#run_check_track("/home/pjr/Downloads/969G5NR1.CSV")	
	#run_check_track("/home/pjr/Downloads/969G5NR1.csv")	
	#run_check_track("/home/pjr/Downloads/969V87W1.csv")	
	#task.check_task_point(54.11983333333334, -0.7379999999999999)
	#print task.show_subset_tp_list()
	#print task.check_barrel(54.2289, -1.2097666666666667, 1)
	
if __name__ == "__main__":
	main()
			
			