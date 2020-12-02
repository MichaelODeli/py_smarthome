# @michaelsmarthome_bot
import telebot
import logging
import os
import torrent_downloader as torrent
import transcriptor as trs
import configparser
import datetime
config = configparser.ConfigParser()
config.read("config.ini")
botid=config.get('main', 'botid')
localip=config.get('main', 'localip')
adminname=config.get('main', 'admin')
admin_chatid=config.get('main', 'admin_chatid')
report = configparser.ConfigParser()
report.read('report.ini')
# user check
def usercheck(username):
    mom=config.get('homeusers', 'mother')
    dad=config.get('homeusers', 'father')
    dan=config.get('homeusers', 'daniel')
    if username==mom or username==dad or username==dan:
        logging.info(u'cmd:checkuser, result:accepted, user:'+username)
        return('True')
    else:
        return('Ошибка. Вы не уполномочены использовать данную команду. Если это не так - свяжитесь с администрацией по команде /admin')

def register_report(username, message, chat_id):
    now = datetime.datetime.now()
    created = now.strftime("%d-%m-%Y %H:%M")
    sections=report.sections()
    secnumber=1+int(sections[-1])
    strnumber=str(secnumber)
    report.add_section(strnumber)
    msglist=[]
    for msg_word in message:
        msglist.append(trs.transcript_report(msg_word))
    message=''.join(msglist)
    report.set(strnumber, 'username', username)
    report.set(strnumber, 'created', created)
    report.set(strnumber, 'message', message)
    report.set(strnumber, 'username', username)
    report.set(strnumber, 'chatid', chat_id)
    report.set(strnumber, 'closed', 'False')
    with open('report.ini', "w") as config_file:
        report.write(config_file)
    return(int(secnumber))

# LOG parameters
# logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.INFO, filename = u'logfile_info.log')
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'logfile_debug.log')
bot = telebot.TeleBot(botid)
logging.info(u"----BOT STARTED----")


# ответ на команды
# admins commands
@bot.message_handler(commands=['admin'])
def admin_message(message):
    msg=message.text
    msglist=msg.split(' ')
    username=message.from_user.username
    if len(msglist)=='1':
        bot.send_message(message.chat.id, 'Для отправки обращения используйте /admin [текст обращения]')
        logging.info(u'cmd:admin, result:error in input by user, user:'+username)
    else:
        chat_id=message.from_user.id
        numb=register_report(username, message.text, str(chat_id))
        bot.send_message(message.chat.id, 'Обращение зарегистрировано. Номер обращения: '+str(numb))
        logging.info(u'cmd:admin, result:sended report, user:'+username+', user_input:dev')
        # лучше это не использовать, а то спам бесконечный будет при ответах на репорты
        bot.forward_message(admin_chatid, message.chat.id, message.message_id)
        bot.send_message(admin_chatid, str('chat_id:'+str(chat_id)+', number:'+str(numb)))
@bot.message_handler(commands=['answer'])
def admin_answer(message):
    username=message.from_user.username
    if username==adminname:
        try:
            msg=message.text
            msglist=msg.split(' ')
            chatid=msglist[2]
            reportnum=msglist[1]
            del msglist[0]
            del msglist[0]
            del msglist[0]
            msgout=' '.join(msglist)
            bot.send_message(chatid, 'Ответ от администрации на Ваше обращение: '+str(msgout))
            newmsglist=[]
            for msg_word in msglist:
                newmsglist.append(trs.transcript_report(msg_word))
            msginreport=' '.join(newmsglist)
            now = datetime.datetime.now()
            closed = now.strftime("%d-%m-%Y %H:%M")
            report.set(reportnum, 'answer', msginreport)
            report.set(reportnum, 'closed_time', closed)
            report.set(reportnum, 'closed', 'True')
            with open('report.ini', "w") as config_file:
                report.write(config_file)
        except IndexError:
            bot.send_message(message.chat.id, '/answer [number of report] [chatid] [message]')
    else:
        logging.info(u'cmd:answer, result:user rejected, user:'+username)
        errorstring='Ошибка. Вы не уполномочены использовать данную команду. Если это не так - свяжитесь с администрацией по команде /admin'
        bot.send_message(message.chat.id, errorstring)
