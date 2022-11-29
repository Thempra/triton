# Triton-bot


Bot to transcribe a Telegram audio recording and save to your Obsidian Vault with OpenAI's Whisper.
  

## Generate API Keys

1. Send /newbot to https://telegram.me/BotFather
2. Reply BotFather with the name of the bot you wish to use.
3. Next, reply BotFather with the username of the bot you wish to use for your bot
4. At this point, your bot should have been created!
  

## Install

It has been dockerized for easy installation, variables can be configured through docker-compose.yml

Example:
```
version: "3"

services:
  kubot:
    container_name: triton
    image: triton
    restart: always
    environment:
      - TG_API_TOKEN=XXXXXXXXXX:XXXXXXXXXXXX-XXXXXXXXXXXXXXX
      - LANGUAGE=spanish
      - PATH_TO_SAVE=./audios/
    volumes:
      - /data/obsidian/Main/001\ -\ 📥\ INBOX:/usr/src/app/audios

```

Run:
```
# docker build . -t triton
# docker-compose up -d
```