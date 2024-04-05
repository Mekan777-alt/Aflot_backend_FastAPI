import motor.motor_asyncio


DATABASE_URL = "mongodb://173.20.0.2:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)

db = client['aflot_backend']
