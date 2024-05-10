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


TOKEN = '7187157539:AAHjH_l7wEy12imMgUSbLkFF2WJAP7GckgA'
GITHUB_TOKEN = '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'
headers = {
  'Authorization': f'Bearer {GITHUB_TOKEN}'
}

bot = telebot.TeleBot(TOKEN)
BASE_URL = 'https://swapi.dev/api/'
GITHUB_URL = 'https://github.com/Alfredocgn/Starwars-DB/blob/main/data'
spam_times = {}
dir_path = os.path.dirname(os.path.realpath(__file__))
env = Environment(loader=FileSystemLoader(dir_path))

template = env.get_template('register_commands.html')



def get_movies(id):
  complete_url = f'{GITHUB_URL}/movies.json'
  response = requests.get('https://raw.githubusercontent.com/Alfredocgn/Starwars-DB/main/data/movies.json?token=GHSAT0AAAAAACMI7LHY5Y3JHAFQTDKDJSRCZR5PGIQ',headers=headers)

  if response.status_code == 200:
    data = response.json()
    filtered_movie = [movie for movie in data if movie['episode'] == id]

    if filtered_movie:
      movie_info = []
      for movie in filtered_movie:
          poster_url = f"https://github.com/Alfredocgn/Starwars-DB/blob/40c59582b82281febf458b3b3298cf1c5f85bfa0/images/movies/Episode-{1}.jpg"
          title = movie['title']
          director =  movie['director']
          # poster_url = movie['poster_url']
          release_date = movie['release_date']
          episode = movie['episode']
          movie_info.append(f'{title} episode {episode}\n Was released in {release_date} \n It was directed by {director}')
          movie_info.append(poster_url)
        
      return movie_info
    else:
      return 'Movie not found'
  else:
    return 'Error fetching data'

    
print(get_movies(1))



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
      movie_poster = ['http://images1.wikia.nocookie.net/__cb20130325100645/moviepedia/de/images/4/41/Episode_IV.jpg',
                      'https://picfiles.alphacoders.com/125/125318.jpg',
                      'https://picfiles.alphacoders.com/125/125470.jpg',
                      'https://www.cinemaclock.com/images/posters/1000x1500/59/star-wars-episode-i-the-phantom-menace-1999-us-poster.jpg',
                      'https://image.tmdb.org/t/p/original/4lHY8che2y1veitVjb3SEgppQrY.jpg',
                      'https://www.themoviedb.org/t/p/original/hHg49exUKyuZ2xUFAhVflUrBnvt.jpg']
      movie_info.append(f'{movie_name} {movie_episode}\n Was released in {movie_date} \n It was directed by {movie_director}')
      movie_info.append(movie_poster)
      return movie_info 
    else:
      return 'Movie not found'
  else :
    return 'Error fetching data'

def get_characters(id):
  complete_url = f'{BASE_URL}people/{id}'
  response = requests.get(complete_url)
  if response.status_code == 200:
    data = response.json()
    movie_characters = []

    if 'name' in data:
      character_name = data['name']
      character_height = data['height']
      character_weight = data['mass']
      character_gender = data['gender']
      character_birth_year = data['birth_year']
      character_poster =['https://s-media-cache-ak0.pinimg.com/originals/83/e8/4f/83e84f10599b5d3d0da73e0ff6e14648.jpg',
                          'https://noguiltfangirl.com/wp-content/uploads/2019/11/rise-of-skywalker-c3p0-poster.jpg',
                          'https://images-na.ssl-images-amazon.com/images/I/413HCn8CekL.jpg',
                          'https://dyn1.heritagestatic.com/lf?set=path[1%2F0%2F7%2F0%2F3%2F10703627]&call=url[file:product.chain]',
                          'https://i.pinimg.com/originals/df/71/64/df7164ebac82b47ea7d4aafbe43d00be.jpg',
                          'https://1.bp.blogspot.com/-sPSbnXlh6xc/Xbf2pY1eTMI/AAAAAAAA-R8/dpua40tSeh8b-ITVsp00rQbrEsvmHIbrgCLcBGAsYHQ/s1600/old-obi-wan-kenobi.jpg']
      movie_characters.append(f'Name: {character_name}\n Height: {character_height}cm \n Weight: {character_weight}kg \n Year of Birth {character_birth_year} ')
      movie_characters.append(character_poster)
      return movie_characters
    else:
      return 'Character not found'
  else :
    return 'Error fetching data'


def get_startships(id):
  complete_url = f'{BASE_URL}starships/{id}'
  response = requests.get(complete_url)
  if response.status_code == 200:
    data = response.json()
    starships = []
    

    if 'name' in data:
      ship_name = data['name']
      ship_model = data['model']
      max_speed = data['max_atmosphering_speed']
      ship_crew_capacity = data['crew']
      ship_poster =['https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.2LZUpGrlv1Hqmkvct-ckPAHaDj%26pid%3DApi&f=1&ipt=bda6fa67a78e0d3d5fb1855939f58e4cc24a6db7e8851084f2872a17642476ac&ipo=images',
                    'https://lumiere-a.akamaihd.net/v1/images/Star-Destroyer_ab6b94bb.jpeg?region=0%2C50%2C1600%2C800',
                    'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/657811c3-939d-4d1e-8fa5-d1adbf999420/dg1s5ys-0ce8fdf5-5f5f-45a0-82e1-859ef478ad84.jpg/v1/fill/w_1229,h_650,q_70,strp/sentinel_class_landing_craft___two_view_by_ravendeviant_dg1s5ys-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9ODQ3IiwicGF0aCI6IlwvZlwvNjU3ODExYzMtOTM5ZC00ZDFlLThmYTUtZDFhZGJmOTk5NDIwXC9kZzFzNXlzLTBjZThmZGY1LTVmNWYtNDVhMC04MmUxLTg1OWVmNDc4YWQ4NC5qcGciLCJ3aWR0aCI6Ijw9MTYwMCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.borY5Lr8HOgTxUIbKjyD-emaq4K0zi8R-rqGkyjFPpg',
                    'https://vignette.wikia.nocookie.net/starwars/images/2/2f/Deathstar_negwt.png/revision/latest?cb=20161002160419',
                    'https://www.wallpaperflare.com/static/517/933/283/star-wars-millennium-falcon-millennium-falcon-wallpaper.jpg',
                    'http://img4.wikia.nocookie.net/__cb20070210175842/starwars/images/c/cd/Ywing.jpg']
      starships.append(f'Ship Name: {ship_name}\n Model: {ship_model}\n Max Speed: {max_speed}\n Crew Capacity : {ship_crew_capacity}')
      starships.append(ship_poster)
      return starships
    else:
      return 'Ship not found'
  else:
    return 'Error fetching data'

