import boto3
from datetime import date, datetime, timedelta,timezone
from datetime import date
import csv
import os


roles = ["arn:aws:iam::070992492667:role/ROLE-ADM", "arn:aws:iam::070992492667:role/ROLE-ADM", "arn:aws:iam::070992492667:role/ROLE-ADM"]

def accesskey_150(session,writer,account):
 usr_details = {}
 client = session.client('iam')
 list_user = client.list_users()
 for user_name in list_user['Users']:
  describe_accesskey = client.list_access_keys(UserName=user_name['UserName'])
  for accesskey_createddate in describe_accesskey['AccessKeyMetadata']:
   current_date = datetime.now(timezone.utc)
   age = (current_date-accesskey_createddate['CreateDate']).days
   if age >= 10:
    usr_details['Account_ID'] = account[4]
    usr_details['USERNAME'] = accesskey_createddate['UserName']
    usr_details['CREATED_DAYS_AGO'] = age
    usr_details['CURRENT_ACCESSKEY'] = accesskey_createddate['AccessKeyId']
    writer.writerow(usr_details)


def main():
 sts_client = boto3.client("sts")
 fieldnames = ["Account_ID","USERNAME","CREATED_DAYS_AGO","CURRENT_ACCESSKEY"]
 file_name = "usr_details.csv"
 with open (file_name,"w",newline='') as csv_file:
  writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
  writer.writeheader()
  for role_arn in roles:
      sts_response = sts_client.assume_role(RoleArn = role_arn,RoleSessionName = "awstoaws")
      session = boto3.Session(
      aws_access_key_id = (sts_response["Credentials"]["AccessKeyId"]),
      aws_secret_access_key = (sts_response["Credentials"]["SecretAccessKey"]),
      aws_session_token = (sts_response["Credentials"]["SessionToken"]))
      account = role_arn.split(":")
      accesskey_150(session,writer,account)

main()