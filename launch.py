# @michaelsmarthome_bot
import telebot
import logging
import os
import torrent_downloader as torrent
import transcriptor as trs
# logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.INFO, filename = u'logfile_info.log')
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'logfile_debug.log')
bot = telebot.TeleBot('botid')
logging.info(u"----BOT STARTED----")
# ответ на команды
@bot.message_handler(commands=['start'])
def start_message(message):
    username=message.from_user.username
    bot.send_message(message.chat.id, message.text)
    bot.send_message(message.chat.id, 'Приветствую. Введите /help для просмотра всех команд.')
    logging.info(u'cmd:start, result:successful, user:'+username)
@bot.message_handler(commands=['admin'])
def admin_message(message):
    username=message.from_user.username
    bot.send_message(message.chat.id, 'Администратор еще спит. Он не доделал эту функцию.')
    logging.info(u'cmd:admin, result:successful, user:'+username)
@bot.message_handler(commands=['help'])
def send_some_message(message):
    username=message.from_user.username
    bot.send_message(message.chat.id, '[мама/даниил/папа] [название] - выгрузка документа (в описании фото)\n\nдокумент [мама/даниил/папа] [название] - получить документ (просто команда)')
    bot.send_message(message.chat.id, 'скачать [файл] - загрузка файла с торрента на сервер (в описании файла)\n\nвыгрузить [файл] [категория] - загрузить ваш файл на сервер с определенной категорией')
    bot.send_message(message.from_user.id, "Если это не помогло - связь с администрацией доступна по команде /admin")
    logging.info(u'cmd:help, result:successful, user:'+username)
# получение фото с документом и занесение его на сервер
# позже реализуем удаление его с серверов телеги
@bot.message_handler(content_types=['photo'])
def photo(message):
    username=message.from_user.username
    try:
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
        logging.info(u'cmd:document(send), result:successful added document, user:'+username)
    except AttributeError:
        bot.send_message(message.from_user.id, "Нет описания у фото. Попробуйте еще раз.")
        logging.warn(u'cmd:document(send), result:user not provided document info, user:'+username)
# сохранение торрент файла и его обработка
@bot.message_handler(content_types=['document'])
def downloadtorrent(message):
    username=message.from_user.username
    if message.caption=='скачать':
        try:
            bot.reply_to(message, 'Файл получен, но не будет загружен. Клиент торрент в разработке.')
            logging.info(u'cmd:download result:successful show warning, user:'+username)
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
    username=message.from_user.username
    chat_id=message.from_user.id
    msglist=str(message.text).split()
    osway = os.getcwd()
    if msglist[0]=='документ':
        logging.info( u'cmd:document(get), result:successful get command document, user:'+username)
        if msglist[1]=='мама':
            logging.info( u'cmd:document(get) result:successful get mother, user:'+username)
            if msglist[2]=='паспорт':
                waytofile=str('мама\\паспорт\\image.jpg')
            if msglist[2]=='ИНН':
                waytofile=str('мама\\ИНН\\image.jpg')
            if msglist[2]=='снилс':
                waytofile=str('мама\\снилс\\image.jpg')
            if msglist[2]=='фото':
                waytofile=str('мама\\фото\\image.jpg')
        if msglist[1]=='папа':
            logging.info( u'cmd:document(get) result:successful get father, user:'+username)
            if msglist[2]=='паспорт':
                waytofile=str('папа\\паспорт\\image.jpg')
            if msglist[2]=='ИНН':
                waytofile=str('папа\\ИНН\\image.jpg')
            if msglist[2]=='снилс':
                waytofile=str('папа\\снилс\\image.jpg')
            if msglist[2]=='фото':
                waytofile=str('папа\\фото\\image.jpg')
        if msglist[1]=='даниил':
            logging.info( u'cmd:document(get) result:successful get daniel, user:'+username)
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
        logging.info( u'cmd:document(get) result:successful sended, user:'+username)
    if msglist[0] == "скачать":
        bot.send_message(message.from_user.id, "Разрабатывается.")
        logging.info( u'Send answer to command "download" to user:'+username)
    if msglist[0] == "выгрузить":
        bot.send_message(message.from_user.id, "Разрабатывается.")
        logging.info( u'Send answer to command "upload" to user:'+username)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Введи /help для помощи.")
        if trs.transcript(msglist[0])!='None':
            logging.info( u'unsupported command "'+trs.transcript(msglist[0])+'" from user:'+username)
        else:
            logging.info( u'unsupported command "'+msglist[0]+'" from user:'+username)
try:
    bot.polling(none_stop=True)
except:
    logging.warning( u'----BOT RESTARTED due to some errors----')
    pass