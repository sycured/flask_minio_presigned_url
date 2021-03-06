from datetime import timedelta

import config as cfg

from flask import Flask, Response, request

from minio import Minio

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = cfg.flask_secret_key

client: Minio = Minio(endpoint=cfg.endpoint, access_key=cfg.access_key,
                      secret_key=cfg.secret_key, secure=cfg.ssl)


def bucket_exists(name: str) -> bool:
    return name in (i.name for i in client.list_buckets())


def file_exists(bucket: str, name: str) -> bool:
    return name in (i.object_name for i in
                    client.list_objects(bucket_name=bucket, prefix=name[:5]))


def return_code(http_code: int) -> Response:
    return app.response_class(status=http_code)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/download/<bucket>/<file>', methods=['GET'])
def download(bucket, file):
    if not (bucket_exists(bucket) and file_exists(bucket, file)):
        return return_code(404)
    return client.presigned_get_object(bucket_name=bucket,
                                       object_name=file,
                                       expires=timedelta(minutes=15))


@app.route('/upload', methods=['POST'])
def upload():
    content = request.get_json(force=True)
    bucket = content['bucket']
    file = content['file']
    if not bucket_exists(bucket):
        return return_code(404)
    return client.presigned_put_object(bucket_name=bucket,
                                       object_name=file,
                                       expires=timedelta(minutes=15))


if __name__ == '__main__':
    app.run(host=cfg.flask_host, port=cfg.flask_port)
