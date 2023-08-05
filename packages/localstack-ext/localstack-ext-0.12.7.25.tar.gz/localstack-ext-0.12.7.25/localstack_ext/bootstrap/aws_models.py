from localstack.utils.aws import aws_models
bVlyq=super
bVlyj=None
bVlyW=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  bVlyq(LambdaLayer,self).__init__(arn)
  self.cwd=bVlyj
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.bVlyW.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,bVlyW,env=bVlyj):
  bVlyq(RDSDatabase,self).__init__(bVlyW,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,bVlyW,env=bVlyj):
  bVlyq(RDSCluster,self).__init__(bVlyW,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,bVlyW,env=bVlyj):
  bVlyq(AppSyncAPI,self).__init__(bVlyW,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,bVlyW,env=bVlyj):
  bVlyq(AmplifyApp,self).__init__(bVlyW,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,bVlyW,env=bVlyj):
  bVlyq(ElastiCacheCluster,self).__init__(bVlyW,env=env)
class TransferServer(BaseComponent):
 def __init__(self,bVlyW,env=bVlyj):
  bVlyq(TransferServer,self).__init__(bVlyW,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,bVlyW,env=bVlyj):
  bVlyq(CloudFrontDistribution,self).__init__(bVlyW,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,bVlyW,env=bVlyj):
  bVlyq(CodeCommitRepository,self).__init__(bVlyW,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
