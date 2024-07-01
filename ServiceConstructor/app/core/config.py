from motor.motor_asyncio import AsyncIOMotorClient

class Settings:
    MONGO_URI: str = "mongodb://localhost:27017/"
    DB_NAME: str = "rules_db"

settings = Settings()

def get_database():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    return client[settings.DB_NAME]
