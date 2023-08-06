import boto3, json, logging

def removeNone(data):
    return { k:v for k, v in data.items() if v is not None }

class DigioAdapter:
  def __init__(self, stackName= 'villa-wallet-dev', user=None, pw=None, region='ap-southeast-1'):
    self.lambdaClient = boto3.client(
        'lambda',
        aws_access_key_id = user,
        aws_secret_access_key = pw ,
        region_name = region
      )
    self.stackName = stackName

  def invoke(self, functionName, data):
    response = self.lambdaClient.invoke(
        FunctionName = functionName,
        InvocationType = 'RequestResponse',
        Payload=json.dumps(data)
    )
    return json.loads(response['Payload'].read())

  def authen(self, data:dict):
    functionName = f'{self.stackName}-lambda-auth'
    return self.invoke(functionName = functionName, data=data)

  def encode(self, data:dict):
    functionName = f'{self.stackName}-lambda-encode'
    return self.invoke(functionName = functionName, data=data)

  def tran(self, data:dict):
    functionName = f'{self.stackName}-lambda-tran'
    return self.invoke(functionName = functionName, data=data)

  def redeem(self, data:dict):
    functionName = f'{self.stackName}-lambda-redeem'
    return self.invoke(functionName = functionName, data=data)

  def cancelTr(self, data:dict):
    functionName = f'{self.stackName}-lambda-cancel-tr'
    return self.invoke(functionName = functionName, data=data)

  def void(self, data:dict):
    functionName = f'{self.stackName}-lambda-void'
    return self.invoke(functionName = functionName, data=data)

  def topup(self, data:dict):
    functionName = f'{self.stackName}-lambda-topup'
    return self.invoke(functionName = functionName, data=data)

  def rtp(self, data:dict):
    functionName = f'{self.stackName}-lambda-rtp'
    return self.invoke(functionName = functionName, data=data)


