echo "start"
docker stop simple_gpt_bot
docker rm simple_gpt_bot
docker rmi simple_gpt_bot
docker build -t simple_gpt_bot .
docker run -d --restart=always --name=simple_gpt_bot -v ./assets:/app/assets simple_gpt_bot
echo "finished - ran container simple_gpt_bot"