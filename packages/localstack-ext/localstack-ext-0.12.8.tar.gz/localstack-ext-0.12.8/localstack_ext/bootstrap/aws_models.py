from localstack.utils.aws import aws_models
YBtLF=super
YBtLu=None
YBtLi=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YBtLF(LambdaLayer,self).__init__(arn)
  self.cwd=YBtLu
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.YBtLi.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,YBtLi,env=YBtLu):
  YBtLF(RDSDatabase,self).__init__(YBtLi,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,YBtLi,env=YBtLu):
  YBtLF(RDSCluster,self).__init__(YBtLi,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,YBtLi,env=YBtLu):
  YBtLF(AppSyncAPI,self).__init__(YBtLi,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,YBtLi,env=YBtLu):
  YBtLF(AmplifyApp,self).__init__(YBtLi,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,YBtLi,env=YBtLu):
  YBtLF(ElastiCacheCluster,self).__init__(YBtLi,env=env)
class TransferServer(BaseComponent):
 def __init__(self,YBtLi,env=YBtLu):
  YBtLF(TransferServer,self).__init__(YBtLi,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,YBtLi,env=YBtLu):
  YBtLF(CloudFrontDistribution,self).__init__(YBtLi,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,YBtLi,env=YBtLu):
  YBtLF(CodeCommitRepository,self).__init__(YBtLi,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
