# @michaelsmarthome_bot
import telebot
import logging
import os
import torrent_downloader as torrent
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'logfile.log')
bot = telebot.TeleBot('telegram_token')
# ответ на команды
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую. Введите /help для просмотра всех команд.')
@bot.message_handler(commands=['help'])
def send_some_message(message):
    bot.send_message(message.chat.id, '[мама/даниил/папа] [название] - выгрузка документа (в описании фото)\n\nдокумент [мама/даниил/папа] [название] - получить документ (просто команда)')
    bot.send_message(message.chat.id, 'скачать [файл] - загрузка файла с торрента на сервер (в описании файла)\n\nвыгрузить [файл] [категория] - загрузить ваш файл на сервер с определенной категорией')
# получение фото с документом и занесение его на сервер
# позже реализуем удаление его с серверов телеги
@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    wayuser=message.caption.split(' ')
    wayuser=' '.join(wayuser)
    osway = os.getcwd()
    save_dir=osway+str('\\documents')+'\\'+str(wayuser.replace(' ', '\\'))+'\\'
    with open(save_dir+"image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.from_user.id, "Файл успешно добавлен. Ссылка на загрузку: soon")

# сохранение торрент файла и его обработка
@bot.message_handler(content_types=['document'])
def downloadtorrent(message):
    if message.caption=='скачать':
        try:
            bot.reply_to(message, 'Файл получен, но не будет загружен. Клиент торрент в разработке.')
            # chat_id = message.chat.id
            # file_info = bot.get_file(message.document.file_id)
            # downloaded_file = bot.download_file(file_info.file_path)
            # osway = os.getcwd()
            # src = osway+ '\\torrents\\' + message.document.file_name
            # srcway = osway+ '\\torrents\\'
            # with open(src, 'wb') as new_file:
            #     new_file.write(downloaded_file)
            # bot.reply_to(message, 'Файл сохранен и скоро будет загружен. Вы получите уведомление.')
            # torrent.download(str(srcway), str(src))
        except Exception as e:
            bot.reply_to(message, e)

# выдача документа
@bot.message_handler(content_types=['text'])
def get_document(message):
    chat_id=message.from_user.id
    msglist=str(message.text).split()
    osway = os.getcwd()
    if msglist[0]=='документ':
        if msglist[1]=='мама':
            if msglist[2]=='паспорт':
                waytofile=str('мама\\паспорт\\image.jpg')
            if msglist[2]=='ИНН':
                waytofile=str('мама\\ИНН\\image.jpg')
            if msglist[2]=='снилс':
                waytofile=str('мама\\снилс\\image.jpg')
            if msglist[2]=='фото':
                waytofile=str('мама\\фото\\image.jpg')
        if msglist[1]=='папа':
            if msglist[2]=='паспорт':
                waytofile=str('папа\\паспорт\\image.jpg')
            if msglist[2]=='ИНН':
                waytofile=str('папа\\ИНН\\image.jpg')
            if msglist[2]=='снилс':
                waytofile=str('папа\\снилс\\image.jpg')
            if msglist[2]=='фото':
                waytofile=str('папа\\фото\\image.jpg')
        if msglist[1]=='даниил':
            if msglist[2]=='паспорт':
                waytofile=str('даниил\\паспорт\\image.jpg')
            if msglist[2]=='ИНН':
                waytofile=str('даниил\\ИНН\\image.jpg')
            if msglist[2]=='снилс':
                waytofile=str('даниил\\снилс\\image.jpg')
            if msglist[2]=='фото':
                waytofile=str('даниил\\фото\\image.jpg')
        get_dir=osway+str('\\documents')+'\\'+waytofile
        get_dir=get_dir.replace('\\', '/')
        photo = open(get_dir, 'rb')
        bot.send_photo(chat_id, photo)
    if msglist[0] == "скачать":
        bot.send_message(message.from_user.id, "Разрабатывается.")
        logging.debug( u'Send answer to command "download"')
    if msglist[0] == "выгрузить":
        bot.send_message(message.from_user.id, "Разрабатывается.")
        logging.debug( u'Send answer to command "upload"')
bot.polling(none_stop=True)