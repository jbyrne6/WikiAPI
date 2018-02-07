import json
import urllib.request
import re
import sys
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Homepage"

#@app.route('/')
def getData():
    searchTerm = input("Enter a band or musician name: ")
    originalSearchTerm = searchTerm
    addInfo = ""
    locationData = ""
    errorResponse = "Check your spelling."
    #if "(band)" not in searchTerm:
    #    searchTerm = searchTerm.title()
    searchTerm = searchTerm.title()

    if " " in searchTerm:
        searchTerm = searchTerm.replace(" ", "%20")
    url = "https://en.wikipedia.org/w/api.php?action=query&titles=" + searchTerm + "&prop=revisions&rvprop=content&format=json&formatversion=2"
    data = urllib.request.urlopen(url).read()
    readableData = json.loads(data)
    try:
        searchTermData = readableData["query"]["pages"][0]["revisions"][0]["content"]
    except:
        print(errorResponse)
        sys.exit()
    if "origin " in searchTermData:
        locationData = re.search('origin\s*=\s*.*', searchTermData)
        addInfo = " (band)"
        #print("band")
    elif "birth_place" in searchTermData:
        locationData = re.search('birth_place\s*=\s*.*', searchTermData)
        addInfo = " (musician)"
        #print("musician")

    if locationData is None:
        searchTerm = searchTerm + addInfo
        if " " in searchTerm:
            searchTerm = searchTerm.replace(" ", "%20")
        url = "https://en.wikipedia.org/w/api.php?action=query&titles=" + searchTerm + "&prop=revisions&rvprop=content&format=json&formatversion=2"
        data = urllib.request.urlopen(url).read()
        readableData = json.loads(data)
        searchTermData = readableData["query"]["pages"][0]["revisions"][0]["content"]
        locationData = re.search('origin\s*=\s*.*', searchTermData)
    #else:
        #print("not in loop")

    location = locationData.group(0)
    location = location.split("[[", 1)[-1]
    location = location.split("|", 1)[-1]
    location = location.split("= ", 1)[-1]
    location = location.split("<", 1)[0]
    location = location.replace("[","")
    location = location.replace("]","")
    location = location.replace("}}","")

    print(location)
    return location
getData()

#https://en.wikipedia.org/w/api.php?action=query&titles=The%20Beatles&prop=revisions&rvprop=content&format=json&formatversion=2
#1. if location data is None, then go to beginning and try to add (band)

if __name__ == "__main__":
    app.run(debug=True)
