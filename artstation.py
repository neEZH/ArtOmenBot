import requests
import json


class AS:
    def __init__(self, name):
        self.__name = name
        print(f"Created AS object [" + self.__name + "]")

    @property
    def name(self):
        return self.__name


    @property
    def projsURL(self):
        return "https://www.artstation.com/users/" + str(self.__name) + "/projects.json"

    @property
    def ifArtist(self):
        url = self.projsURL
        data = requests.get(url).text
        print("ifArtist:" + str(bool(data)))
        return bool(data)

    @property
    def ifProjs(self):
        print("ifProjs:" + str(bool(self.getProjs)))
        return bool(self.getProjs)

    @property
    def getProjs(self):
        url = self.projsURL
        # returns array
        return json.loads(requests.get(url).text)["data"]

    @property
    def lastArt(self):
        projList = self.getProjs
        maxPublDate = max([project["published_at"] for project in projList])
        lastProj = next(project for project in projList if project["published_at"] == maxPublDate)
        print("Link: " + str(lastProj["permalink"]))

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