#!/bin/bash
mkdir telegram_bot && cd telegram_bot && apt update -y && apt upgrade -y
apt install curl python3-venv screen -y && python3 -m venv venvBOT && source venvBOT/bin/activate
pip install pytelegrambotapi datetime subprocess paramiko 
touch ~/tmp.cron
echo '@reboot screen -dmS BotScreen bash -c "source /root/telegram_bot/venvBOT/bin/activate && python3 /root/telegram_bot/venvBOT/bot_v3.10.py"' >> ~/tmp.cron 
crontab ~/tmp.cron
rm ~/tmp.cron 
# Проверка добавления команды в crontab
if crontab -l | grep -q '/root/telegram_bot/venvBOT/bot_v3.10.py'; then
    echo "Команда успешно добавлена в crontab"
else
    echo "Ошибка: команда не была добавлена в crontab"
fi
# Первая попытка скачивания бота
curl -o /root/telegram_bot/venvBOT/bot_v3.10.py https://cloud.mail.ru/public/CCeA/CU9Y5cd86/bot_v3.10.py

# Проверка успешного скачивания бота после первой попытки
if [ -f "/root/telegram_bot/venvBOT/bot_v3.10.py" ]; then
    echo "Бот успешно скачался в /root/telegram_bot/venvBOT/bot_v3.10.py для его запуска используйте python3 /root/telegram_bot/venvBOT/bot_v3.10.py  или просто перезагрузите ПК"
else
    echo "Ошибка при скачивании бота. Попытка скачать по другой ссылке..."
    # Вторая попытка скачивания бота
    curl -o /root/telegram_bot/venvBOT/bot_v3.10.py "https://drive.google.com/uc?export=download&id=1q8xKv9TIIBKhQIMG2oO0TkMwEv0VHybv"

    # Проверка успешного скачивания бота после второй попытки
    if [ -f "/root/telegram_bot/venvBOT/bot_v3.10.py" ]; then
        echo " Бот успешно скачался в /root/telegram_bot/venvBOT/bot_v3.10.py для его запуска используйте python3 /root/telegram_bot/venvBOT/bot_v3.10.py  или просто перезагрузите ПК "
    else
        echo "Ошибка при скачивании бота по другой ссылке"
    fi
fi
