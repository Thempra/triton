import os
import re
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
import whisper
import boto3
from botocore.client import Config

TG_API_TOKEN =  os.getenv("TG_API_TOKEN")
PATH_TO_SAVE =  os.getenv("PATH_TO_SAVE", default='./audios/')
LANGUAGE_WHISPER =  os.getenv("LANGUAGE")
INBOX =  os.getenv("INBOX").replace('\\','')

ENDPOINT_URL = os.getenv("ENDPOINT_URL")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
BUCKET = os.getenv("BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

def get_voice(update: Update, context: CallbackContext) -> None:
	filename=str(datetime.now().timestamp())
	audio_file = PATH_TO_SAVE+filename+".ogg"
	if not os.path.exists(PATH_TO_SAVE):
		os.makedirs(PATH_TO_SAVE)

	#Download audio
	new_file = context.bot.get_file(update.message.voice.file_id)
	new_file.download(audio_file)

	#Transcribe
	model_fp32 = whisper.load_model(name="small", device="cpu")
	result = model_fp32.transcribe(audio_file, language=LANGUAGE_WHISPER)

	#Detect Title
	result_split = re.split('; |, |\. |\*|\n',result["text"])
	filename = result_split[0] if len (result_split) > 1 else re.split("s", result["text"])[0]

	body="".join(result["text"].split(filename))
	body=''.join(body.split('.', 1))

	fp = open(PATH_TO_SAVE+filename+".md", 'w')
	fp.write(body)
	fp.close()
	os.remove(audio_file)

	if ENDPOINT_URL:
		s3 = boto3.resource('s3', 
				endpoint_url=ENDPOINT_URL, 
				aws_access_key_id=AWS_ACCESS_KEY_ID, 
				aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
				config=Config(s3={"addressing_style": "path"}))

		try:
			s3.Bucket(BUCKET).upload_file(PATH_TO_SAVE+filename+".md", INBOX+"/"+filename+".md")
		except Exception as e:
			print("Failed to upload file!")

	update.message.reply_text(filename +"\n\n"+body)


if not TG_API_TOKEN:
	print("Please, fill TG_API_TOKEN.")
	exit()

updater = Updater(TG_API_TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.voice , get_voice))
updater.start_polling()
updater.idle()