#
# 20190313	 Working version taken from Eclipse
#
import ephem
#from ephem import Sun
import datetime
import pytz
from timezonefinder import TimezoneFinder
from dateutil.tz import gettz
import tzlocal

# 
# This module provides a function to test whether sunset time has passed
# given the coordinates of a location, normally the airfield for which flights are being logged.
# The time at the airfield coordinates is used and not local (ie system) time so should take into account Summer Time/Winter Time at the
# logging location
#
# 20190119
#
# Code based on an idea supplied by Steve Ball
#


class init_sunset_test():
	def __init__(self, loc):
		#
		# This is the only part that is not time dependent
		#
		tzf = TimezoneFinder()
		tz = tzf.certain_timezone_at(lng=float(loc[1]), lat=float(loc[0]))
		self.timezone = pytz.timezone(tz)
		self.UTC = pytz.timezone('UTC')
		self.s = ephem.Sun()
		self.location = ephem.Observer()
		self.location.lat = loc[0]
		self.location.long = loc[1]
		self.location.elevation = loc[2]						# ephem object Datetime in UTC
		self.location.pressure = 0
		return
		
	def is_sunset_now(self, loc): 
		#
		# Test if the previous sunrise and the next sunset or on the same day
		# then the sun must have risen, ie time is past sunrise and set today
		# since next sunset is tomorrow, ie the sun has set, hence risen and set today.
		# It thus requires current time to be used as basis
		#
		
		self.utc_dt = datetime.datetime.now(self.UTC)
		self.local_dt = datetime.datetime.now(self.timezone)
		#print "Time zone: ", self.timezone, " Time zone Datetime Now: ", self.local_dt, " UTC Datetime Now: ", self.utc_dt
		
		self.location.date = self.utc_dt							# ephem object Datetime in UTC
		self.Sunset = self.location.next_setting(self.s)			# UTC  sunset time, ephem object type
		self.Sunrise = self.location.previous_rising(self.s)		# UTC sunrise time, ephem object type
		
		self.utc_srdt = datetime.datetime.strptime(str(self.Sunrise.datetime()), "%Y-%m-%d %H:%M:%S.%f")	# Convert to datetime type
		self.utc_ssdt = datetime.datetime.strptime(str(self.Sunset.datetime()), "%Y-%m-%d %H:%M:%S.%f")		# Convert to datetime type
		
		self.tz_srdt = self.utc_srdt.replace(tzinfo=pytz.utc).astimezone(self.timezone) 	# Convert to timezone time, ie local time
		self.tz_ssdt = self.utc_ssdt.replace(tzinfo=pytz.utc).astimezone(self.timezone) 	# Convert to timezone time, ie local time
		self.tz_srdt_day = datetime.datetime.strftime(self.tz_srdt,"%Y/%m/%d")				# Get current local sunrise day 
		self.tz_ssdt_day = datetime.datetime.strftime(self.tz_ssdt,"%Y/%m/%d")				# Get current local sunset day
		self.tz_dt_day = datetime.datetime.strftime(self.local_dt,"%Y/%m/%d")					# Get current local day
		'''
		print 	" Local srdt: ", self.tz_srdt, \
				" Local ssdt: ",self.tz_ssdt, \
				" Local sunrise day: ", self.tz_srdt_day, \
				" Local sunset day: ", self.tz_ssdt_day, \
				" Local now day: ", self.tz_dt_day
		'''
		#
		# Have to check that sunrise and sunset are on the same day 
		# Because sunrise and sunset day has been determined by time then, 
		# if yes then sun not set, else sun has set	
		#
		if self.tz_srdt_day == self.tz_dt_day and self.tz_ssdt_day == self.tz_dt_day:
#			print "Previous sunrise & next sunset on same day, must daylight, sun not set. Local Time: ", self.local_dt, " Sunset: ", self.tz_ssdt
			return False
		else:
#			print "Previous sunrise & next sunset not same day, must be night time, sun is set. Local Time: ", self.local_dt, " Sunset: ", self.tz_ssdt
			print(" Local srdt(sun rise date): ", self.tz_srdt, \
					" Local ssdt(sub set date: ",self.tz_ssdt, \
					" Local sunrise day: ", self.tz_srdt_day, \
					" Local sunset day: ", self.tz_ssdt_day, \
					" Local now day: ", self.tz_dt_day)
			
			return True	
	
	def local_sunset(self):	 
		return datetime.datetime.strftime(self.tz_ssdt,"%H:%M")
			
#	def utc_to_local(self, utc_dt):
#		local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(self.timezone)
#		return local_tz.normalize(local_dt) # .normalize might be unnecessary
		
#
# Testing
#
'''
location = [str(54.2289592), str(-1.20928758608), 238.25]		#Europe/UK Sutton Bank
check = init_sunset_test(location)
issunset = check.is_sunset_now(location)
print "Is sun set now?: ", issunset
location = [str(34.052235), str(-118.243683), 238.25]			#USA/Los Angeles, don't worry about altitude
check = init_sunset_test(location)
issunset = check.is_sunset_now(location)
print "Is sun set now?: ", issunset
'''		

		
		
	
		


