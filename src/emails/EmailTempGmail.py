import requests
import time

from src.utils.LinkExtract import LinkExtractor


class EmailTempGmail:

    def __init__(self, api) -> None:
        global links
        links = []

        self.api = api
        self.email = ''
        self.timestamp = ''

        url = "https://temp-gmail.p.rapidapi.com/get"

        querystring = {"domain": "gmail.com", "username": "random", "server": "server-1", "type": "real"}

        headers = {
            "X-RapidAPI-Host": "temp-gmail.p.rapidapi.com",
            "X-RapidAPI-Key": self.api
        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()

        if response['code'] == 200:
            self.email = response['items']['email']
            self.timestamp = response['items']['timestamp']
        else:
            Exception("Couldn't get E-Mail...")

    def checkEmail(self):

        url = "https://temp-gmail.p.rapidapi.com/check"

        querystring = {"email": self.email, "timestamp": self.timestamp}

        headers = {
            "X-RapidAPI-Host": "temp-gmail.p.rapidapi.com",
            "X-RapidAPI-Key": "28d36f41b7msh30398bd1d7ed3b8p1b924fjsnddc67ade2aa7"
        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()

        if response['code'] == 200 and len(response['items']) != 0:
            return response['items'][0]['mid']
        else:
            return None

    def get_message(self, id):

        url = "https://temp-gmail.p.rapidapi.com/read"

        querystring = {"email": self.email, "message_id": id}

        headers = {
            "X-RapidAPI-Host": "temp-gmail.p.rapidapi.com",
            "X-RapidAPI-Key": "28d36f41b7msh30398bd1d7ed3b8p1b924fjsnddc67ade2aa7"
        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()

        # print(response['items']['body'])
        return response['items']['body']

    def waitForEmail(self):
        tries = 0
        while tries < 30:
            id = self.checkEmail()
            if id is not None:
                msg_content = self.get_message(id=id)
                l = LinkExtractor(msg_content)
                link = l.out_link
                return link
            tries += 1
            time.sleep(10)

        return False
