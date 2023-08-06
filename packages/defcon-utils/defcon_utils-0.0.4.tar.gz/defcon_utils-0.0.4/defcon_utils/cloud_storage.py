import requests
import re
import json
import boto3
import os
import uuid
from botocore.client import Config
from enum import Enum

class S3: 
    class ACL(Enum): 
        PRIVATE = "private" # "Owner gets FULL_CONTROL. No one else has access rights."
        PUBLIC_READ = "public-read" # "Owner gets FULL_CONTROL. The AllUsers group gets READ access."
        PUBLIC_READ_WRITE = "public-read-write" # "Owner gets FULL_CONTROL. The AllUsers group gets READ and WRITE access. Granting this on a bucket is generally not recommended."
        AWS_EXEC_READ = "aws-exec-read" # "Owner gets FULL_CONTROL. Amazon EC2 gets READ access to GET an Amazon Machine Image (AMI) bundle from Amazon S3."    
        AUTH_READ = "authenticated-read" # "Owner gets FULL_CONTROL. The AuthenticatedUsers group gets READ access."
        OWNER_READ = "bucket-owner-read" # "Object owner gets FULL_CONTROL. Bucket owner gets READ access. If you specify this canned ACL when creating a bucket, Amazon S3 ignores it."
        OWNER_FULL_CONTROL = "bucket-owner-full-control" # "Both the object owner and the bucket owner get FULL_CONTROL over the object. If you specify this canned ACL when creating a bucket, Amazon S3 ignores it."
        LOG_DELIVERY_WRITE = "log-delivery-write" # "The LogDelivery group gets WRITE and READ_ACP permissions on the bucket."
        
        
    def s3_client(self):
        return boto3.client('s3', region_name=self.BUCKET_REGION,
                            config=Config(s3={'addressing_style': 'path'}),
                            aws_access_key_id=self.PUBLIC_KEY,
                            aws_secret_access_key=self.SECRET_KEY)


    def s3_resource(self):
        return boto3.resource('s3', region_name=self.BUCKET_REGION,
                            aws_access_key_id=self.PUBLIC_KEY,
                            aws_secret_access_key=self.SECRET_KEY)
    
    def __init__(self, aws_public_key, aws_secret_key, bucket_name, bucket_region): 
        self.PUBLIC_KEY = aws_public_key
        self.SECRET_KEY = aws_secret_key
        self.BUCKET_REGION = bucket_region
        self.BUCKET_NAME = bucket_name

    def get_presigned_url_and_fields(self, folder, file_name, acl=None, replace_name_with_uuid=True, expiry_time=300):
        """

        expiry_time: The number of seconds the presigned post is valid
            for.
        """
        if not acl: 
            acl = self.ACL.PRIVATE
        if not isinstance(acl, self.ACL): 
            raise Exception('Invalid data provided for acl. Should be an instance of S3.ACL')
        if replace_name_with_uuid:
            extension = file_name.split(".")[-1]
            key = "{}/{}.{}".format(folder, uuid.uuid4(), extension)
        else:
            key = "{}/{}".format(folder, file_name)
        response = self.s3_client().generate_presigned_post(
            Bucket=self.BUCKET_NAME,
            Key=key,
            ExpiresIn=expiry_time,
            Fields={"acl": acl.value},
            Conditions=[
                {"acl": acl.value}
            ]
        )
        return response['url'], response['fields']
    
    def generate_view_only_presigned_url(self, object_path, expiration=15*60):
        """
        :param bucket: Type: String Name of the bucket
        :param object_path: Type: String Complete path of the object in S3
        :param expiration: Type: Int Url validity in seconds
        :return: Type: String The url to access resource
        """
        response = self.s3_client().generate_presigned_url('get_object',
                                                    Params={'Bucket': self.BUCKET_NAME,
                                                            'Key': object_path},
                                                    ExpiresIn=expiration)
        return response


    def upload_file_object(self, path, file_object, **kwargs):
        self.s3_client().upload_fileobj(file_object, self.BUCKET_NAME, path, ExtraArgs=kwargs)
        return True


    def upload_object(self, data, path):
        obj = self.s3_resource().Object(self.BUCKET_NAME, path)
        obj.put(Body=data)

        return True



def upload_data_to_dropbox(dropbox_token, file_name, file_data):
    '''Upload file to dropbox

            Args:
                file_name (str): File name with path on dropbox. (Should start with /)
                file_data (str): Data to upload to dropbox.
            Returns:
                str: Shared url for download.
            '''

    TOKEN = dropbox_token
    DROPBOX_UPLOAD_ARGS = {
        'path': None,
        'mode': 'overwrite',
        'autorename': True,
        'strict_conflict': True
    }
    DROPBOX_UPLOAD_URL = 'https://content.dropboxapi.com/2/files/upload'

    DROPBOX_SHARE_DATA = {
        'path': None,
        'settings': {
            'requested_visibility': 'public'
        }
    }
    DROPBOX_SHARE_URL = 'https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings'

    DROPBOX_DELETE_DATA = {
        'path': None
    }
    DROPBOX_DELETE_URL = 'https://api.dropboxapi.com/2/files/delete_v2'


    dropbox_path = file_name
    DROPBOX_UPLOAD_ARGS['path'] = dropbox_path
    DROPBOX_SHARE_DATA['path'] = dropbox_path
    DROPBOX_DELETE_DATA['path'] = dropbox_path

    # Try to delete the file before upload
    # It's possible to overwrite but this way is cleaner
    headers = {'Authorization': 'Bearer ' + TOKEN,
               'Content-Type': 'application/json'}

    requests.post(DROPBOX_DELETE_URL, data=json.dumps(DROPBOX_DELETE_DATA), headers=headers)

    headers = {'Authorization': 'Bearer ' + TOKEN,
               'Dropbox-API-Arg': json.dumps(DROPBOX_UPLOAD_ARGS),
               'Content-Type': 'application/octet-stream'}

    # Upload the file
    r = requests.post(DROPBOX_UPLOAD_URL, data=file_data, headers=headers)

    if r.status_code != requests.codes.ok:
        print("Failed: upload file to Dropbox: {errcode}".format(errcode=r.status_code))
        return None

    headers = {'Authorization': 'Bearer ' + TOKEN,
               'Content-Type': 'application/json'}

    # Share and return downloadable url
    r = requests.post(DROPBOX_SHARE_URL, data=json.dumps(DROPBOX_SHARE_DATA), headers=headers)

    if r.status_code != requests.codes.ok:
        print("Failed: get share link from Dropbox {errcode}".format(errcode=r.status_code))
        return None

    # Replace the '0' at the end of the url with '1' for direct download
    return re.sub('dl=.*', 'raw=1', r.json()['url'])
