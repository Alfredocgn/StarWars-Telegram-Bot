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
from jinja2 import Environment, FileSystemLoader
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")





bot = telebot.TeleBot(TOKEN)
BASE_URL = 'https://swapi.dev/api/'
spam_times = {}
dir_path = os.path.dirname(os.path.realpath(__file__))
env = Environment(loader=FileSystemLoader(dir_path))

template = env.get_template('register_commands.html') 



def get_movies(id):

  
  response = requests.get(f'https://raw.githubusercontent.com/Alfredocgn/Starwars-DB/main/data/movies.json')

  if response.status_code == 200:
    data = response.json()

    filtered_movie = [movie for movie in data if movie['episode'] == id]

    if filtered_movie:
      movie_info = []
      for movie in filtered_movie:
          title = movie['title']
          director =  movie['director']
          poster_url = movie['poster_url']
          release_date = movie['release_date']
          episode = movie['episode']
          movie_info.append(f'{title} episode {episode}\n Was released in {release_date} \n It was directed by {director}')
          movie_info.append(poster_url)
        
      return movie_info
    else:
      return 'Movie not found'
  else:
    return 'Error fetching data'
  

def get_characters(id):
  response = requests.get(f'https://raw.githubusercontent.com/Alfredocgn/Starwars-DB/main/data/characters.json')


  if response.status_code == 200:
    data = response.json()


    filtered_character = [character for character in data if character['id'] == id]

    if filtered_character:
      character_info = []
      for character in filtered_character:
          name = character['name']
          species =  character['species']
          character_poster_url = character['poster_url']
          gender = character['gender']
          movies = ', '.join(character['movies'])
          character_info.append(f'Name: {name}\n Specie: {species}\n Gender: {gender} \n Movies Apparition: {movies}')
          character_info.append(character_poster_url)
        
      return character_info
    else:
      return 'Character not found'
  else:
    return 'Error fetching data'
  
  
def get_ships(id):
  response = requests.get(f'https://raw.githubusercontent.com/Alfredocgn/Starwars-DB/main/data/ships.json')


  if response.status_code == 200:
    data = response.json()


    filtered_ship = [ship for ship in data if ship['id'] == id]

    if filtered_ship:
      ship_info = []
      for ship in filtered_ship:
          model = ship['name']
          type =  ship['type']
          ship_poster_url = ship['poster_url']
          movies = ', '.join(ship['movies'])
          ship_info.append(f'Model: {model}\n Type: {type}\n Movies Apparition: {movies}')
          ship_info.append(ship_poster_url)
        
      return ship_info
    else:
      return 'Ship not found'
  else:
    return 'Error fetching data'




def handle_spam(user_id):
  if user_id in spam_times:
    spam_time = spam_times[user_id]
    elapsed_time = time.time() - spam_time

    if elapsed_time < 3:
      return True
    else :
      del spam_times[user_id]
  return False

def register_command(user_id, command, username):
    entry = {
        'date': time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()),
        'command': command,
        'user_id': user_id,
        'username': username
    }
    

    with open('register_commands.html', 'r') as file:
        content = file.read()
    

    new_entry = f"        <tr>\n                    <td>{entry['date']}</td>\n                    <td>{entry['command']}</td>\n                    <td>{entry['user_id']}</td>\n                    <td>@{entry['username']}</td>\n                </tr>\n"
    
    content = content.replace('</tbody>', f"{new_entry}</tbody>")
    
    with open('register_commands.html', 'w') as file:
        file.write(content)



@bot.message_handler(commands=['start'])
def cmd_start(message):

  bot.send_message(message.chat.id, f"Hello {message.from_user.first_name},Welcome to the Star Wars Bot")
  if message.chat.id == message.chat.id:
    register_command(message.chat.id, "/start", message.from_user.username)
  bot.send_chat_action(message.chat.id,'upload_photo')
  url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Star_Wars_Logo.svg/2560px-Star_Wars_Logo.svg.png'
  bot.send_photo(message.chat.id, url)
  bot.reply_to(message,text=f"""<i><b><u>Command menu</u></b></i>
                <b><i>/start</i></b> ➡️ Start Menu
                <b><i>/films</i></b> ➡️ Films
                <b><i>/characters</i></b> ➡️ Characters
                <b><i>/ships</i></b> ➡️ Ships
                """,parse_mode ='html')
  

@bot.message_handler(commands=['films'])
def  cmd_films(message):
  if message.chat.id == message.chat.id:
    register_command(message.chat.id, "/films", message.from_user.username)
  bot.send_chat_action(message.chat.id,'typing')

  markup = InlineKeyboardMarkup(row_width=1)
  btn_e_IV = InlineKeyboardButton('Episodio IV',callback_data='e_IV')
  btn_e_V = InlineKeyboardButton('Episodio V',callback_data='e_V')
  btn_e_VI = InlineKeyboardButton('Episodio VI',callback_data='e_VI')
  btn_e_I = InlineKeyboardButton('Episodio I',callback_data='e_I')
  btn_e_II = InlineKeyboardButton('Episodio II',callback_data='e_II')
  btn_e_III = InlineKeyboardButton('Episodio III',callback_data='e_III')
  btn_close = InlineKeyboardButton('Close',callback_data='close')

  markup.add(btn_e_IV,btn_e_V,btn_e_VI,btn_e_I,btn_e_II,btn_e_III,btn_close)
  bot.send_message(message.chat.id, text= 'Select a Movie',parse_mode='MarkdownV2',reply_markup=markup)


