from xml.dom import minidom
import zipfile
from fitparse import FitFile

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from datetime import date


# Enable debug logging
import logging
import itertools
logging.basicConfig(level=logging.INFO)

today = date.today()

'''
#try:
# Initialize Garmin client with credentials
# Only needed when your program is initialized
client = Garmin('viktor_fagerlind@hotmail.com', '6iZoXg4EooP3dpUg')

# Login to Garmin Connect portal
# Only needed at start of your program
# The library will try to relogin when session expires
client.login()

# Get activities data
activities = client.get_activities(0,1) # 0=start, 1=limit
print(activities)

#for activity in activities:
activity = activities[0]
activity_id = activity["activityId"]
#print('\n\n------ Activity: ' + str(activity_id) + ' ------')

#tcx_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.TCX)
#xmldoc = minidom.parseString(tcx_data)

zip_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
zip_filename = f"./{str(activity_id)}.zip"
with open(zip_filename, "wb") as fb:
    print('------ ' + zip_filename + ' ------')
    fb.write(zip_data)

with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
    zip_ref.extractall('.')
'''
activity_id = '5094851020'

fitfile = FitFile(f'./{str(activity_id)}.fit')
fitfile.parse()

# Get all data messages that are of type record
sought = {'lap':['avg_cadence', 'total_distance', 'total_elapsed_time', 'timestamp'],
          'length':['avg_swimming_cadence', 'total_strokes', 'total_elapsed_time', 'timestamp']}
for info_type in sought:
    print('\n---' + info_type + '---')
    msg = next(fitfile.get_messages(info_type))
    for field in msg:
        if field.name in sought[info_type]:
            print('{:>38}'.format(field.name), end ='')
    for msg in fitfile.get_messages(info_type, as_dict=False):
        # Go through all the data entries in this record
        print('')
        for field in msg:
            if field.name in sought[info_type]:
                # Print the records name and value (and units if it has any)
                if field.value is None:
                    print('{:>25} {:>12}'.format('--', '-'), end='')
                elif field.units:
                    print('{:>25} {:>12}'.format(str(field.value), field.units), end='')
                else:
                    print('{:>25} {:>12}'.format(str(field.value), '-'), end='')

for msg in fitfile.messages:
    print('\n\n==> ' + msg.name, end=': ')
    print(msg)
    for d in msg:
        print(d, end=', ')
print('')

'''
xmldoc = minidom.parse('activity_5083417722.tcx')
laps = xmldoc.getElementsByTagName('Lap')
for lap in laps:
    lap.getElementByTagName()[0]
'''
#print(tree)

#print(tcx_data)
'''
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client init: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client init")
    quit()
'''
'''
# Get full name from profile
try:
    print(client.get_full_name())
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get full name: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get full name")
    quit()


# Get unit system from profile
try:
    print(client.get_unit_system())
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get unit system: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get unit system")
    quit()


# Get activity data
try:
    print(client.get_stats(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get stats: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get stats")
    quit()


# Get heart rate data
try:
    print(client.get_heart_rates(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get heart rates: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get heart rates")
    quit()


# Get body composition data
try:
    print(client.get_body_composition(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get body composition: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get body composition")
    quit()


# Get stats and body composition data
try:
    print(client.get_stats_and_body(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get stats and body composition: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get stats and body composition")
    quit()

# Get activities data
try:
    activities = client.get_activities(0,1) # 0=start, 1=limit
    print(activities)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get activities: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get activities")
    quit()

# Download an Activity
try:
   for activity in activities:
      activity_id = activity["activityId"]

      gpx_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.GPX)
      output_file = f"./{str(activity_id)}.gpx"
      with open(output_file, "wb") as fb:
          print('------ ' + output_file + ' ------')
          fb.write(gpx_data)

      tcx_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.TCX)
      output_file = f"./{str(activity_id)}.tcx"
      with open(output_file, "wb") as fb:
          print('------ ' + output_file + ' ------')
          fb.write(tcx_data)

      zip_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
      output_file = f"./{str(activity_id)}.zip"
      with open(output_file, "wb") as fb:
          print('------ ' + output_file + ' ------')
          fb.write(zip_data)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get activity data: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get activity data")
    quit()
    

#Get sleep data
try:
    print(client.get_sleep_data(today.isoformat()))

except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get sleep data: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get sleep data")
    quit()

'''