# config data

add config.json file to assets folder

need config data see in example_config.json
```
{
  "BOT_TOKEN": "телеграм бот токен, спросите его у botfather",
  "ACCESS_KEY": "пароль обынчых пользователей",
  "SU_ACCESS_KEY": "admin_password",
  "OPENAI_API_KEY": "ключ опен аи или их прокси",
  "GPT_BACKEND": "https://api.proxyapi.ru/openai/v1 - or other api url",
  "GPT_MODEL": "gpt-3.5-turbo"
}
```


# run project

* variant 1. run with docker: 
  * cd "project folder"; sudo bash ./rebuild.sh
  * for remove container and image: sudo bash ./remove.sh


* variant 2. run with python 3.10. 
  * cd "project folder"
  * install and activate venv
  * python3 -m pip install -r requirements.txt; python3 tg_bot.py &


# using bot

* для доступа к боту введите /start ACCESS_KEY или админ добавит пользователя вручную
* команда /start выводит user_id для добавления 
* Бот помнит последние 10 сообщений
* Для установки системного сообщения напишите /system ваше сообщение
* /info - для получения вашей информации
* /reset - очистить историю сообщений
* бот использует гпт 3.5 турбо, тк она дешевле, но вы можете поменять это в конфиге

# admin area

* /admin super_user_pass - для входа в админ режим
* /config key value - изменит данные в конфиге бота.
* /reboot - перезапустить бота, будет перезапуск контейнера с новыми конфигами
* /reset_client - обновить подключение к чат гпт - надо делать после изменения токена и урла чата гпт
* /stat - статистика по пользователям
* /rm user_id - удалить пользователя по его телеграм id
* /add user_id - добавить пользователя по его телеграм id
* /mass message text - отправить массовое сообщение всем пользователям бота
