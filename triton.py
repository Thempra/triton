import os
import re
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
import whisper


tg_api_token =  os.getenv("TG_API_TOKEN")
path_to_save =  os.getenv("PATH_TO_SAVE", default='./audios/')
language_whisper =  os.getenv("LANGUAGE")


def get_voice(update: Update, context: CallbackContext) -> None:
	filename=str(datetime.now().timestamp())
	audio_file = path_to_save+filename+".ogg"
	if not os.path.exists(path_to_save):
		os.makedirs(path_to_save)

	#Download audio
	new_file = context.bot.get_file(update.message.voice.file_id)
	new_file.download(audio_file)
	
	#Transcribe
	model_fp32 = whisper.load_model(name="small", device="cpu")
	result = model_fp32.transcribe(audio_file, language=language_whisper)
	
	#Detect Title
	result_split = re.split('; |, |\. |\*|\n',result["text"])
	filename = title = result_split[0] if len (result_split) > 1 else re.split("s", result["text"])[0]
	
	fp = open(path_to_save+filename+".md", 'w')
	fp.write(result["text"])
	fp.close()
	os.remove(audio_file)

	update.message.reply_text(result["text"])


if not tg_api_token:
	print("Please, fill TG_API_TOKEN.")
	exit()

updater = Updater(tg_api_token)
updater.dispatcher.add_handler(MessageHandler(Filters.voice , get_voice))
updater.start_polling()
updater.idle()