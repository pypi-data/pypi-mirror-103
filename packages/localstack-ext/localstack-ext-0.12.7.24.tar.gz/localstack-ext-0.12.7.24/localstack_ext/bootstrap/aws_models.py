from localstack.utils.aws import aws_models
UvrTb=super
UvrTQ=None
UvrTo=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  UvrTb(LambdaLayer,self).__init__(arn)
  self.cwd=UvrTQ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.UvrTo.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,UvrTo,env=UvrTQ):
  UvrTb(RDSDatabase,self).__init__(UvrTo,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,UvrTo,env=UvrTQ):
  UvrTb(RDSCluster,self).__init__(UvrTo,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,UvrTo,env=UvrTQ):
  UvrTb(AppSyncAPI,self).__init__(UvrTo,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,UvrTo,env=UvrTQ):
  UvrTb(AmplifyApp,self).__init__(UvrTo,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,UvrTo,env=UvrTQ):
  UvrTb(ElastiCacheCluster,self).__init__(UvrTo,env=env)
class TransferServer(BaseComponent):
 def __init__(self,UvrTo,env=UvrTQ):
  UvrTb(TransferServer,self).__init__(UvrTo,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,UvrTo,env=UvrTQ):
  UvrTb(CloudFrontDistribution,self).__init__(UvrTo,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,UvrTo,env=UvrTQ):
  UvrTb(CodeCommitRepository,self).__init__(UvrTo,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
