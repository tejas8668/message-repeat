from os import getenv
from pymongo import MongoClient

class Config(object):
    API_HASH = getenv("API_HASH")
    API_ID = int(getenv("API_ID", 0))
    AS_COPY = True if getenv("AS_COPY", "True") == "True" else False
    BOT_TOKEN = getenv("BOT_TOKEN", "")
    MONGO_URI = getenv("MONGO_URI")
    MONGO_DB = getenv("MONGO_DB")
    MESSAGES_COLLECTION = getenv("MESSAGES_COLLECTION")
    CONFIG_COLLECTION = getenv("CONFIG_COLLECTION")
    MESSAGE_REPEAT_TIME = int(getenv("MESSAGE_REPEAT_TIME", 3600))  # 1 hour
    MESSAGES_PER_INTERVAL = int(getenv("MESSAGES_PER_INTERVAL", 4))
    CHANNELS = {
    "group1": {
        "sources": ["-1002487065354"],
        "destinations": ["-1002464896968"]
    },
    "group2": {
        "sources": ["-1002398034096"],
        "destinations": ["-1002176533426"]
    }
}

    # मोंगो डीबी क्लाइंट बनाएं
    client = MongoClient(MONGO_URI)

    # डेटाबेस बनाएं
    db = client[MONGO_DB]

    # COLLECTION बनाएं
    messages_collection = db[MESSAGES_COLLECTION]
    config_collection = db[CONFIG_COLLECTION]

    #dgYiLNTVFTseZXWp
    #mongodb+srv://tejaschavan1110:dgYiLNTVFTseZXWp@cluster0.d9ifv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
