#
# Function to determine latitude, longitude and elevation given location place name details.
# Details are returned as a list.
# For example if called as:
# loc = get_coords("My Gliding Club UK")
#   then:
#        latitude = loc[0], longitude = loc[1], elevation = loc[2]
#
import os
#os.environ["GOOGLE_API_KEY"] = "api_key_from_google_cloud_platform"
#os.environ["GOOGLE_API_KEY"] = "OGN_Flogger"
#20181010    This has a problem that google geocoder API now needs a Key to get elevation data. For now it has to be supplied
#            in the GUI field. The elevation can be found using: https://www.freemaptools.com/elevation-finder.htm
# 
#20181010    This has a problem that google geocoder API now needs a Key to get elevation data. For now it has to be supplied
#            in the GUI field. The elevation can be found using: https://www.freemaptools.com/elevation-finder.htm
# 
from geopy.geocoders import Nominatim
import geocoder
from geopy.exc import GeocoderTimedOut 
import time
from geopy.geocoders.base import ERROR_CODE_MAP
import geopy
from geopy import geocoders
import requests
import json

import ssl
import certifi

def set_ssl_context():
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    print("geopy.geocoders.options.default_ssl_context is: ", ctx)

def get_coords(address, settings):
    print("get_coords called with: ", address)
    set_ssl_context()
    
    try:    
        geolocator = Nominatim(user_agent="OGN_Flogger")
    except:
        print("Nominatim failed")    
#    geolocator = Nominatim()
#    g = geolocator.geocode()
    try:
        place, (lat, lng) = geolocator.geocode(address, exactly_one=True, timeout=20)
    except:
        print("Geolocator failed. Address is: ", address)
#    place, (lat, lng) = geolocator.geocode(address, exactly_one=True, timeout=10, verify=False)
    print("Location details. %s: %.5f, %.5f" % (place, lat, lng))
    
    #if settings.FLOGGER_QNH <> "":
    #    return lat, lng, settings.FLOGGER_QNH
#    lng = str(-1.20930940595)
#    lat = str(54.2289539)
    lng = str(lng)
    lat = str(lat)
#    url = "https://elevation-api.io/api/elevation?points=(" + lat + "," + lng
    #url = "https://elevation-api.io/api/elevation?points=(" + lat + "," + lng + ")" 
    #print "url string is: ", url
    #jsondata = requests.get(str(url))
    #x = json.loads(jsondata.text)
    #alt =  x["elevations"][0]["elevation"]
    #print type(alt)
    #print "elevation is: ", alt
    #return lat, lng, alt

    url = "http://api.opentopodata.org/v1/eudem25m?locations=" + lat + "," + lng
    print("New url: ", url)
    res = requests.post(str(url), data=dict(key1="elevation"))
    #print "res: ", res.text
    x = json.loads(res.text)
    #print "x is: ", x
    alt = x["results"][0]["elevation"]
    print("Opentopodata rtns: ", alt)
    
    return lat, lng, alt

#https://api.opentopodata.org/v1/eudem25m?locations=54.2309197,-1.20836974297 
#
#gives
#
#results    
#0    
#dataset    "eudem25m"
#elevation    288.49591064453125
#location    
#lat    54.2309197
#lng    -1.20836974297
#status    "OK"
    
    #
    # Below here doesn't work any more
    #
    ele = geocoder.google([lat, lng], method='elevation') 
    print(address, " Elevation is: ", ele.meters)
    try:
        geolocator = Nominatim(user_agent="OGN_Flogger")
        try:   
            location = geolocator.geocode(address, timeout=5, exactly_one=True)  # Only 1 location for this address
#            location = geocoder.google(address, timeout=5, exactly_one=True)  # Only 1 location for this address
            if location == None:
                print("Geocoder Service timed out or Airfield: ", address, " not known by geocode locator service. Check settings")
                return False
            print(address, " Is at: ", " Lat: ", location.latitude, " Long: ", location.longitude, " Alt: ", location.altitude)
#            print address, " Is at: ", location.latlng
#           print address, " Is at: ", " Lat: ", location.latitude, " Long: ", location.longitude, " Alt: ", location.altitude
            
            i = 1
            while i <= 5:
#                ele = geocoder.google([location.latitude, location.longitude], method='elevation')
                ele = geocoder.google([location.latitude, location.longitude], method='elevation', key= "")
#                ele = geolocator.geocode([location.latitude, location.longitude], method='elevation')
#                ele = geocoder.google([location.latitude, location.longitude], method='elevation', key="AIzaSyA6FEQW_6e5Va0bUd9BHqTLUWEqFmKOSXg")
#                ele = geocoder.bing([location.latitude, location.longitude], method="reverse")
                print("Elevation returned: ", ele)
                if ele.meters == None:
                    print("geocoder.google try: ", i)
                    i = i + 1
                    time.sleep(1)
                    continue
                else:
                    print("Geolocator worked for: ", address, " Lat: ", location.latitude, " Long: ", location.longitude, " Ele: ",ele.meters)
                    return location.latitude, location.longitude, ele.meters
                print("Geolocator failed for: ", address, " Lat: ", location.latitude, " Long: ", location.longitude, " Ele: ", ele.meters, "Try a Restart") 
                exit(2)
            
        except ERROR_CODE_MAP[400]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[400])
        except ERROR_CODE_MAP[401]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[401])
        except ERROR_CODE_MAP[402]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[402])
        except ERROR_CODE_MAP[403]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[403])
        except ERROR_CODE_MAP[407]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[407])
        except ERROR_CODE_MAP[412]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[412])
        except ERROR_CODE_MAP[413]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[413])
        except ERROR_CODE_MAP[414]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[414])
        except ERROR_CODE_MAP[502]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[502])
        except ERROR_CODE_MAP[503]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[503])
        except ERROR_CODE_MAP[504]:
            print(" ERROR_CODE_MAP is: ",  ERROR_CODE_MAP[503])
        return False
    except GeocoderTimedOut as e:
        print("Geocoder Service timed out for Airfield: ", address)
        return False