def handle_spam(user_id):
  if user_id in spam_times:
    spam_time = spam_times[user_id]
    elapsed_time = time.time() - spam_time

    if elapsed_time < 60:
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


def get_entries_from_file():
    entries = []
    with open('register_commands.html', 'r') as file:
        rendered_html = file.read()
        start_tag = '<li>'
        end_tag = '</li>'
        while start_tag in rendered_html and end_tag in rendered_html:
            start_index = rendered_html.find(start_tag)
            end_index = rendered_html.find(end_tag)
            entry_html = rendered_html[start_index:end_index + len(end_tag)]
            parts = entry_html.split(' - ')
            if len(parts) == 4:
                entry = {
                    'date': parts[0][len(start_tag):],
                    'command': parts[1],
                    'user_id': parts[2],
                    'username': parts[3]
                }
                entries.append(entry)
            rendered_html = rendered_html[end_index + len(end_tag):]
    return entries

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
  btn_c3po = InlineKeyboardButton('C3P0',callback_data='C3P0')
  btn_r2d2 = InlineKeyboardButton('R2D2',callback_data='R2D2')
  btn_vader = InlineKeyboardButton('Darth Vader',callback_data='vader')
  btn_leia = InlineKeyboardButton('Leia Organa',callback_data='leia')
  btn_kenobi = InlineKeyboardButton('Obi Wan Kenobi',callback_data='kenobi')
  btn_close = InlineKeyboardButton('Close',callback_data='close')

  markup.add(btn_luke,btn_c3po,btn_r2d2,btn_leia,btn_vader,btn_kenobi,btn_close)
  bot.send_message(message.chat.id,text='Select a Character',parse_mode='MarkdownV2',reply_markup=markup)

@bot.message_handler(commands=['ships'])
def cmd_ships(message):
  if message.chat.id == message.chat.id:
    register_command(message.chat.id, "/ships", message.from_user.username)
  bot.send_chat_action(message.chat.id,'typing')

  markup = InlineKeyboardMarkup(row_width=1)
  btn_corvette = InlineKeyboardButton('CR90 Corvette',callback_data='corv')
  btn_destroyer = InlineKeyboardButton('Star Destroyer',callback_data='destroyer')
  btn_craft = InlineKeyboardButton('Sentinel Landing Craft',callback_data='landing')
  btn_star = InlineKeyboardButton('Death Star',callback_data='star')
  btn_falcon = InlineKeyboardButton('Millenium Falcon',callback_data='falcon')
  btn_y_wing = InlineKeyboardButton('Y-wing',callback_data='y-wing')
  btn_close = InlineKeyboardButton('Close',callback_data='close')

  markup.add(btn_corvette,btn_destroyer,btn_craft,btn_star,btn_falcon,btn_y_wing,btn_close)
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
    movie_episode_to_id = {'e_IV': 1, 'e_V': 2, 'e_VI': 3, 'e_I': 4, 'e_II': 5, 'e_III': 6}
    movie_id = movie_episode_to_id[call.data]

    if cid == cid:
      register_command(cid, f'Button Movie Episode: {call.data}', call.from_user.username)
    star_wars_films = get_movies(movie_id)
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')
    bot.send_photo(cid,star_wars_films[1],caption=star_wars_films[0])
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')
  elif call.data in ['luke','C3P0','R2D2','leia','vader','kenobi']:
    character_name_to_id = {'luke': 1, 'C3P0': 2, 'R2D2': 3,  'vader': 4,'leia': 5, 'kenobi': 10}

    character_id = character_name_to_id[call.data]
    if cid == cid:
      register_command(cid, f'Character Button: {call.data}', call.from_user.username)
    character_info = get_characters(character_id)
    if character_id == 10:
      character_id = 6
    else :
      character_id
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')
    bot.send_photo(cid,character_info[1][character_id-1],caption=character_info[0])
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')

  elif call.data in ['corv','destroyer','landing','star','falcon','y-wing']:
    ship_name_to_id = {'corv':2,'destroyer':3,'landing':5,'star':9,'falcon':10,'y-wing':11}
    ship_id = ship_name_to_id[call.data]
    ship_index = list(ship_name_to_id.values()).index(ship_id)
    if cid == cid:
      register_command(cid, f'Ship Button: {call.data}', call.from_user.username)
    ships_info = get_startships(ship_id)
    bot.send_sticker(cid,'https://t.me/Java_CodificAR/26')
    bot.send_photo(cid,ships_info[1][ship_index],caption=ships_info[0])
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
  




