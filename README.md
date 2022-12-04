# Triton


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
  triton:
    container_name: triton
    image: thempra/triton
    restart: always
    environment:
      - TG_API_TOKEN=XXXXXXXXXX:XXXXXXXXXXXX-XXXXXXXXXXXXXXX
      - LANGUAGE=spanish

```

## Example environment variables

```
- TG_API_TOKEN=XXXXXXXXX:XXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXX
- LANGUAGE=spanish
- BUCKET=bucketname
- INBOX=001\ -\ 📥\ INBOX
- ENDPOINT_URL=https://xxxxxx.xxxxxxx.xxx
- AWS_DEFAULT_REGION=xx-xxxx-xx
- AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxx
- AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Run
```
# docker build . -t triton
# cp .env.test .env
# source .env
# docker-compose up -d
```
