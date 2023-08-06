from localstack.utils.aws import aws_models
MdBYg=super
MdBYz=None
MdBYR=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  MdBYg(LambdaLayer,self).__init__(arn)
  self.cwd=MdBYz
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.MdBYR.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,MdBYR,env=MdBYz):
  MdBYg(RDSDatabase,self).__init__(MdBYR,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,MdBYR,env=MdBYz):
  MdBYg(RDSCluster,self).__init__(MdBYR,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,MdBYR,env=MdBYz):
  MdBYg(AppSyncAPI,self).__init__(MdBYR,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,MdBYR,env=MdBYz):
  MdBYg(AmplifyApp,self).__init__(MdBYR,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,MdBYR,env=MdBYz):
  MdBYg(ElastiCacheCluster,self).__init__(MdBYR,env=env)
class TransferServer(BaseComponent):
 def __init__(self,MdBYR,env=MdBYz):
  MdBYg(TransferServer,self).__init__(MdBYR,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,MdBYR,env=MdBYz):
  MdBYg(CloudFrontDistribution,self).__init__(MdBYR,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,MdBYR,env=MdBYz):
  MdBYg(CodeCommitRepository,self).__init__(MdBYR,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
