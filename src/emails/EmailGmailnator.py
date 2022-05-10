import requests
import time
from html.parser import HTMLParser


class MyParser(HTMLParser):
    def __init__(self, output_list=None):
        HTMLParser.__init__(self)
        if output_list is None:
            self.output_list = []
        else:
            self.output_list = output_list

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.output_list.append(dict(attrs).get('href'))


class EmailGmailnator():

    def __init__(self, api) -> None:

        self.email_api = api
        self.email = ""

        response = requests.post('https://gmailnator.p.rapidapi.com/generate-email', headers={
            "content-type": "application/json",
            "X-RapidAPI-Host": "gmailnator.p.rapidapi.com",
            "X-RapidAPI-Key": self.email_api
        },
                                 json={'options': ["1"]})

        print(response)

        if response.status_code == 200:
            self.email = response.json()['email']
        else:
            Exception("Couldn't get E-Mail...")

    def checkEmail(self):
        url = "https://gmailnator.p.rapidapi.com/inbox"

        payload = {
            "email": self.email,
            "limit": 1
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Host": "gmailnator.p.rapidapi.com",
            "X-RapidAPI-Key": self.email_api
        }

        response = requests.request("POST", url, json=payload, headers=headers).json()

        if len(response) != 0:
            return response[0]['id']
        else:
            return None

    def getMessage(self, id):
        url = "https://gmailnator.p.rapidapi.com/messageid"

        querystring = {"id": id}

        headers = {
            "X-RapidAPI-Host": "gmailnator.p.rapidapi.com",
            "X-RapidAPI-Key": "28d36f41b7msh30398bd1d7ed3b8p1b924fjsnddc67ade2aa7"
        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()

        return response['content']

    def waitForEmail(self):
        tries = 0
        while tries < 30:
            time.sleep(10)
            id = self.checkEmail()
            if id is not None:
                msg_content = self.getMessage(id=id)
                p = MyParser()
                ouput_links = p.feed(msg_content)
                return ouput_links[1]
            tries += 1
        return False
