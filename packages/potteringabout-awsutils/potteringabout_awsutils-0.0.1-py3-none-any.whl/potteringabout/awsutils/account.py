import boto3
import botocore

class Account:

  credentials = {}

  def assume_role(self, accountId, role):
    global credentials
    cred = "{}::{}".format(accountId, role)
    if cred not in self.credentials:
      try:
        sts_client = boto3.client('sts')
        assumed_role_object=sts_client.assume_role(
          RoleArn="arn:aws:iam::" + accountId + ":role/" + role,
          RoleSessionName=role + "-Session"
        )
      except botocore.exceptions.ClientError as error:
        try:
          if error.response["Error"]["Code"] == "AccessDenied":
            print("Access Denied to account[{}] and role [{}]".format(accountId, role))
        except:
          pass
        raise error

      self.credentials[cred]=assumed_role_object['Credentials']
    return self.credentials[cred]

  def resource(self, accountId, rtype, role):
    creds = self.assume_role(accountId=accountId, role=role)
    ec2_resource=boto3.resource(
      rtype,
      aws_access_key_id=creds['AccessKeyId'],
      aws_secret_access_key=creds['SecretAccessKey'],
      aws_session_token=creds['SessionToken']
    )
    return ec2_resource

  def client(self, accountId, rtype, role):
    creds = self.assume_role(accountId=accountId, role=role)
    client=boto3.client(
      rtype,
      aws_access_key_id=creds['AccessKeyId'],
      aws_secret_access_key=creds['SecretAccessKey'],
      aws_session_token=creds['SessionToken']
    )
    return client
