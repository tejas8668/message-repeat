import logging
logger = logging.getLogger(__name__)

from pyrogram import filters
from bot import channelforward
from config import Config
from translation import Translation
from pymongo import MongoClient

# MongoDB क्लाइंट बनाएं
client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB]
messages_collection = db["messages"]


################################################################################################################################################################################################################################################
# start command

@channelforward.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(client, message):
    await message.reply(
        text=Translation.START,
        disable_web_page_preview=True,
        quote=True
    )

################################################################################################################################################################################################################################################
# about command

@channelforward.on_message(filters.command("about") & filters.private & filters.incoming)
async def about(client, message):
    await message.reply(
        text=Translation.ABOUT,
        disable_web_page_preview=True,
        quote=True
    )

################################################################################################################################################################################################################################################
# add command

@channelforward.on_message(filters.command("add") & filters.private & filters.incoming)
async def add(client, message):
    await message.reply("Please enter the channel ID you want to index")
    channel_id = message.text.split(" ")[1]
    messages = await channelforward.get_messages(int(channel_id), limit=100)
    for message in messages:
        message_dict = {
            "channel_id": channel_id,
            "message_id": message.id,
            "message_text": message.text,
            "message_type": message.type
        }
        messages_collection.insert_one(message_dict)
    await message.reply("Channel messages indexed successfully")

################################################################################################################################################################################################################################################
# clear command

@channelforward.on_message(filters.command("clear") & filters.private & filters.incoming)
async def clear(client, message):
    messages_collection.delete_many({})
    await message.reply("Stored messages deleted successfully")

################################################################################################################################################################################################################################################
# clrcnl command

@channelforward.on_message(filters.command("clrcnl") & filters.private & filters.incoming)
async def clrcnl(client, message):
    channel_id = message.chat.id
    messages = await channelforward.get_messages(channel_id, limit=100)
    for message in messages:
        await channelforward.delete_messages(channel_id, message.id)
    await message.reply("Channel messages deleted successfully")
