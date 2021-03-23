from django.shortcuts import render
from satellites.models import Target, Observation
from django.http import HttpResponse, HttpResponseNotFound
from django.db import transaction
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.conf import settings
import dateutil.parser
import base64
import simplekml
from django.core.files import File
import os


@csrf_exempt
#create and store targets from coordinates with name attached
def setTarget(request):

    # If this is a POST request then retrieve the body data
    if request.method == 'POST':

        try:
            body_unicode = request.body.decode('utf-8')
            #load request body as json
            body = json.loads(body_unicode)

            #store coordinate as Point
            coord=Point(body['long'], body['lat'], body['elevation'])
            graph=Target(coord=coord, name=body['name'])
            graph.save()

            return HttpResponse()
        except:
            return HttpResponse(status=500)

    return HttpResponseNotFound()

@csrf_exempt
#find all targets within bounding box coordinates
def getTargets(request):

    if request.method == 'POST':

        try:
            body_unicode = request.body.decode('utf-8')
            #load request body as json
            points = json.loads(body_unicode)
            #convert coords to Points
            for i in range(len(points)):
                points[i]=Point(points[i]['long'], points[i]['lat'], points[i]['elevation'])

            #search for targets within bounding box of Points
            targets = queryTargets(points)

            return JsonResponse(targets, safe=False)
        except:
            return HttpResponse(status=500)

    return HttpResponseNotFound()

#helper function to query targets
def queryTargets(points):

    #create Polygon obj
    boundingBox=Polygon((points[0], points[1], points[2], points[3], points[0]))

    #search models whose coord fields are within boundingbox
    targets = list(Target.objects.filter(coord__within=boundingBox))

    #convert model to dict obj
    for i in range(len(targets)):
        targets[i]=model_to_dict(targets[i])
        targets[i]['coords']=targets[i]['coord'].coords
        del targets[i]['coord']

    return targets

@csrf_exempt
#store Observation instance according to params
#NOTE: image param is expected to be base64 encoded
def setObservation(request):

    # If this is a POST request then retrieve the body data
    if request.method == 'POST':

        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            #load request body as Json and write base64 encoded image field to img file
            with open("observation.png", 'wb') as f:
                f.write(base64.b64decode(body['image']))

            thumbnail="observation.png"

            #create model instance, save its image field with the image file above
            graph=Observation(image=thumbnail, timestamp=dateutil.parser.parse(body['timestamp']), name=body['name'])
            graph.image.save(
            name=os.path.basename(settings.IMG_URL+"/observation.png"),
            content=File(open("observation.png", 'rb'))
            )
            graph.save()

            return HttpResponse()
        except:
            return HttpResponse(status=500)

    return HttpResponseNotFound()

#helper function to query observations
def queryObservations(points, fromTime, toTime, retrieveImageFile):

    #create Polygon from Points
    boundingBox=Polygon((points[0], points[1], points[2], points[3], points[0]))

    #search models whose coords fields are within boundingbox
    targets = list(Target.objects.filter(coord__within=boundingBox))
    observations=[]
    #go through Target models selected
    for target in targets:
        #search Observations whose name are similar to the Targets selected
        observations+=list(Observation.objects.filter(name=target.name, timestamp__range=[fromTime,toTime]))
    #convert Observation to dict obj,
    #pass on observation image field if param in header is true
    for i in range(len(observations)):
        observations[i]=model_to_dict(observations[i])
        if retrieveImageFile:
            observations[i]['imageFile']=observations[i]['image']
        with open(observations[i]['image'].path, "rb") as image_file:
            observations[i]['image'] = base64.b64encode(image_file.read()).decode('utf-8')
    return observations

@csrf_exempt
#get a list of observations within boundingBox and time interval
def getObservations(request):

    if request.method == 'POST':

        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            points = body['points']
            fromTime = body['fromTime']
            toTime = body['toTime']

            #convert coords to Points
            for i in range(len(points)):
                points[i]=Point(points[i]['long'], points[i]['lat'], points[i]['elevation'])

            #search all Observations within boundingbox and within timeframe
            observations=queryObservations(points, fromTime, toTime, False)

            return JsonResponse(observations, safe=False)
        except:
            return HttpResponse(status=500)

        #html="<img src=\"data:image/png;base64,"+observations[0]['image']+"\">"

    return HttpResponseNotFound('<h1>Page not found</h1>')

@csrf_exempt
#retrieve kml file with targets localised
def viewTargets(request):

    if request.method == 'POST':

        try:
            kml=simplekml.Kml()

            body_unicode = request.body.decode('utf-8')
            points = json.loads(body_unicode)
            #convert coords to Points
            for i in range(len(points)):
                points[i]=Point(points[i]['long'], points[i]['lat'], points[i]['elevation'])

            #create Polygon for kml file
            boundingBox=Polygon((points[0], points[1], points[2], points[3], points[0]))
            pol=kml.newpolygon(name="bounding box", outerboundaryis=boundingBox, innerboundaryis=boundingBox)
            pol.style.polystyle.color="50000000"
            pol.style.polystyle.outline=0

            #get all target within boundingbox
            targets = queryTargets(points)
            for target  in targets:
                #add new point corresponding to Target to kml file
                kml.newpoint(name=target['name'], coords=[target['coords']])


            kml.save("targets.kml")
            #send stringified kml file content in json obj
            targets={"KmlFileStringified":kml.kml()}

            return JsonResponse(targets, safe=False)
        except:
            return HttpResponse(status=500)

    return HttpResponseNotFound()


@csrf_exempt
#retrieve kml file with observations localised according to target they represent
def viewObservations(request):

    if request.method == 'POST':

        try:
            kml=simplekml.Kml()

            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            points = body['points']
            fromTime = body['fromTime']
            toTime = body['toTime']
            #convert coords to Points
            for i in range(len(points)):
                points[i]=Point(points[i]['long'], points[i]['lat'], points[i]['elevation'])

            #create Polygon
            boundingBox=Polygon((points[0], points[1], points[2], points[3], points[0]))
            #add Polygon to kml file
            pol=kml.newpolygon(name="bounding box", outerboundaryis=boundingBox, innerboundaryis=boundingBox)
            pol.style.polystyle.color="50000000"
            pol.style.polystyle.outline=0

            #get observations within time and space intervals
            observations = queryObservations(points, fromTime, toTime, True)
            targets = queryTargets(points)
            for observation  in observations:
                #match observation to coorrespoding target
                target=list(filter(lambda elem: elem['name']==observation['name'] , targets))[0]
                #add ground overlay with image of observation at target location in kml file
                kml = simplekml.Kml()
                ground = kml.newgroundoverlay(name=target['name'])
                ground.icon.href = observation['imageFile'].url
                ground.gxlatlonquad.coords = [(target['coords'][0],target['coords'][1]),(target['coords'][0]+0.01,target['coords'][1]),(target['coords'][0]+0.01,target['coords'][1]+0.01),(target['coords'][0],target['coords'][1]+0.01)]


            kml.save("observations.kml")
            #save stringified kml file in json obj
            observations={"KmlFileStringified":kml.kml()}

            return JsonResponse(observations, safe=False)
        except:
            return HttpResponse(status=500)

    return HttpResponseNotFound()
