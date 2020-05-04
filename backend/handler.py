import json
from flask import Flask, jsonify, request, redirect, make_response
import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
import random
import string
from boto.s3.connection import S3Connection

s3_client = boto3.client('s3')
app=Flask(__name__)
ctr=0
buck_name=''
response1=''
def lambda_handler(event, context):
    namee=bucket_name(buck_name)
    countObject()
    deleteAll()
    response1 = s3_client.create_bucket(
    ACL='public',
    Bucket=namee,
    CreateBucketConfiguration={
        'LocationConstraint': 'ap-south-1'
    })

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        upload_path=''.join(namee)
        s3_client.upload_file(upload_path,bucket, key)


    def bucket_name(user_input):
        N = 7
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N)) 
        newName = user_input+str(res)
        return newName 
    
    @app.route('/deleteAll', methods='[POST]')
    def deleteAll():
        s3 = boto3.resource('s3')
        bucket=s3.Bucket(buck_name)
        if "No Item to delete" in bucket.objects.all().delete():
            return make_response(jsonify("Msg: You already have no pics dude"), 411)
        else:
            return make_response(jsonify("Msg: Successfully deleted all your pics"), 200)

    @app.route('/countObject', methods='[GET]')
    def countObject():
        conn = S3Connection('access-key','secret-access-key')
        bucket = conn.get_bucket('bucket')
        for key in bucket.list():
            if str(key.name)[-3] == "png" | str(key.name)[-3] == "bmp" | str(key.name)[-3] == "jpg" | str(key.name)[-3] == "gif":
                ctr=ctr+1;    
        if ctr == 0:
            return make_response(jsonify("Msg: Your bucket is empty dude"), 200)
        else:
            return make_response(jsonify("Msg: Total no of objects are "+ctr), 200)

    response = {
        "statusCode": 200,
        "body": json.dumps(response1)
        }
    return response