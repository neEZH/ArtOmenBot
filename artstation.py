import requests
import json


class AS:
    def __init__(self, name):
        self.__name = name
        self.__projs = self.getProjs
        print(f"Created AS object [" + self.__name + "]")

    @property
    def name(self):
        return self.__name


    @property
    def projsURL(self):
        return "https://www.artstation.com/users/" + str(self.__name) + "/projects.json"

    @property
    def ifArtist(self):
        print("ifArtist:" + str(bool(self.__projs)))
        return bool(self.__projs)

    @property
    def getProjs(self):
        url = self.projsURL
        # returns array
        if requests.get(url).text:
            return json.loads(requests.get(url).text)["data"]
        else:
            return False

    @property
    def lastArt(self):
        projList = self.__projs
        maxPublDate = max([project["published_at"] for project in projList])
        lastProj = next(project for project in projList if project["published_at"] == maxPublDate)
        # returns object
        return lastProj

    @staticmethod
    def findWork(query="", perPage="5"):
        url = "https://www.artstation.com/api/v2/search/projects.json"
        try:
            req = {"page": 1, "per_page": int(perPage), "query": str(query)}
            return json.loads(requests.get(url, json=req).text)["data"]
        except Exception:
            return {"error": str(Exception)}
        # Sorting: "relevance" "likes" "date" "rank"

    @staticmethod
    def findArtist(query="", perPage="5"):
        url = "https://www.artstation.com/api/v2/search/users.json"
        try:
            req = {"page": 1, "per_page": int(perPage), "query": str(query)}
            return json.loads(requests.get(url, json=req).text)["data"]
        except Exception:
            return {"error": str(Exception)}