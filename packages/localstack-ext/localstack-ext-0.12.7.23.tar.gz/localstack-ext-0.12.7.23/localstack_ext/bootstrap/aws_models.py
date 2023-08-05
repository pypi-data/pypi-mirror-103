from localstack.utils.aws import aws_models
VctzM=super
VctzY=None
Vctze=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  VctzM(LambdaLayer,self).__init__(arn)
  self.cwd=VctzY
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Vctze.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Vctze,env=VctzY):
  VctzM(RDSDatabase,self).__init__(Vctze,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Vctze,env=VctzY):
  VctzM(RDSCluster,self).__init__(Vctze,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Vctze,env=VctzY):
  VctzM(AppSyncAPI,self).__init__(Vctze,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Vctze,env=VctzY):
  VctzM(AmplifyApp,self).__init__(Vctze,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Vctze,env=VctzY):
  VctzM(ElastiCacheCluster,self).__init__(Vctze,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Vctze,env=VctzY):
  VctzM(TransferServer,self).__init__(Vctze,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Vctze,env=VctzY):
  VctzM(CloudFrontDistribution,self).__init__(Vctze,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Vctze,env=VctzY):
  VctzM(CodeCommitRepository,self).__init__(Vctze,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
