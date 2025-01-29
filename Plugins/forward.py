import asyncio
import random
from pyrogram import filters
from bot import channelforward
from config import Config
from pymongo import MongoClient

# MongoDB क्लाइंट बनाएं
client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB]
messages_collection = db["messages"]

# Function to store messages
async def store_messages():
    for group, channels in Config.CHANNELS.items():
        MESSAGE_STORAGE[group] = {}
        for source in channels["sources"]:
            MESSAGE_STORAGE[group][source] = []
            messages = await channelforward.get_messages(int(source), limit=100)
            for message in messages:
                message_dict = {
                    "message_id": message.id,
                    "message_text": message.text,
                    "message_type": message.type
                }
                MESSAGE_STORAGE[group][source].append(message_dict)

# Function to repeat messages
async def repeat_messages():
    while True:
        for group, channels in Config.CHANNELS.items():
            if not channelforward.is_busy():
                for source in channels["sources"]:
                    messages_to_send = random.sample(MESSAGE_STORAGE[group][source], Config.MESSAGES_PER_INTERVAL)
                    for destination in channels["destinations"]:
                        for message in messages_to_send:
                            await channelforward.send_message(int(destination), message)
        await asyncio.sleep(Config.MESSAGE_REPEAT_TIME)

# Function to handle incoming messages
@channelforward.on_message(filters.channel)
async def handle_message(client, message):
    for group, channels in Config.CHANNELS.items():
        if str(message.chat.id) in channels["sources"]:
            message_dict = {
                "group": group,
                "source": str(message.chat.id),
                "message_id": message.id,
                "message_text": message.text,
                "message_type": message.type
            }
            messages_collection.insert_one(message_dict)
            MESSAGE_STORAGE[group].append(message)

# Initialize the message storage
async def init_message_storage():
    await store_messages()

# Start the repeat messages loop
async def start_repeat_messages():
    await repeat_messages()

# Run the init_message_storage and start_repeat_messages functions
async def main():
    await init_message_storage()
    await start_repeat_messages()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
