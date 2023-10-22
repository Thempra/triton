import os
import re
from datetime import datetime
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import whisperx
import boto3
from botocore.client import Config

TG_API_TOKEN =  os.getenv("TG_API_TOKEN")

ONLY_TRANSCRIBE = os.getenv("ONLY_TRANSCRIBE", True)
ENDPOINT_URL = os.getenv("ENDPOINT_URL")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
BUCKET = os.getenv("BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

#Temp save data
PATH_TO_SAVE =  os.getenv("PATH_TO_SAVE", default='./audios/')
filename=str(datetime.now().timestamp())
AUDIO_FILE = PATH_TO_SAVE+filename+".ogg"


try:
	INBOX =  os.getenv("INBOX").replace('\\','')
except Exception as e:
     INBOX = None

async def downloader(update, context):
	new_file = await context.bot.get_file(update.message.audio.file_id if "audio" in update.message.to_dict() else update.message.voice.file_id )
	await new_file.download_to_drive(AUDIO_FILE)


async def get_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	if not os.path.exists(PATH_TO_SAVE):
		os.makedirs(PATH_TO_SAVE)

	await downloader(update,context)
     
	#Transcribe
	#model_fp32 = whisper.load_model(name="small", device="cpu")
	model_fp32 = whisperx.load_model("large-v2", device="cpu", compute_type="int8")

	result = model_fp32.transcribe(AUDIO_FILE)
	transcribed_text = result['segments'][0]["text"]

	if not ONLY_TRANSCRIBE:
		#Detect Title
		result_split = re.split('; |, |\. |\*|\n',transcribed_text)
		filename = result_split[0] if len (result_split) > 1 else re.split("s", transcribed_text)[0]

		body="".join(transcribed_text.split(filename))
		body=''.join(body.split('.', 1))

		save_file(filename, body)
		await update.message.reply_text(filename +"\n\n"+body)
	else:
		await update.message.reply_text(transcribed_text)

	os.remove(AUDIO_FILE)

     

def save_file(title, body):
    fp = open(PATH_TO_SAVE+title+".md", 'w')
    fp.write(body)
    fp.close()

    if ENDPOINT_URL:
     s3 = boto3.resource('s3', 
				endpoint_url=ENDPOINT_URL, 
				aws_access_key_id=AWS_ACCESS_KEY_ID, 
				aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
				config=Config(s3={"addressing_style": "path"}))

     try:
      s3.Bucket(BUCKET).upload_file(PATH_TO_SAVE+title+".md", INBOX+"/"+title+".md")
     except Exception as e:
      print("Failed to upload file!")



if not TG_API_TOKEN:
	print("Please, fill TG_API_TOKEN.")
	exit()

application = Application.builder().token(TG_API_TOKEN).build()
application.add_handler(MessageHandler(filters.VOICE or filters.AUDIO , get_voice))
application.run_polling(allowed_updates=Update.ALL_TYPES)

