import sys
lNsdo=object
lNsdp=staticmethod
lNsdY=False
lNsdb=Exception
lNsdX=None
lNsdF=input
lNsdP=list
import json
import logging
import getpass
from localstack.config import CONFIG_FILE_PATH,load_config_file
from localstack.constants import API_ENDPOINT
from localstack.utils.common import to_str,safe_requests,save_file,load_file
LOG=logging.getLogger(__name__)
class AuthProvider(lNsdo):
 @lNsdp
 def name():
  raise
 def get_or_create_token(self,username,password,headers):
  pass
 def get_user_for_token(self,token):
  pass
 @lNsdp
 def providers():
  return{c.name():c for c in AuthProvider.__subclasses__()}
 @lNsdp
 def get(provider,raise_error=lNsdY):
  provider_class=AuthProvider.providers().get(provider)
  if not provider_class:
   msg='Unable to find auth provider class "%s"'%provider
   LOG.warning(msg)
   if raise_error:
    raise lNsdb(msg)
   return lNsdX
  return provider_class()
class AuthProviderInternal(AuthProvider):
 @lNsdp
 def name():
  return 'internal'
 def get_or_create_token(self,username,password,headers):
  data={'username':username,'password':password}
  response=safe_requests.post('%s/user/signin'%API_ENDPOINT,json.dumps(data),headers=headers)
  if response.status_code>=400:
   return
  try:
   result=json.loads(to_str(response.content or '{}'))
   return result['token']
  except lNsdb:
   pass
 def read_credentials(self,username):
  print('Please provide your login credentials below')
  if not username:
   sys.stdout.write('Username: ')
   sys.stdout.flush()
   username=lNsdF()
  password=getpass.getpass()
  return username,password,{}
 def get_user_for_token(self,token):
  raise lNsdb('Not implemented')
def login(provider,username=lNsdX):
 auth_provider=AuthProvider.get(provider)
 if not auth_provider:
  providers=lNsdP(AuthProvider.providers().keys())
  raise lNsdb('Unknown provider "%s", should be one of %s'%(provider,providers))
 username,password,headers=auth_provider.read_credentials(username)
 print('Verifying credentials ... (this may take a few moments)')
 token=auth_provider.get_or_create_token(username,password,headers)
 if not token:
  raise lNsdb('Unable to verify login credentials - please try again')
 configs=load_config_file()
 configs['login']={'provider':provider,'username':username,'token':token}
 save_file(CONFIG_FILE_PATH,json.dumps(configs))
def logout():
 configs=json_loads(load_file(CONFIG_FILE_PATH,default='{}'))
 configs['login']={}
 save_file(CONFIG_FILE_PATH,json.dumps(configs))
def json_loads(s):
 return json.loads(to_str(s))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