@bot.message_handler(commands=['adminid'])
def adminid(message):
    username=message.from_user.username
    if username==adminname:
        chat_id=message.from_user.id
        config.set('main', 'admin_chatid', str(chat_id))

@bot.message_handler(commands=['help'])
def send_some_message(message):
    username=message.from_user.username
    bot.send_message(message.chat.id, '[мама/даниил/папа] [название] - выгрузка документа (в описании фото)\n\nдокумент [мама/даниил/папа] [название] - получить документ (просто команда)')
    bot.send_message(message.chat.id, 'скачать [файл] - загрузка файла с торрента на сервер (в описании файла)\n\nвыгрузить [файл] [категория] - загрузить ваш файл на сервер с определенной категорией')
    bot.send_message(message.from_user.id, "Если это не помогло - связь с администрацией доступна по команде /admin")
    logging.info(u'cmd:help, result:successful, user:'+username)
@bot.message_handler(commands=['start'])
def start_message(message):
    username=message.from_user.username
    bot.send_message(message.chat.id, message.text)
    bot.send_message(message.chat.id, 'Приветствую. Введите /help для просмотра всех команд.')
    logging.info(u'cmd:start, result:successful, user:'+username)


# получение фото с документом и занесение его на сервер
# позже реализуем удаление его с серверов телеги
@bot.message_handler(content_types=['photo'])
def photo(message):
    username=message.from_user.username
    if usercheck(username)=='True':
        try:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)
            wayuser=message.caption.split(' ')
            wayuser=' '.join(wayuser)
            osway = os.getcwd()
            save_dir=osway+str('\\documents')+'\\'+str(wayuser.replace(' ', '\\'))+'\\'
            file_location=localip+str('\\documents')+'\\'+str(wayuser.replace(' ', '\\'))+'\\'
            file_location=file_location.replace('\\', '/')
            with open(save_dir+"image.jpg", 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.from_user.id, "Файл успешно добавлен. Ссылка на загрузку: "+file_location)
            logging.info(u'cmd:document(send), result:successful added document, user:'+username)
        except AttributeError:
            bot.send_message(message.from_user.id, "Нет описания у фото. Попробуйте еще раз.")
            logging.warn(u'cmd:document(send), result:user not provided document info, user:'+username)
    else:
        bot.send_message(message.from_user.id, usercheck(username))
        logging.info(u'cmd:document(send), result:user rejected, user:'+username)

# сохранение торрент файла и его обработка
@bot.message_handler(content_types=['document'])
def downloadtorrent(message):
    username=message.from_user.username
    if usercheck(username)=='True':
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
    else:
        bot.send_message(message.from_user.id, usercheck(username))
        logging.info(u'cmd:download, result:user rejected, user:'+username)

# выдача документа
@bot.message_handler(content_types=['text'])
def get_document(message):
    username=message.from_user.username
    chat_id=message.from_user.id
    msglist=str(message.text).split()
    osway = os.getcwd()
    if msglist[0]=='документ':
        if usercheck(username)=='True':
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
            elif msglist[1]=='папа':
                logging.info( u'cmd:document(get) result:successful get father, user:'+username)
                if msglist[2]=='паспорт':
                    waytofile=str('папа\\паспорт\\image.jpg')
                if msglist[2]=='ИНН':
                    waytofile=str('папа\\ИНН\\image.jpg')
                if msglist[2]=='снилс':
                    waytofile=str('папа\\снилс\\image.jpg')
                if msglist[2]=='фото':
                    waytofile=str('папа\\фото\\image.jpg')
            elif msglist[1]=='даниил':
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
            logging.info( u'cmd:document(get), result:successful sended, user:'+username)
        else:
            bot.send_message(message.from_user.id, usercheck(username))
            logging.info(u'cmd:document_get, result:user rejected, user:'+username)
    elif msglist[0] == "скачать":
        bot.send_message(message.from_user.id, "Разрабатывается.")
        logging.info( u'Send answer to command "download" to user:'+username)
    elif msglist[0] == "выгрузить":
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
except Exception as e:
    logging.warning( u'----BOT RESTARTED, because '+str(e))
    pass