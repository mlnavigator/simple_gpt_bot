# config data

add config.json file to assets folder

need config data see in example_config.json
```
{
  "BOT_TOKEN": "телеграм бот токен, спросите его у botfather",
  "ACCESS_KEY": "пароль обынчых пользователей",
  "SU_ACCESS_KEY": "admin_password",
  "OPENAI_API_KEY": "ключ опен аи или их прокси",
  "GPT_BACKEND": "https://api.proxyapi.ru/openai/v1 - or other api url"
}
```


# run project

* run commands from main folder with project
* docker build -t simple_gpt_bot .
* docker run -d --restart=always --name=simple_gpt_bot -v ./assets:/app/assets simple_gpt_bot
* run previous command from main folder of project, or set absolute path to assets folder with config
* after changing ./assets/config.json - stop and remove container and run it again

# using bot

* для доступа к боту введите /start ACCESS_KEY или админ добавит пользователя вручную
* команда /start выводит user_id для добавления 
* Бот помнит последние 10 сообщений
* Для установки системного сообщения напишите /system ваше сообщение
* /info - для получения вашей информации
* /reset - очистить историю сообщений
* бот использует гпт 3.5 турбо, тк она дешевле

# admin area

* /admin super_user_pass - для входа в админ режим
* /config key value - изменит данные в конфиге бота.
* /reboot - перезапустить бота, будет перезапуск контейнера с новыми конфигами
* /reset_client - обновить подключение к чат гпт - надо делать после изменения токена и урла чата гпт
* /stat - статистика по пользователям
* /rm user_id - удалить пользователя по его телеграм id
* /add user_id - добавить пользователя по его телеграм id