@bot.message_handler(commands=['characters'])
def cmd_characters(message):
  if message.chat.id == message.chat.id:
    register_command(message.chat.id, "/characters", message.from_user.username)
  bot.send_chat_action(message.chat.id,'typing')

  markup = InlineKeyboardMarkup(row_width=1)
  btn_luke = InlineKeyboardButton('Luke Skywalker',callback_data='luke')
  btn_leia = InlineKeyboardButton('Leia Organa',callback_data='leia')
  btn_han = InlineKeyboardButton('Han Solo',callback_data='han')
  btn_vader = InlineKeyboardButton('Darth Vader',callback_data='vader')
  btn_kenobi = InlineKeyboardButton('Obi Wan Kenobi',callback_data='kenobi')
  btn_yoda = InlineKeyboardButton('Yoda',callback_data='yoda')
  btn_close = InlineKeyboardButton('Close',callback_data='close')

  markup.add(btn_luke,btn_leia,btn_han,btn_vader,btn_kenobi,btn_yoda,btn_close)
  bot.send_message(message.chat.id,text='Select a Character',parse_mode='MarkdownV2',reply_markup=markup)

@bot.message_handler(commands=['ships'])
def cmd_ships(message):
  if message.chat.id == message.chat.id:
    register_command(message.chat.id, "/ships", message.from_user.username)
  bot.send_chat_action(message.chat.id,'typing')

  markup = InlineKeyboardMarkup(row_width=1)
  btn_falcon = InlineKeyboardButton('Millenium Falcon',callback_data='falcon')
  btn_x_wing = InlineKeyboardButton('X-Wing',callback_data='x-wing')
  btn_tie = InlineKeyboardButton('TIE Fighter',callback_data='tie')
  btn_slave = InlineKeyboardButton('Slave I',callback_data='slave')
  btn_destroyer = InlineKeyboardButton('Star Destroyer',callback_data='destroyer')
  btn_death = InlineKeyboardButton('Death Star',callback_data='death')
  btn_close = InlineKeyboardButton('Close',callback_data='close')

  markup.add(btn_falcon,btn_x_wing,btn_tie,btn_slave,btn_destroyer,btn_death,btn_close)
  bot.send_message(message.chat.id,text='Select a Ship',parse_mode='MarkdownV2',reply_markup=markup)


@bot.callback_query_handler(func=lambda x:True)
def inline_buttons_action(call):
  cid = call.from_user.id
  mid = call.message.id

  if handle_spam(cid):
    bot.answer_callback_query(call.id,"Spam! Wait a minute!",show_alert=True)
    return
  spam_times[cid] = time.time()

  if call.data == 'close':
    bot.delete_message(cid,mid)
    register_command(cid, "Close Button", call.from_user.username)
  elif call.data.startswith('e_'):
    movie_episode_to_id = {'e_IV': 4, 'e_V': 5, 'e_VI': 6, 'e_I': 1, 'e_II': 2, 'e_III': 3}
    movie_id = movie_episode_to_id[call.data]

    if cid == cid:
      register_command(cid, f'Button Movie Episode: {call.data}', call.from_user.username)
    star_wars_films = get_movies(movie_id)
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')
    bot.send_photo(cid,star_wars_films[1],caption=star_wars_films[0])
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')
  elif call.data in ['luke','leia','han','vader','kenobi','yoda']:
    character_name_to_id = {'luke': 1, 'leia': 2, 'han': 3,  'vader': 4,'kenobi': 5, 'yoda': 6}
    character_id = character_name_to_id[call.data]

    if cid == cid:
      register_command(cid, f'Character Button: {call.data}', call.from_user.username)
    character_info = get_characters(character_id)
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')
    bot.send_photo(cid,character_info[1],caption=character_info[0])
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')

  elif call.data in ['falcon','x-wing','tie','slave','destroyer','death']:
    ship_name_to_id = {'falcon':1,'x-wing':2,'tie':3,'slave':4,'destroyer':5,'death':6}
    ship_id = ship_name_to_id[call.data]
    if cid == cid:
      register_command(cid, f'Ship Button: {call.data}', call.from_user.username)
    ships_info = get_ships(ship_id)
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')
    bot.send_photo(cid,ships_info[1],caption=ships_info[0])
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')

@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def bot_text_msg(message):
  if message.text and message.text.startswith("/"):
      bot.send_message(message.chat.id, "Command not available")
  else:
    bot.send_chat_action(message.chat.id, "upload_photo")
    foto = 'https://static-00.iconduck.com/assets.00/not-allowed-icon-2048x2048-iihgwn74.png'
    bot.send_photo(message.chat.id, foto, "Not available")



if __name__ == '__main__':
  print('bot running')
  bot.infinity_polling()
  




