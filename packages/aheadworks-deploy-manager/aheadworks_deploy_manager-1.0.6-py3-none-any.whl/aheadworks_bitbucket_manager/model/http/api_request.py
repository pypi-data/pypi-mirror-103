import requests


class ApiRequest:
    """request class for web api"""

    def __init__(self, config):
        self.config = config
        self.url = self.config.url
        self.auth_headers = {'Authorization': "Bearer {}".format(self.config.token), }

    def get(self, location, params=None, headers=None):
        """ get request to bitbucket api
        :param location: url location path
        :param params: request query params
        :param headers: http headers
        :return: text of response
        """
        if headers is None:
            headers = self.auth_headers
        url = f'{self.url}{location}'
        r = requests.get(url=url, params=params, headers=headers)
        return r.text

    def post(self, location, headers=None, data=None, json=None, files=None):
        """
        :param location: location: url location path
        :param headers:  http headers
        :param data: request data
        :param json: json in request body
        :param files: dictionary with opened files
        :return: response
        """
        url = f'{self.url}{location}'
        r = requests.post(url, headers=headers, data=data, json=json, files=files)
        return r

    def put(self, location, headers=None, data=None, json=None):
        """
        :param location: url location path
        :param headers: http headers
        :param data: request data
        :param json: json in request body
        :return: response
        """
        url = f'{self.url}{location}'
        r = requests.post(url, headers=headers, data=data, json=json)
        return r

    def delete(self, location, headers=None):
        """
        :param location:  url location path
        :param headers: http headers
        :return: status code
        """
        url = f'{self.url}{location}'
        if headers is None:
            headers = self.auth_headers
        r = requests.delete(url, headers=headers)
        return r.status_code
