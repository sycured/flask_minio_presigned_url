from distutils.util import strtobool
from os import getenv
from secrets import token_urlsafe

flask_host: str = getenv(key='FLASK_HOST', default='127.0.0.1')
flask_port: int = getenv(key='FLASK_PORT', default=3000)
flask_secret_key: str = getenv(key='FLASK_SECRET_KEY',
                               default=str(token_urlsafe(32)))

access_key: str = getenv(key='MINIO_ACCESS_KEY', default=None)
endpoint: str = getenv(key='MINIO_ENDPOINT', default=None)
secret_key: str = getenv(key='MINIO_SECRET_KEY', default=None)
ssl: bool = strtobool(getenv(key='MINIO_SSL', default=True))