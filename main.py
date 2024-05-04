import telebot 
import time
import threading
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup 
from telebot.types import ForceReply 
from telebot.types import ReplyKeyboardRemove 
import logging
import platform
import requests


TOKEN = ''

bot = telebot.TeleBot(TOKEN)
BASE_URL = 'https://swapi.dev/api/'

def get_films(id):
  complete_url = f'{BASE_URL}films/{id}'
  response = requests.get(complete_url)
  if response.status_code == 200:
    data = response.json()
    movie_info =[]

    if 'title' in data:
      movie_name = data['title']
      movie_episode = data['episode_id']
      movie_opening = data['opening_crawl'][:200]
      movie_date = data['release_date'][:4]
      movie_director = data['director']
      movie_poster = 'http://images1.wikia.nocookie.net/__cb20130325100645/moviepedia/de/images/4/41/Episode_IV.jpg'
      movie_info.append(f'{movie_name} {movie_episode}\n was released in {movie_date} \n It was directed by *{movie_director}*')
      movie_info.append(movie_poster)
      return movie_info
    else:
      return 'Movie not found'
  else :
    return 'Error fetching data'


@bot.message_handler(commands=['start'])
def cmd_start(message):
  bot.send_message(message.chat.id, f"Hello {message.from_user.first_name},Welcome to the Star Wars Bot")
  if message.chat.id == message.chat.id:
    register = []
    register.append(str(message.chat.id)),
    file = open('register_ID.txt','a',encoding = 'utf-8')
  for i in register:
    file.write(time.strftime("%d/%m/%Y %H:%M:%S",time.localtime())+ '\n')
    file.write(f'Command:/start\n')
    file.write(f'UserID: {i}\n')
    file.write(f'Username: @{message.from_user.username}\n')
    file.close()
  bot.send_chat_action(message.chat.id,'upload_photo')
  url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Star_Wars_Logo.svg/2560px-Star_Wars_Logo.svg.png'
  bot.send_photo(message.chat.id, url)
  bot.reply_to(message,text=f"""<i><b><u>Command menu</u></b></i>
                <b><i>/start</i></b> ➡️ Start Menu
                <b><i>/Films</i></b> ➡️ Films
                """,parse_mode ='html')
  

@bot.message_handler(commands=['Films'])
def  cmd_films(message):
  star_wars_films = get_films(1)
  bot.send_photo(message.chat.id,star_wars_films[1])
  bot.reply_to(message,star_wars_films)








@bot.message_handler(commands=['help'])
def cmd_help(message):
  bot.reply_to(message,'Este es el comando de ayuda')

if __name__ == '__main__':
  print('bot running')
  bot.polling(non_stop=True)




