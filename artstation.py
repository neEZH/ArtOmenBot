import requests
import json

class AS:
    def __init__(self, name):
        self.name = name

    def ifArtist(self):
        return bool(requests.get("https://www.artstation.com/users/" + str(self.name) + "/projects.json").text)

    def ifProjs(self):
        return bool(self.getProjs()['total_count'])

    def getProjs(self):
        return json.loads(requests.get("https://www.artstation.com/users/" + str(self.name) + "/projects.json").text)["data"]

    def lastArt(self):
        #
        # maxDate = ""
        # maxIx = 0
        return next(project for project in self.getProjs() if project["published_at"] == max([project["published_at"] for project in self.getProjs()]))
        # for prDate in (self.getProjs()["data"]["published_at"] for self.getProjs() )
        # for proj in self.getProjs()["data"]:
        #     if maxDate < proj["published_at"]:
        #         maxDate = proj["published_at"]

