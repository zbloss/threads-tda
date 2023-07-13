import pydantic

class MongoSettings(pydantic.BaseModel):
    uri: str = "mongodb://127.0.0.1:27017"
    database: str = "threadsdb"
    collection: str = "threads"

    class Config:
        env_file = ".env"
        env_prefix = "MONGO_"
