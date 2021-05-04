import json, logging, requests

from config import config as cfg
from urllib.parse import quote
from datetime import datetime

def check_status(success_code=200, silent=False):
    '''Checks response of API request for status code. If status code
    does not return the specified success_code, it throws an error.'''

    if not isinstance(success_code, list):
        success_codes = [success_code]
    else:
        success_codes = list(success_code)

    def decorator(api_call_function):

        def wrapper(*args, **kwargs):
            response = api_call_function(*args, **kwargs)
            if response.status_code in success_codes:
                if not silent:
                    logging.info("Called %s %s",
                          response.request.method, response.request.url)
            else:
                logging.info("Called %s %s",
                             response.request.method,
                             response.request.url)
                logging.error("ERROR: Status code = {0}"
                              .format(response.status_code))
                logging.error("Request body:")
                logging.error(response.request.body)
                logging.error("Response:")
                logging.error(json.dumps(response.text))
            return response

        return wrapper

    return decorator

class BaseClient(object):
  '''Client wrapper around the requests library. This class should be used
  or extended by other clients.'''

  def __init__(self, host, port, auth, base_url='/api'):
    if port:
        self.url = 'https://{}:{}'.format(host, port)
    else:
        self.url = 'https://{}'.format(host)
    self.auth = auth
    self.base_url = base_url

  def request(self, method, endpoint, **kwargs):
    '''Wrapper around requests, request that fills in url and auth
    information.'''
    session = requests.Session()
    session.auth = self.auth
    return session.request(
      method=method,
      url=self.url + self.base_url + endpoint,
      auth=self.auth,
      verify=False,
      **kwargs
    )

class Api:
    '''
    An interface to the API, uses a BaseClient object to handle all
    requests.
    '''
    def __init__(self,):
        auth = requests.auth.HTTPDigestAuth(cfg.USER, cfg.PW)
        self.client = BaseClient(host=cfg.HOST,
                                 port=cfg.PORT if hasattr(cfg,'PORT') else None,
                                 auth=auth)

    def check_connection(self):
        # Check connection
        pass

    @check_status(success_code=200)
    def todos(self):
        '''
        The todos method fetches the todos api endpoint
        '''
        return self.client.request('GET', '/todos')
    # Add other endpoints below