import os

import pydantic
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class MongoSettings(pydantic.BaseModel):
    username: str = None
    password: str = None
    host: str = "127.0.0.1"
    port: str = "27017"
    database: str = "threadsdb"

    @property
    def uri(self) -> str:
        username_password = None
        if self.username and self.password:
            username_password = f"{username}:{password}@"
        uri: str = f"mongodb://{username_password}{self.host}:{self.port}"
        return uri


username = os.environ.get("MONGODB_USERNAME")
password = os.environ.get("MONGODB_PASSWORD")
host = os.environ.get("MONGODB_HOST_URL")
port = os.environ.get("MONGODB_HOST_PORT")
database = os.environ.get("MONGODB_DATABASE")

env_settings = {}
if username:
    env_settings["username"] = username

if password:
    env_settings["password"] = password

if host:
    env_settings["host"] = host

if port:
    env_settings["port"] = port

if database:
    env_settings["database"] = database

default_settings = MongoSettings(**env_settings)
