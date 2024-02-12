import requests
import json
import jwt
import os
from uuid import uuid4
import boto3
from datetime import datetime, timedelta

from vendor_management_system.settings import PUBLIC_KEY, DB
from main_app.constants import AWS_BUCKET

def generate_token(user_dict):

	token = jwt.encode({"exp": datetime.now() + timedelta(days=7) , **user_dict}, PUBLIC_KEY, algorithm="HS256")
	
	return token

def verify_token(token):
	
	decoded_token = {}	
	if token:
		try:
			auth_token  = token.split(" ")[-1] if "Bearer" in token else token

			decoded_token = jwt.decode(auth_token, PUBLIC_KEY, algorithms="HS256", options={"verify_exp": False})

		except Exception as e:
			return False, {}

		user_doc = DB.users.find_one({"id": decoded_token["id"]}) or {}
		if not user_doc.get('token_valid'):
			return False, {}
	
	else:
		return False, {}
	
	return True, decoded_token

def wati_endpoint():
	wati_api_endpoint = f"https://live-server-106300.wati.io/api/v1/sendTemplateMessage?whatsappNumber="
	wati_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzNGJmYzIyNS05MmY4LTQzNTMtODA3Yy02ODU4ZjY4OGU2MGYiLCJ1bmlxdWVfbmFtZSI6Im5hZ2VuZHJhLmt1bWFyQHdjdWJlaW5kaWEuY29tIiwibmFtZWlkIjoibmFnZW5kcmEua3VtYXJAd2N1YmVpbmRpYS5jb20iLCJlbWFpbCI6Im5hZ2VuZHJhLmt1bWFyQHdjdWJlaW5kaWEuY29tIiwiYXV0aF90aW1lIjoiMDUvMjIvMjAyMyAxMDowMTo0NyIsImRiX25hbWUiOiIxMDYzMDAiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.4FMJHzSytSfFGtGWlSWL15vktZDZmK8MdIiaMDjWVrM"

	headers = {
					"Content-Type": "application/json",
					"Authorization": f"Bearer {wati_api_key}"
				}
	return wati_api_endpoint, headers


def wati_template(mobile, template,parameters):
	wati_api_endpoint,headers = wati_endpoint()
	wati_api_endpoint= wati_api_endpoint + "91" + mobile
	payload = {
		"template_name": template,
		"broadcast_name": template,
		"parameters": parameters
	}
	response = requests.post(wati_api_endpoint, headers=headers, data=json.dumps(payload))

def handle_uploaded_file(file, filename, folder):

	if not os.path.exists('upload/'):
		os.mkdir('upload/')

	file_path = f'{folder}/{filename}' if folder else filename

	file_name = file.name
	file_content = file.read()
	file_extension = os.path.splitext(file_name)[1].lower()
	filename = filename + file_extension
	with open('upload/' + filename, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)
	s3_client = boto3.client('s3',
		aws_access_key_id='AKIA47QGJQBUYN6LWHMM',
		aws_secret_access_key='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',
		region_name="eu-north-1"
	)
	s3_client.upload_file('upload/'+ filename, AWS_BUCKET, file_path)
	return file_name, file_extension, filename,file_content

def generate_url(key):
	s3_client = boto3.client('s3',
		aws_access_key_id='AKIA47QGJQBUYN6LWHMM',
		aws_secret_access_key='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',
		region_name="ap-south-1"
	)
	if "." in key:
		key = key.split('.')[0]
	response = s3_client.generate_presigned_url('get_object', Params={'Bucket': AWS_BUCKET, 'Key': key}, ExpiresIn=3600)
	return response