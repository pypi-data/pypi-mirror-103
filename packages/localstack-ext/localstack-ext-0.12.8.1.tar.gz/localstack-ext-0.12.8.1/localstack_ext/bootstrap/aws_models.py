from localstack.utils.aws import aws_models
qdeXm=super
qdeXj=None
qdeXa=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  qdeXm(LambdaLayer,self).__init__(arn)
  self.cwd=qdeXj
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.qdeXa.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,qdeXa,env=qdeXj):
  qdeXm(RDSDatabase,self).__init__(qdeXa,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,qdeXa,env=qdeXj):
  qdeXm(RDSCluster,self).__init__(qdeXa,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,qdeXa,env=qdeXj):
  qdeXm(AppSyncAPI,self).__init__(qdeXa,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,qdeXa,env=qdeXj):
  qdeXm(AmplifyApp,self).__init__(qdeXa,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,qdeXa,env=qdeXj):
  qdeXm(ElastiCacheCluster,self).__init__(qdeXa,env=env)
class TransferServer(BaseComponent):
 def __init__(self,qdeXa,env=qdeXj):
  qdeXm(TransferServer,self).__init__(qdeXa,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,qdeXa,env=qdeXj):
  qdeXm(CloudFrontDistribution,self).__init__(qdeXa,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,qdeXa,env=qdeXj):
  qdeXm(CodeCommitRepository,self).__init__(qdeXa,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
