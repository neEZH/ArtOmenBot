import requests
import json


class AS:
    def __init__(self, name):
        self.name = name

    @property
    def projsURL(self):
        return "https://www.artstation.com/users/" + str(self.name) + "/projects.json"

    @property
    def ifArtist(self):
        url = self.projsURL
        data = requests.get(url).text
        return bool(data)

    @property
    def ifProjs(self):
        return bool(self.getProjs()['total_count'])

    @property
    def getProjs(self):
        url = self.projsURL
        return json.loads(requests.get(url).text)["data"]

    @property
    def lastArt(self):
        # return next(project for project in self.getProjs() if project["published_at"] == max([project["published_at"] for project in self.getProjs()]))
        maxPublDate = max([project["published_at"] for project in self.getProjs])
        projList = self.getProjs
        return next(project for project in projList if project["published_at"] == maxPublDate)

    @staticmethod
    def findWork(query="", perPage="5" ):
        url ="https://www.artstation.com/api/v2/search/projects.json"
        try:
            req = {"page": 1, "per_page": int(perPage), "query": str(query)}
            return requests.get(url, json=req).text
        except Exception:
            return {"error": str(Exception)}
        # Sorting: relevance likes date rank

    @staticmethod
    def findArtist(query="", perPage="5"):
        url ="https://www.artstation.com/api/v2/search/users.json"
        try:
            req = {"page": 1, "per_page": int(perPage), "query": str(query)}
            return requests.get(url, json=req).text
        except Exception:
            return {"error": str(Exception)}


