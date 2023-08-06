from localstack.utils.aws import aws_models
EAqsJ=super
EAqsM=None
EAqsc=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EAqsJ(LambdaLayer,self).__init__(arn)
  self.cwd=EAqsM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.EAqsc.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,EAqsc,env=EAqsM):
  EAqsJ(RDSDatabase,self).__init__(EAqsc,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,EAqsc,env=EAqsM):
  EAqsJ(RDSCluster,self).__init__(EAqsc,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,EAqsc,env=EAqsM):
  EAqsJ(AppSyncAPI,self).__init__(EAqsc,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,EAqsc,env=EAqsM):
  EAqsJ(AmplifyApp,self).__init__(EAqsc,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,EAqsc,env=EAqsM):
  EAqsJ(ElastiCacheCluster,self).__init__(EAqsc,env=env)
class TransferServer(BaseComponent):
 def __init__(self,EAqsc,env=EAqsM):
  EAqsJ(TransferServer,self).__init__(EAqsc,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,EAqsc,env=EAqsM):
  EAqsJ(CloudFrontDistribution,self).__init__(EAqsc,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,EAqsc,env=EAqsM):
  EAqsJ(CodeCommitRepository,self).__init__(EAqsc,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
