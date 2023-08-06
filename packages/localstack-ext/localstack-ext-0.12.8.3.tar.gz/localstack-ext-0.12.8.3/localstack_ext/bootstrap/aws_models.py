from localstack.utils.aws import aws_models
fTjMA=super
fTjMc=None
fTjMz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  fTjMA(LambdaLayer,self).__init__(arn)
  self.cwd=fTjMc
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.fTjMz.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,fTjMz,env=fTjMc):
  fTjMA(RDSDatabase,self).__init__(fTjMz,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,fTjMz,env=fTjMc):
  fTjMA(RDSCluster,self).__init__(fTjMz,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,fTjMz,env=fTjMc):
  fTjMA(AppSyncAPI,self).__init__(fTjMz,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,fTjMz,env=fTjMc):
  fTjMA(AmplifyApp,self).__init__(fTjMz,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,fTjMz,env=fTjMc):
  fTjMA(ElastiCacheCluster,self).__init__(fTjMz,env=env)
class TransferServer(BaseComponent):
 def __init__(self,fTjMz,env=fTjMc):
  fTjMA(TransferServer,self).__init__(fTjMz,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,fTjMz,env=fTjMc):
  fTjMA(CloudFrontDistribution,self).__init__(fTjMz,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,fTjMz,env=fTjMc):
  fTjMA(CodeCommitRepository,self).__init__(fTjMz,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
