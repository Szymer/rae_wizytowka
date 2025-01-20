from requests import post, Session



API_HOST = "https://url_systemu/api/v1/"


class CermemeoAPI:
    def __init__(self):
        self.session  =  Session()
        # self.session.headers.update('Content-Type: application/json')
        # self.session.auth = ('Token {auth_token}')


    def post(self, data):
        payload = data.json()
        # response = self.session.post(f"{API_HOST}", json = payload, timeout = 5)
        # return response.json()
        print(payload)
        return True