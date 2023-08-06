import requests
import os
import stat
import json
import getpass
#for making the auth, maybe make its own folder
from .logger import logging as log
from cachetools import TTLCache
try:
    from dmc import gettoken
except ImportError:
    log.warning('Cannot use DMC if centrify.dmc is not installed')
    pass
class getConfigPath:
    def __init__(self, fName="config.json"):
        if os.name == "posix":        
            self.path = os.path.join(os.path.expanduser('~'), fName)
        elif os.name == "nt":
            self.path = os.path.join(os.environ['USERPROFILE'], fName)
    @property
    def real_path(self):
        return self.path
class f_check:
    def __init__(self):
        with open(getConfigPath().real_path, 'r') as json_file:
            self.loaded = json.load(json_file)
            self.dump = json.dumps(self.loaded)
            self.loads = json.loads(self.dump)
class auth:
    def __init__(self):
        log.info('Starting Auth process...')
        if f_check().loaded['auth'] == 'DMC':
            log.info('Setting auth headers for DMC......')
            self._headers = {}
            self._headers["X-CENTRIFY-NATIVE-CLIENT"] = 'true'
            self._headers['X-CFY-SRC' ]= 'python'
            try:
                self._headers['Authorization']  = 'Bearer {0}'.format(gettoken(f_check().loaded['scope']))
            except KeyError:
                log.error('Issue with getting DMC scope')
                raise Exception
        elif f_check().loaded['auth'] == 'OAUTH': 
            if 'client_secret' not in f_check().loaded['body']: 
                log.warning("Password Not Saved, Please provide password of Oauth Account or save PW")
                self._pw = getpass.getpass("Please provide Password for Oauth account: {0}\n".format(f_check().loaded['body']['client_id']))
                # Use the auth class to call that instead of this shit
                self.json_d = json.dumps(f_check().loaded)
                self.update = json.loads(self.json_d)
                ########
                self.update['body']['client_secret'] = self._pw
            self._rheaders = {}
            self._rheaders['X-CENTRIFY-NATIVE-CLIENT'] = 'true'
            self._rheaders['Content-Type'] = 'application/x-www-form-urlencoded'
            self._rbody = self.update['body']
            log.info('Oauth URL of app is: {}'.format(self.update['urls']['app_url'])) 
            log.info('Oauth token request Headers are: {}'.format(self._rheaders)) 
            try:
                log.info('Setting auth headers for OAUTH......')
                req = requests.post(url= self.update['urls']['app_url'], headers= self._rheaders, data= self._rbody).json()
            except:
                log.error("Issue getting token")
                log.error("Response: {0}".format(json.dumps(req)))
                raise Exception
            self._headers = {}
            #FIGURE OUT WHY THE FUCK THIS BREAKS THE ENTIRE THING
            #try:
            self._headers["Authorization"] = "Bearer {access_token}".format(**req)
            #except KeyError:
            #    print("wrong PW more than likely")
            #    log.error("Issue setting the headers")
            self._headers["X-CENTRIFY-NATIVE-CLIENT"] = 'true'
        else:
            log.error('An Internal error occurred. Please check the congif file in current users working dir.')
    @property
    def headers(self):
        return self._headers
class Cache:
    def __init__(self):
        self._cache = TTLCache(maxsize=10, ttl=360)
        self._cache['header'] = auth().headers
    @property
    def cached(self):
        return self._cache

#put in mem cache here to instantiate it and have it be called from this file

