from __future__ import unicode_literals 
import requests
import json
import base64
import wget
from jsonpath_ng import jsonpath, parse
from telebot import TeleBot
import youtube_dl
import requests
import json
import time
import os
import base64
import shutil, sys
from zipfile import ZipFile
from shutil import rmtree
from os.path import basename
from jsonpath_ng import jsonpath, parse
TOKEN = os.environ['TOKEN']
bot = TeleBot(TOKEN)
# Handle '/start' and '/help'
@bot.message_handler(commands=['privkey', 'start'])
def send_usuario(message):
    user_id = str(message.from_user.id)
    user_first_name = str(message.chat.first_name) 
    msg = bot.reply_to(message, f"Hey! {user_first_name} tu id es : {user_id} \n Ingresa ID del curso")
    chat_id = message.chat.id
    lista_cursos = message.text
    #prueba guardar y verificar en base de datos#
    #prueba guardar y verificar en base de datos#
    bot.register_next_step_handler(msg, process_name_step)
def process_name_step(message):
    try:
        chat_id = message.chat.id
        lista_cursos = message.text
        msg = bot.send_message(chat_id, 'Estamos bajando el curso!')
    except Exception as e:
        bot.reply_to(message, 'oooops')

    for num1 in lista_cursos.split(','):
        dictionary = {
        "query": "query course($courseId: String!) {course(id: $courseId) {title attachmentSet{edges{node{attachment}}} modules{videoLectureSet{edges{node{title  subtitleList{subtitleFile} videoLectureSource{provider desktopPlaylists{url}}}}}} }}",
        "operationName": "course",
    "variables": {
            "courseId": int(num1)
        }
        }
        print("Descargando : "+num1)
        jsonString = json.dumps(dictionary)
        url = "https://www.crehana.com/api/v2/graph/"
        headers = {
                "content-type": "application/json",
                "creh-platform-type": "desktop",
                "authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJhbmRvbWN1cnNlc3BybzEyMzQ1NkB5b3BtYWlsLmNvbSIsImV4cCI6MTY0NjA4MTkzMywianRpIjoiYzA3NWM4OGE4ZDBmMTFlY2I0NmEwMjQyYWMxMTAwMDMiLCJvcmlnSWF0IjoxNjQ0Nzg1OTMzfQ.XGhbTyBM_nZSqETQz0fgOjScKJtymMO2wAQmBO2R8FU",
                "Accept-Language": "es",
                "x-requested-with": "XMLHttpRequest"
            }

        response = requests.post(url, data=jsonString, headers=headers)

        json_data = json.loads(response.text)
        file = open(num1+"-wtemp.txt", "w")
        file.write(response.text)
        file.close()
    #capturo titulo
        with open(num1+"-wtemp.txt", 'r', encoding="latin-1") as json_file:
            json_data = json.load(json_file)
        jsonpath_expression = parse('data.course.title')
        for tits in jsonpath_expression.find(json_data):
                curstitle = tits.value
                print (curstitle)
    #fin captura titulo
    #inicio captura files links
        with open(num1+"-wtemp.txt", 'r', encoding="latin-1") as json_file:
            json_data = json.load(json_file)
        jsonpath_expression = parse('data.course.attachmentSet.edges[*].node.attachment')
        for filesdmk in jsonpath_expression.find(json_data):
                print(filesdmk.value,file=open(num1+"-files.txt","a"))
     #inicio captura files links          
        with open(num1+"-wtemp.txt", 'r', encoding="latin-1") as json_file:
            json_data = json.load(json_file)
        jsonpath_expression = parse('data.course.modules.[*].videoLectureSet.edges.[*].node.videoLectureSource.[0].desktopPlaylists.[*].url')
        for match1 in jsonpath_expression.find(json_data):
                print(match1.value,file=open(num1+".txt","a"))
        if os.path.isfile(num1+'.txt') ==True :
            pass
        else :
            with open(num1+"-wtemp.txt", 'r', encoding="latin-1") as json_file:
                json_data = json.load(json_file)
            jsonpath_expression = parse('data.course.modules.[*].videoLectureSet.edges.[*].node.videoLectureSource.[*].desktopPlaylists.[*].url')
            for match2 in jsonpath_expression.find(json_data):
                print(match2.value,file=open(num1+".txt","a"))
    file="./"+num1+".txt"
    filezip="./"+num1+"-files.txt"
    bot.send_message(chat_id, "Te estamos enviando el curso: "+curstitle)
    bot.send_document(chat_id, document=open(file, 'rb'),caption="Enlaces a videos directos")
    bot.send_message(chat_id, "Te estamos enviando los descargables")
    bot.send_document(chat_id, document=open(filezip, 'rb'),caption="Enlaces directos a archivos")
    os.remove(num1+"-wtemp.txt")
    os.remove(num1+"-files.txt")
    os.remove(num1+".txt")
###########################################LIMPIEZA#
bot.polling()
