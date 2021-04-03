import requests
import json


class AS:
    def __init__(self, name):
        self.name = name

    @property
    def ifArtist(self):
        return bool(requests.get("https://www.artstation.com/users/" + str(self.name) + "/projects.json").text)

    @property
    def ifProjs(self):
        return bool(self.getProjs()['total_count'])

    @property
    def getProjs(self):
        return json.loads(requests.get("https://www.artstation.com/users/" + str(self.name) + "/projects.json").text)[
            "data"]

    @property
    def lastArt(self):
        # return next(project for project in self.getProjs() if project["published_at"] == max([project["published_at"] for project in self.getProjs()]))
        maxPublDate = max([project["published_at"] for project in self.getProjs])
        projList = self.getProjs
        return next(project for project in projList if project["published_at"] == maxPublDate)

    @staticmethod
    def findWork(query="", perPage="5"):
        try:
            req = {"additional_fields": [], "filters": "", "page": 1, "per_page": int(perPage), "pro_first": 1, "query": str(query), "sorting": "rank"}
        except Exception:
            return {"error": str(Exception)}
        # Sorting: relevance likes date rank

        return json.loads(requests.get("https://www.artstation.com/api/v2/search/projects.json", json=req).text)
