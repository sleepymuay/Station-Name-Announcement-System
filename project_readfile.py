import importlib.util
import os
import sys

# List of required packages
required_packages = ['pandas', 'pygame']

# Check if a package is installed
def package_installed(package_name):
    spec = importlib.util.find_spec(package_name)
    return spec is not None

# Install missing packages
def install_packages(package_list):
    for package in package_list:
        print(f"Installing {package}...")
        os.system(f"pip install {package}")

# Check for required packages
missing_packages = [package for package in required_packages if not package_installed(package)]

# If any packages are missing, install them
if missing_packages:
    print("Some required packages are missing. Installing...")
    install_packages(missing_packages)
    # Restart script to import newly installed packages
    os.execl(sys.executable, sys.executable, *sys.argv)
    
import serial
from time import *
import pandas as pd
import datetime
import math
import pygame

def dec2deg(value):
   dec = value/100.00
   deg = int(dec)
   min = (dec - int(dec))/0.6
   position = deg + min
   position = "%.7f" %(position)
   return position


def getspeed():
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.1)
    gpsdata=ser.readline()
    gpsdata = gpsdata.decode("unicode_escape")
    gpsdata = gpsdata.split(',')
    # print(gpsdata)
    if "$GNRMC" in gpsdata[0]:
        speed = round(float(gpsdata[7])*1.852,2)
        print("func",speed)
        return float(speed)
   
mapscale = 18   
    
# Array to store station data
stations = []
pygame.mixer.init()

# Read station from csv name "station.csv"
csv_file_path = 'station.csv'
df = pd.read_csv(csv_file_path)
max_station = 8
previous_station = 0

for _, row in df.iterrows():
    station_info = {
        'station_number': int(row['station_number']),
        'latitude1': float(row['lattitute1']),
        'latitude2': float(row['lattitute2']),
        'longitude1': float(row['longtitute1']),
        'longitude2': float(row['longtitute2']),
        'name': row['station_name'],
        'sound': str(row['station_sound']),
        'latitude' : (float(row['lattitute1']) + float(row['lattitute2']))/2 ,
        'longitude' : (float(row['longtitute1']) + float(row['longtitute2']))/2 ,
    }
    stations.append(station_info)

try:
    while True:
        port="/dev/ttyAMA0"
        ser=serial.Serial(port, baudrate=9600, timeout=0.05)
        gpsdata=ser.readline()
        gpsdata = gpsdata.decode("unicode_escape")
        gpsdata = gpsdata.split(',')
        if "$GNRMC" in gpsdata[0]:
            hrs, min, sec = gpsdata[1][0:2], gpsdata[1][2:4], gpsdata[1][4:6]
            day, month, year = gpsdata[9][0:2], gpsdata[9][2:4], gpsdata[9][4:6]
            datetimeutc = "{}:{}:{} {}/{}/{}".format(hrs, min, sec, day, month, year)
            time_format = '%Y/%m/%d-%H:%M:%S'
            datetimeutc = datetime.datetime.now().strftime(time_format)
            speed = round(float(gpsdata[7])*1.852,2)
            message = "Datetime={} ,speed={} kmph".format(datetimeutc, speed)
            print(message)
        if "GNGGA" in gpsdata[0]:
            print(gpsdata)
            lat = dec2deg(float(gpsdata[2]))
            lon = dec2deg(float(gpsdata[4]))
            alt = gpsdata[9]
            satcount = gpsdata[7]
            
            for station in stations:
                station_dist = math.sqrt((float(lat) - float(station['latitude']))**2 + (float(lon) - float(station['longitude']))**2)
                print(station_dist)
                if station_dist < 0.00019:  # Adjust threshold distance for stations
                    if(previous_station == station):
                        break
                    print(f"At station {station['name']} ({station['station_number']})")
                    previous_station = station
                    pygame.mixer.music.load("./sound/appoarch/"+(station['sound'])+".mp3") 
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy() == True:
                        pygame.time.Clock().tick(10)
                    while True:
                        next_station_index=0
                        speed = getspeed()
                        if speed is not None:
                            if(next_station_index != max_station):
                                next_station_index = (float(station['station_number']) % len(stations)) + 1
                            # Find the next station based on station number
                            if next_station_index > len(stations):
                                next_station_index = 0  # Wrap around to the first station
                            next_station_index = (float(station['station_number']) % len(stations)) + 1
                            
                            next_station = next(s for s in stations if s['station_number'] == next_station_index)

                            if speed > 10:
                                print(f"Next station: {next_station['name']} ({next_station['station_number']})")
                                pygame.mixer.music.load("./sound/next/"+(next_station['sound'])+".mp3") 
                                pygame.mixer.music.play()
                                while pygame.mixer.music.get_busy() == True:
                                    pygame.time.Clock().tick(10)
                                break
       

except (KeyboardInterrupt, SystemExit):
    print("\nExiting.")
