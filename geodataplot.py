print("Welcome!")
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.patches as mpatches
now = datetime.utcnow()
daydelta = int(input("How many days do you want to plot? (≤ 240) "))
pasttime = datetime.utcnow() - timedelta(days=daydelta)
pasttimestr = datetime.isoformat(pasttime).split('.')[0]
pasttimestr = pasttimestr + 'Z'
print("Start time:", pasttimestr)

timestr = datetime.isoformat(now).split('.')[0]
timestr = timestr + 'Z'
url = "https://geomag.usgs.gov/ws/data/?id=BOU&elements=H&format=json&starttime=" + pasttimestr + "&endtime=" + timestr
print("URL:", url)
print("Requesting JSON data...")
request = requests.get(url)
data = request.text
if(request.status_code == 200):
    print("Done!", request.status_code)
else:
    print("RESPONSE CODE", request.status_code)
#data = data.replace(",null","")
print("Loading JSON data...")
jsondata = json.loads(data)
print("Done!")
print("Filtering data...")
fildat = jsondata["values"][0]["values"]
fildattime = jsondata["times"]
fildattime = fildattime[:len(fildat)]
fildattime = pd.to_datetime(fildattime)
print("Done!")
# Rolling Average
fildatdf = pd.DataFrame(fildat)
windowsz = int(input('Window size? '))
print("Making rolling average...")
datrollav = fildatdf.rolling(windowsz).mean()
print("Done!")
print(len(datrollav))
print("Making Plot...")
red_patch = mpatches.Patch(color='red', label='Rolling Average')
black_patch = mpatches.Patch(color='black', label='Raw Data')
plt.plot(fildattime, fildat, color='black', linewidth=1)
plt.plot(fildattime, datrollav, color='red', linewidth=1)
plt.ylim(20600,20800)
plt.legend([black_patch, red_patch], ['Raw Data', 'Rolling Average'])
plt.grid(linestyle=':')
plt.title('Boulder Magnetometer - ' + str(daydelta) + ' Days')
plt.xlabel('Time')
plt.ylabel('nT')
print("Done!")
plt.show()
print("Goodbye!")
