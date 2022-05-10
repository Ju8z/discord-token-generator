import requests
import time


class SmsSmsActivate:
    def get_code(self):
        response = requests.get('https://api.sms-activate.org/stubs/handler_api.php?api_key=' + self.phoneAPI + '&action=getStatus&id=' + self.id).text

        print(response)
        if 'STATUS_OK' not in response and self.retries < self.max_time * 2:
            print(f"{self.retries}here waiting")
            self.retries += 1
            time.sleep(30)
            return self.get_code()
        elif self.retries >= self.max_time * 2:
            return False
        else:
            return response.split(':')[1]

    def sent(self) -> None:
        requests.get('https://api.sms-activate.org/stubs/handler_api.php?api_key=' + self.phoneAPI + '&action=setStatus&status=1&id=' + self.id)

    def done(self) -> None:
        requests.get('https://api.sms-activate.org/stubs/handler_api.php?api_key=' + self.phoneAPI + '&action=setStatus&status=6&id=' + self.id)

    def banned(self) -> None:
        requests.get('https://api.sms-activate.org/stubs/handler_api.php?api_key=' + self.phoneAPI + '&action=setStatus&status=8&id=' + self.id)

    def waitforcode(self):
        self.sent()
        res = self.get_code()
        if res is not False:
            self.done()
            return res
        self.banned()
        return False

    def __init__(self, phoneAPI) -> None:
        self.max_time = 20
        self.retries = 0
        self.phoneAPI = phoneAPI
        response = requests.get(
            'https://api.sms-activate.org/stubs/handler_api.php?api_key=' + self.phoneAPI + '&action=getNumber&service=ds&ref=1715152&country=6').text
        if ":" not in response:
            Exception(response)
        print("1", response)
        self.id = response.split(':')[1]
        self.number = response.split(':')[2]
