import logging
from datetime import datetime
import telebot
import subprocess
import paramiko

logging.basicConfig(level=logging.DEBUG)

with open("/root/telegram_bot/venvBOT/token.txt", "r") as file:
    api_token = file.read().strip()

bot = telebot.TeleBot(api_token)
group1_ids = []
group2_ids = [981732506]

@bot.message_handler(content_types=['text', 'document'])
def handle_message(message):
    user_id = message.from_user.id
    if user_id in group1_ids:
        if message.text == '/start':
            send_group1_buttons(message.chat.id)
        elif message.text == 'сетевая конфигурация':
            send_network_configuration_buttons(message.chat.id)
        elif message.text == 'базовый набор':
            send_basic_set_buttons(message.chat.id)
        elif message.text == 'сервисы и процессы':
            send_services_and_processes_buttons(message.chat.id)
        elif message.text == 'Статистика блочных устройств':
            send_block_device_statistics_buttons(message.chat.id)
        elif message.text == 'Пользователи':
            send_users_buttons(message.chat.id)
        else:
            execute_command_group1(message)
    elif user_id in group2_ids:
        if message.text == '/start':
            send_group2_buttons(message.chat.id)
        elif message.text in ['service nginx status', 'service cron status']:
            execute_command_group2(message)
        else:
            bot.send_message(message.chat.id, 'Неверная команда.')
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к этому боту.')

def execute_command_group1(message):
    command = message.text

    try:
        at_index = command.find('@')
        if at_index != -1:
            # Код для выполнения команды на удаленном хосте
            remote_command = command[:at_index].strip()
            with open("temp_command.txt", "w") as file:
                file.write(remote_command)

            with open("/root/telegram_bot/venvBOT/credentials.txt", "r") as file:
                username, password = [line.strip() for line in file]
            remote_pc = f"{command[at_index+1:].strip()}.zhemanovy.ru"

            logging.debug(f"Установление SSH-соединения с {remote_pc}")
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(remote_pc, username=username, password=password)
            with open("temp_command.txt", "r") as file:
                remote_command = file.read().strip()

            if remote_command.startswith(("service", "systemctl")):
                remote_command = f"sudo {remote_command}"

            logging.debug(f"Выполнение команды на удаленном ПК: {remote_command}")
            stdin, stdout, stderr = ssh_client.exec_command(remote_command)

            output = stdout.read().decode()

            command_name = remote_command.split()[0]  # Получаем название команды
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Получаем текущую дату и время
            filename = f"{command_name}_{remote_pc}_{current_time}.txt"  # Формируем имя файла
            with open(filename, "w") as file:
                file.write(output)
            with open(filename, "rb") as file:
                bot.send_document(message.chat.id, file)

            ssh_client.close()

        else:
            logging.debug(f"Выполнение локальной команды: {command}")
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()

            command_name = command.split()[0]  # Получаем название команды
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Получаем текущую дату и время

            filename = f"{command_name}_{current_time}.txt"  # Формируем имя файла
            with open(filename, "w") as file:
                file.write(output.decode())
            with open(filename, "rb") as file:
                bot.send_document(message.chat.id, file)

    except Exception as e:
        logging.error(str(e))
        bot.send_message(message.chat.id, str(e))

def execute_command_group2(message):
    command = message.text

    try:
        # Execute the allowed commands
        if command.startswith(("service", "systemctl")):
            command = f"sudo {command}"

        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

        command_name = command.split()[0]  # Get the command name
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Get the current date and time

        filename = f"{command_name}_{current_time}.txt"  # Generate the file name
        with open(filename, "w") as file:
            file.write(output.decode())

        with open(filename, "rb") as file:
            bot.send_document(message.chat.id, file)

    except Exception as e:
        logging.error(str(e))
        bot.send_message(message.chat.id, str(e))

# Button-related functions
def send_group1_buttons(chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    buttons = ['сетевая конфигурация', 'базовый набор', 'сервисы и процессы', 'Статистика блочных устройств', 'Пользователи']
    keyboard.add(*buttons)
    bot.send_message(chat_id, 'Выберите группу команд:', reply_markup=keyboard)

def send_network_configuration_buttons(chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    buttons = ['ping -c 6 8.8.8.8', 'ip a', 'ip r', 'ifconfig']
    keyboard.add(*buttons)
    bot.send_message(chat_id, 'Выберите команду:', reply_markup=keyboard)

def send_basic_set_buttons(chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    buttons = ['cd ~', 'ls -lAt', 'pwd', 'mkdir test_dir']
    keyboard.add(*buttons)
    bot.send_message(chat_id, 'Выберите команду:', reply_markup=keyboard)

def send_services_and_processes_buttons(chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    buttons = ['systemctl list-units --type=service --all', 'ps -aux', 'service nginx status']
    keyboard.add(*buttons)
    bot.send_message(chat_id, 'Выберите команду:', reply_markup=keyboard)

def send_block_device_statistics_buttons(chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    buttons = ['lsblk', 'df -h', 'cat /proc/mounts']
    keyboard.add(*buttons)
    bot.send_message(chat_id, 'Выберите команду:', reply_markup=keyboard)

def send_users_buttons(chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    buttons = ['cat /etc/passwd', 'cat /etc/group', 'cat /etc/sudoers']
    keyboard.add(*buttons)
    bot.send_message(chat_id, 'Выберите команду:', reply_markup=keyboard)

def send_group2_buttons(chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    buttons = ['service nginx status', 'service cron status']
    keyboard.add(*buttons)
    bot.send_message(chat_id, 'Выберите команду:', reply_markup=keyboard)
bot.polling()

