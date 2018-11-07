import ogr, os
import time, datetime
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

gpx_path = "C:/Users/ngavish/.qgis2/python/plugins/GPXToSpaceTimeCube/sample data/AaseeLoop.gpx" #Enter your GPX Path here

#Open GPX
in_path = os.path.join (gpx_path)
in_driver= ogr.GetDriverByName("GPX")
data_source = in_driver.Open(in_path,0)

#Plot parameters
mpl.rcParams ['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.gca(projection='3d')

#Create layer from data source
if data_source is None:
    print "Could not open %s" % (in_path)
else:
    print "Opened %s" % (in_path)
    layer = data_source.GetLayer(4) # 0 - waypoints, 1 - routes, 2 - tracks, 3 - route points, 4 - track points 
            
#Get time and spatial data from GPX dynamically and plot
x=[] #Latitude
y=[] #Latitude
z=[] ##Time in minutes since start 
elapsedTime=[] #Time in seconds since epoch
DTArray=[] ##Array of python strings
DateTimeArray=[] #Python datetime object of each point
schema=[]

ldefn = layer.GetLayerDefn()
for n in range(ldefn.GetFieldCount()):
    fdefn = ldefn.GetFieldDefn(n)
    schema.append(fdefn.name)

try:
    timeIndex=schema.index('time')
except ValueError:
    print "No time field found"

try:
    for feat in layer:
        pt = feat.geometry()
        x.append(pt.GetX())
        y.append(pt.GetY())
        dateTime=feat.GetField(timeIndex)
        try:
            DT=datetime.datetime.strptime(dateTime, "%Y/%m/%d %H:%M:%S+00" )
        except ValueError:
            DT=datetime.datetime.strptime(dateTime, "%Y/%m/%d %H:%M:%S.%f+00" )
        DateTimeArray.append(DT)
        SSE= time.mktime(DT.timetuple()) #Seconds since epoch
        elapsedTime.append(SSE)
        DTArray.append(DT.strftime("%H:%M:%S"))
except TypeError:
    print "Time field does contain none or invalid dates"


#Create sub title for plot
title=DateTimeArray[0].strftime("%Y/%m/%d")+" " +DTArray[0]+" to " + DateTimeArray[-1].strftime("%Y/%m/%d")+" "+DTArray[-1]

#Extract elapsed time in minutes 
z.append(0) #First item in elapsedTime array should be 0 
for i in range(1,len(elapsedTime)):
    z.append((elapsedTime[i]-elapsedTime[0])/60)

#Plot X,Y,Z
ax.plot(x,y,z)

#Labels & Plot
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Time (Minutes)')
ax.legend()
plt.axis("equal")
fig.suptitle('Space Time Cube', fontsize=12, fontweight='bold')
plt.title(title,loc='center')
plt.show()

#Optionally save the image
#plt.savefig("C:/Output/SpaceTimePlot.jpg", dpi=100, format="jpg")

##Optionally animate image 
#for angle in range(0, 360):
#    ax.view_init(30, angle)
#    plt.draw()
#    plt.pause(.001)

print "DONE"
