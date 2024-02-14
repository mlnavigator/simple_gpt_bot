# env data

add .env file to cred folder

.env file data
```
BOT_TOKEN=
ACCESS_KEY=
OPENAI_API_KEY=
GPT_BACKEND=
```


# run project

* run commands from folder with project
* docker build -t MlNavigator/simple_gpt_bot .
* docker run -d --restart=always --name=simple_gpt_bot --env-file ./cred/.env MlNavigator/simple_gpt_bot

