from datetime import timedelta

from flask import Flask, request
from minio import Minio
from minio.error import ResponseError

import config as cfg

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = cfg.flask_secret_key

client = Minio(endpoint=cfg.endpoint, access_key=cfg.access_key,
               secret_key=cfg.secret_key, secure=cfg.ssl)


def bucket_exists(name):
    if name in [i.name for i in client.list_buckets()]:
        return True
    else:
        return False


def file_exists(bucket, name):
    if name in [i.object_name for i in
                client.list_objects(bucket_name=bucket, prefix=name[:5])]:
        return True
    else:
        return False


def return_code(http_code: int):
    return app.response_class(status=http_code)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/download/<bucket>/<file>', methods=['GET'])
def download(bucket, file):
    if not (bucket_exists(bucket) and file_exists(bucket, file)):
        return return_code(404)
    try:
        return client.presigned_get_object(bucket_name=bucket,
                                           object_name=file,
                                           expires=timedelta(minutes=15))
    except ResponseError as err:
        print(err)
        return return_code(500)


@app.route('/upload', methods=['POST'])
def upload():
    content = request.get_json(force=True)
    bucket = content['bucket']
    file = content['file']
    if not bucket_exists(bucket):
        return return_code(404)
    try:
        return client.presigned_put_object(bucket_name=bucket,
                                           object_name=file,
                                           expires=timedelta(minutes=15))
    except ResponseError as err:
        print(err)
        return return_code(500)


if __name__ == '__main__':
    app.run(host=cfg.flask_host, port=cfg.flask_port)
