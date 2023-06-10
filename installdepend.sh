#!/bin/bash
mkdir telegram_bot && cd telegram_bot && apt update -y && apt upgrade -y
apt install curl python3-venv screen -y && python3 -m venv venvBOT && source venvBOT/bin/activate
pip install pytelegrambotapi datetime subprocess paramiko 
touch ~/tmp.cron
echo '@reboot screen -dmS BotScreen bash -c "source /root/telegram_bot/venvBOT/bin/activate && python3 /root/telegram_bot/venvBOT/bot_v3.10.py"' >> ~/tmp.cron 
crontab ~/tmp.cron
rm ~/tmp.cron 
# �������� ���������� ������� � crontab
if crontab -l | grep -q '/root/telegram_bot/venvBOT/bot_v3.10.py'; then
    echo "������� ������� ��������� � crontab"
else
    echo "������: ������� �� ���� ��������� � crontab"
fi
# ������ ������� ���������� ����
curl -o /root/telegram_bot/venvBOT/bot_v3.10.py -LJO https://github.com/Start127/diplom/bot_v3.10.py

# �������� ��������� ���������� ���� ����� ������ �������
if [ -f "/root/telegram_bot/venvBOT/bot_v3.10.py" ]; then
    echo "��� ������� �������� � /root/telegram_bot/venvBOT/bot_v3.10.py ��� ��� ������� ����������� python3 /root/telegram_bot/venvBOT/bot_v3.10.py  ��� ������ ������������� ��"
else
    echo "������ ��� ���������� ����. ������� ������� �� ������ ������..."
    # ������ ������� ���������� ����
    curl -o /root/telegram_bot/venvBOT/bot_v3.10.py "https://drive.google.com/uc?export=download&id=1q8xKv9TIIBKhQIMG2oO0TkMwEv0VHybv"

    # �������� ��������� ���������� ���� ����� ������ �������
    if [ -f "/root/telegram_bot/venvBOT/bot_v3.10.py" ]; then
        echo " ��� ������� �������� � /root/telegram_bot/venvBOT/bot_v3.10.py ��� ��� ������� ����������� python3 /root/telegram_bot/venvBOT/bot_v3.10.py  ��� ������ ������������� �� "
    else
        echo "������ ��� ���������� ���� �� ������ ������"
    fi
fi
