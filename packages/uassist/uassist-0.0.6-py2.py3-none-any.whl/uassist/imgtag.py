"""imagetag module
"""
def imgtag(imgpath):
    """Extracts EXIF metadata from photo and outputs relevant information

    Args:
        imgpath (str): path to image file

    Returns:
        dict: metadata information
    """    

    import exifread
    from exifread.utils import get_gps_coords

    # Open image file for reading (must be in binary mode)
    f = open(imgpath, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f, details=False)
    gps = get_gps_coords(tags)

    latdd = round(gps[0], 7)
    longdd = round(gps[1], 7)
    
    gpsaltval = [c.decimal() for c in tags["GPS GPSAltitude"].values]
    gpsalt = round(gpsaltval[0], 2)

    date = tags["Image DateTime"]
    imgh = tags["EXIF ExifImageLength"]
    imgw = tags["EXIF ExifImageWidth"]
    make = tags["Image Make"]
    model = tags["Image Model"]

    print("UAS Make & Model: " + str(make) + " " + str(model))
    print("Capture Date & Time: " + str(date))
    print("Image resolution: " + str(imgh) + " x " + str(imgw))
    print("Latitude: " + str(latdd))
    print("Longitude: " + str(longdd))
    print("Altitude: " + str(gpsalt) + " meters")

    return [latdd, longdd, gpsalt]

def imgdir(folderpath):

    import os, exifread, ipyleaflet, datetime, uassist
    from exifread.utils import get_gps_coords
    from ipyleaflet import Marker, Popup
    from ipywidgets import HTML

    altlist = []
    xlist = []
    ylist = []
    timelist = []
    imghwlist = []
    makemodellist =[]
    coorddict = {}
    m = uassist.Map(google_map = "HYBRID", height="600px")

    for filename in os.listdir(folderpath):
        if filename.endswith(".jpg") or filename.endswith(".JPG"): 
            #print(os.path.join(folder, filename))cona
            #print(filename)
            filepath = folderpath + "/" + filename
            f = open(filepath, 'rb')
            tags = exifread.process_file(f, details=False)

            # GPS Altitude Values
            gpsaltval = [c.decimal() for c in tags["GPS GPSAltitude"].values]
            gpsalt = round(gpsaltval[0], 2)
            altlist.append(gpsalt)

            # GPS Coords
            gps = get_gps_coords(tags)
            latdd = round(gps[0], 7)
            longdd = round(gps[1], 7)
            
            xlist.append(latdd)
            ylist.append(longdd)

            xy = [latdd, longdd]
            xyz = [latdd, longdd, gpsalt]

            coorddict[filename] = xyz

            # timestamps
            datetimestr = str(tags.get("Image DateTime"))
            datetimeobj = datetime.datetime.strptime(datetimestr, '%Y:%m:%d %H:%M:%S')
            timelist.append(datetimeobj)
            
            # model
            make = str(tags["Image Make"])
            model = str(tags["Image Model"])
            makemodel = (make + " " + model)
            if makemodel not in makemodellist:
                makemodellist.append(makemodel)
            
            #image width and height
            imgh = str(tags.get("EXIF ExifImageLength"))
            imgw = str(tags.get("EXIF ExifImageWidth"))
            imghw = (imgw + " x " + imgh)
            if imghw not in imghwlist:
                imghwlist.append(imghw)

            
            # Map markers and popup
            marker = Marker(location=xy, draggable=False)
            m.add_layer(marker)
            
            message = HTML()
            message.value = (filename + "</br>" + str(gpsalt) + " m altitude" + "</br>" + str(datetimestr))
            
            marker.popup = message
            

            #print(filename + "- (" + str(latdd) + ", " + str(longdd) + ", " + str(gpsalt) + ")")
            #print(filename + " " + str(xyz))
            continue
        else:
            continue

    #print(altlist)
    imgcount = len(altlist)

    altsum = sum(altlist)
    altavg = (altsum / imgcount)

    mintime = min(timelist)
    maxtime = max(timelist)

    print("Image Count: " + str(imgcount))
    print("Average Altitude: " + str(round(altavg, 3)))
    print("Max Altitude " + str(max(altlist)))
    print("Min Altitude: " + str(min(altlist)))
    print("UAS Make & Model(s): " + str(makemodellist))
    print("Image resolution(s): " + str(imghwlist))
    print("Time range: " + str(mintime) + " - " + str(maxtime))




    bounds = [[min(xlist),min(ylist)], [max(xlist), max(ylist)]] 
    m.fit_bounds(bounds)
    #The lat/lon bounds in the form [[south, east], [north, west]].

    #res = list(coorddict.keys())[0]
    #center = list(coorddict.get(res))[0:2]
    #print(center)

    return(m)