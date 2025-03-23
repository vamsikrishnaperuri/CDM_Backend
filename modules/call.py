# This method deals with sending the messages

from gtts import gTTS
import boto3
import os
from twilio.rest import Client

def generateAudio(mytext):
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    name = "file1.mp3"
    myobj.save(name)
    # os.system(name)
    print("Audio Generated")
    return name

def sendToS3Instance(file, bucket_name="gvp-bucket"):
    

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="ap-south-1"
    )
    s3 = session.client('s3')
    s3.upload_file(file, bucket_name, file)
    audio_url_new = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file}, ExpiresIn=3600)
    print(audio_url_new)
    return audio_url_new

def call(text="Hello this is Harsha. Is this working"):
    _ = generateAudio(text)
    audio_url = sendToS3Instance(_)
    generateCall(audio_url, "")

def generateCall(audio_url, to_number="+919494517819"):
    print("Ready to call")
    

    client = Client(account_sid, auth_token)
    call = client.calls.create(
        url=audio_url,
        to="+919494517819",
        from_="+18788776649")
    print(call.sid)

call()