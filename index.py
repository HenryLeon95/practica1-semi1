from flask import Flask, request, jsonify, Response
from time import time
import hashlib
import uuid
import base64
import boto3
import db_creds
import pymysql
import creds
import json


app = Flask (__name__)
db_config = db_creds.db_creds()
aws = creds
app.config['JSON_AS_ASCII'] = False

#db config
user = 'admin'
password = 'admin_mysql'
host = 'mysqldb.cahzfivbuo9y.us-east-2.rds.amazonaws.com'
database = 'practica1'
db = pymysql.connect(host=host, user=user, password=password, database=database)


@app.route('/api')
def main():
    print("Hola")
    return "Hello World!"


@app.route('/api/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    username = request_data['username']
    name = request_data['name']
    password = request_data['password']
    foto = request_data['foto']
    extension = request_data['extension']
    image = request_data['image']
    status = "..."


    if(foto != "vacio"):
        filename = 'Fotos_Perfil/' + image + str(uuid.uuid1()) + "." + extension #uuid() genera un id unico para el archivo en s3
    else:
        filename = 'Fotos_Perfil/default.jpg'  

    try:
        print("Intentando insertar en base de datos")

        cursor = db.cursor()
        cursor.execute("Insert into users (usuario, nombre, password, foto) VALUES (%s, %s, %s, %s)", (username, name, password, filename))
        db.commit()

        try:
            print("Intentando insertar en S3")
            if(foto != "vacio"):
                bytes = base64.b64decode(foto)
                print(filename)
                client = boto3.client(
                    's3',
                    region_name=aws.s3_creds.region_name,
                    aws_access_key_id=aws.s3_creds.aws_access_key_id,
                    aws_secret_access_key=aws.s3_creds.aws_secret_access_key
                )

                client.put_object(
                    ACL='public-read',
                    Body=bytes,
                    Bucket= "practica1-g18-imagenes",
                    Key=filename,
                    ContentType= "image"
                )
            status = 'User Created Syccessfully'
        except:
            status = 'ERROR! S3.'
    except:
        status = 'ERROR! This user is already registered.'
        
    return jsonify({'result': status})


@app.route("/api/login", methods=["POST"])
def login():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    status = "..."
    try:
        cursor = db.cursor()
        cursor.execute("Select * from users where usuario = %s and password = %s ;", (username, password))
        # cursor.execute("Select * from users;")
        fils = cursor.fetchall()
        
        db.commit()
        # db.close()
        return jsonify({'result': fils[0]})

    except:
        status = 'ERROR! This user is not registered.'

    return jsonify({'result': status})


@app.route("/tarea3-201503577", methods=["POST"])
def get_labels():
    request_data = request.get_json()
    #Asumiremos que solo vendra una imagen
    image = request_data['image']
    accessKeyId= "AKIAUFAWXK2WWLCNXOP2"
    secretAccessKey= "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" 
    region= 'us-east-2'

    rek = boto3.client(
        'rekognition',
        region_name=region,
        aws_access_key_id=accessKeyId,
        aws_secret_access_key=secretAccessKey)

    response = rek.detect_labels(
        Image={
            'Bytes': base64.b64decode(image)
        }, 
        MaxLabels= 234
    )

    print("Labels detected | Percentage")
    for label in response['Labels']:
        print('{} | {}%'.format(label['Name'], label['Confidence']))

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)