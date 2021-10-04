''' NOTES
> for the on_message_delete, on_message_edit events and confess bot command to work, $setstaff <channel ID> and $setconf <channel ID> command has to be run manually everytime the bot restarts. Solution- assign the channel automatically, but how? Channel can be assigned in on_ready but it will be hard-coded

> most commands from on_message event have been converted to proper bot commands, you can find them at the end

>create a command with
@client.command()
async def commandname(ctx, *, arg): #or just ctx if no parameters are needed
  #your commands here
  #use ctx.send(your message here) to send messages in the channel

EMBED
  embed_server = discord.Embed(title = "Put title here", description = "Description here")

  fields_server = []

  for name, value, inline in fields_server:
    embed_server.add_field(name = name , value = value, inline = inline)

  await ctx.send(embed = embed_server) 
'''
import discord
import os
import requests
import json
import random
import pypokedex
from discord.ext import commands
import requests
import json
import random
import html
import asyncio
from typing import Optional
from datetime import date
import jikanpy
from jikanpy import Jikan
print("Hello")
Dictionary=dict()
Questions=[]
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ', ':'--..--', '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-'}
MORSE_CODE_DICT1=dict(zip(MORSE_CODE_DICT.values(),MORSE_CODE_DICT.keys())) 
staffch, confch= None, None
confflag= False


intents = discord.Intents.all() #for on_member_join/remove
client=discord.Client()
client= commands.Bot(command_prefix="$", intents= intents) 
client.remove_command('help') #do not remove!! disables the default help msg
Guild = object()


trigger=['fuck']
sad_words=['sad','depressed','udaas']
starter_encouragements=["Cheer up","Hang in there"]
def get_quote():
  response=requests.get('https://zenquotes.io/api/random')
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+' -'+json_data[0]['a']
  return quote
  
@client.event
async def on_ready():
  game = discord.Game("? no, I'm being made(⌒▽⌒)☆")
  await client.change_presence(activity= game, status=discord.Status.online)
  print("We have logged in as {0.user}"
  .format(client))

@client.event
async def on_message(message):
  #moderation : deletes message containing trigger words and informs user through DM
  if any(word.lower() in message.content.lower() for word in trigger):
      if isinstance(message.channel, discord.channel.DMChannel)==False:
        await message.delete()
      User= message.author
      await User.send("That phrase is not allowed!!")
      global confflag
      confflag= True
  msg=message.content
  
  if (msg.startswith!='$morse' and any(word in msg for word in sad_words)):
    await message.channel.send(random.choice(starter_encouragements))


  #dad joke / not optimised. At all.
  if message.content.startswith("I'm") or message.content.startswith("i'm") or message.content.startswith("im") or message.content.startswith("Im"):
    cnn= message.content[3:]
    dadjoke= "Hi "+cnn+" I'm dad!"
    await message.channel.send(dadjoke)

  await client.process_commands(message) #DO.NOT. REMOVE THIS.

#============================================================================
#=========================== END OF ON_MESSAGE ==============================
#============================================================================

@client.event
async def on_message_delete(message): #logs deleted message in assigned staff chat (see: command setlog)
  if staffch== None:
    pass
  else:
    delm= discord.Embed(title= "Deleted Message", colour= discord.Colour.from_rgb(235, 64, 52))
    delm.add_field(name= str(message.author.name)+"#"+str(message.author.discriminator), value= message.content, inline= True)
    await staffch.send(embed= delm)

@client.event
async def on_message_edit(oldMessage, newMessage): #logs edited message in assigned staff chat
  if staffch== None:
    pass
  else:
    editm= discord.Embed(title= "Edited Message by "+str(oldMessage.author), colour= discord.Colour.from_rgb(66, 239, 245))
    editm.add_field(name="Before", value= oldMessage.content, inline= True)
    editm.add_field(name= "After", value= newMessage.content, inline= True)
    await staffch.send(embed= editm)

#============================================================================#
#-------------------------------BOT COMMANDS---------------------------------#
#============================================================================#

#help message ; default is disabled
@client.command()
async def help(ctx):
    embed = discord.Embed(title = 'Categories', description = "Choose category by replying with the desired category number")
    embed_commands = discord.Embed(title = "Commands", description = "Here is the list of commands.")   
    embed_replies = discord.Embed(title = "Replies", description = "Here is the list of replies.")

    fields = [("$hello", "Replies",True),("$inspire", "Sends a quote", False), ("$ping", "returns pong with ms",False),("$morse", "Text to Morse & Morse to Text convertor", False), ("$randomcolour", "Generates a random colour and gives RGB code", False), ("randompokemon", "Gives a random pokemon name with dex info", False), ("$pokedex", "Gives pokedex info of the pokemon entered", False),("$trivia","Asks general knowledge mcq questions",False), ("$user [Aliases: $userinfo]", "Returns user info \n Can take other users as input", False), ("$server [aliases: $serverinfo, $guild, $guildinfo", "Returns server info", False),("$anime [Name]","Gives searched anime details", False)]

    fields2 = [("Bad words", "Deletes the message",True),("Sad words", "Encourages the user", False), ("I'm","Dad",False)]

    fields_categories = [("1. COMMANDS", "Bot commands list",True),("2. REPLIES", "Bot replies", False)]


    for category, category_desc, category_inline in fields_categories:
      embed.add_field(name = category, value = category_desc, inline = category_inline)
    embed.set_author(name = 'Kuchnaya Bot', icon_url ="https://media.tenor.com/images/6f7771dbabe8f7a3711e7121ac166ed3/tenor.gif")
    await ctx.send(embed = embed)

    mreply= await client.wait_for('message')
    if mreply.content=="1" and mreply.author==ctx.author:
        for name, value, inline in fields:
          embed_commands.add_field(name = name, value = value, inline = inline)
          embed_commands.set_author(name = 'Kuchnaya Bot', icon_url ="https://media.tenor.com/images/6f7771dbabe8f7a3711e7121ac166ed3/tenor.gif")
        await ctx.send(embed = embed_commands)
    
    elif mreply.content=="2" and mreply.author==ctx.author:
        for reply_of, replies_with, reply_inline in fields2:
          embed_replies.add_field(name = reply_of, value = replies_with, inline =reply_inline)
          embed_replies.set_author(name = 'Kuchnaya Bot', icon_url ="https://media.tenor.com/images/6f7771dbabe8f7a3711e7121ac166ed3/tenor.gif")
        await ctx.send(embed = embed_replies)

    else:
      await ctx.send("Invalid message!")
#====================== END OF HELP COMMAND ================================

#set log channel
@client.command()
async def setlog(ctx, arg):
  if ctx.author.permissions_in(ctx.channel).administrator== True:
    chID= int(arg)
    global staffch
    staffch= client.get_channel(chID)
    await staffch.send(embed= discord.Embed(title="Settings saved!", colour= discord.Colour.from_rgb(212, 255, 237)))
  else:
    await ctx.send("You do not have enough permissions to use this command.")

@client.command(name='animesearch',aliases=['animeinfo','anime'])
async def animesearch(ctx,*,arg):
  if(arg.lower()=='random'):
    jikan = Jikan()
    Top=jikan.top('anime',page=random.randint(1,20))
    m=random.choice(Top['top'])
    arg=m['title']
  try:
    jikan = Jikan()
    mushishi = jikan.search('anime',arg,page=1)
    Anime=jikan.anime(mushishi['results'][0]['mal_id'])
    image=Anime['image_url']
    synopsis=Anime['synopsis']
    title=Anime['title']
    title_english=Anime['title_english']
    title_japanese=Anime['title_japanese']
    title_synonyms=Anime['title_synonyms']
    episodes=Anime['episodes']
    status=Anime['status']
    score=Anime['score']
    rank=Anime['rank']
    popularity=Anime['popularity']
    trailer_url=Anime['trailer_url']
    g=Anime['genres']
    genres=list(map(lambda x:x['name'],g))
    trailer=Anime['trailer_url']
    url=Anime['url']
    embed_user=discord.Embed(title = title,color=discord.Colour.blue())
    embed_user.set_footer(text = 'Made by Harshvardhan#2278')
    embed_user.set_image(url = image)
    fields_user=[('Rating',score,True),('Rank',rank,True),('Popularity',popularity,True),('Status',status,True),('No of episodes',episodes,True),('Genre',', '.join(genres),False),('MAL link',url,False),("Synopsis:",synopsis[0:1020]+"...",False),('Trailer',trailer,False)]

    for name, value, inline in fields_user:
      embed_user.add_field(name = name , value = value, inline = inline)
    
    await ctx.send(embed = embed_user)
    # await ctx.send("```Synopsis:\n"+synopsis+"```")
  except:
    await ctx.send("Sorry could'nt find that anime in the database")

@client.command(name='mangasearch',aliases=['mangainfo','manga'])
async def mangasearch(ctx,*,arg):
  if(arg.lower()=='random'):
    jikan = Jikan()
    Top=jikan.top('manga',page=random.randint(1,20))
    m=random.choice(Top['top'])
    arg=m['title']
  try:
    jikan = Jikan()
    mushishi = jikan.search('manga',arg,page=1)
    Manga=jikan.manga(mushishi['results'][0]['mal_id'])
    image=Manga['image_url']
    synopsis=Manga['synopsis']
    title=Manga['title']
    title_english=Manga['title_english']
    title_japanese=Manga['title_japanese']
    title_synonyms=Manga['title_synonyms']
    volumes=Manga['volumes']
    chapters=Manga['chapters']
    # episodes=Manga['episodes']
    status=Manga['status']
    score=Manga['score']
    rank=Manga['rank']
    popularity=Manga['popularity']
    g=Manga['genres']
    genres=list(map(lambda x:x['name'],g))
    url=Manga['url']
    spin_off=0
    if('Spin-off' in Manga['related'].keys()):
      spin_off=list(map(lambda x:x['name'],Manga['related']['Spin-off']))
    embed_manga=discord.Embed(title = title,color=discord.Colour.blue())
    embed_manga.set_footer(text = 'Made by Harshvardhan#2278')
    embed_manga.set_image(url = image)
    fields_manga=[]
    if(spin_off!=0):
      fields_manga=[('Rating',score,True),('Rank',rank,True),('Popularity',popularity,True),('Status',status,True),('English Title',title_english,True),('Japanese Title',title_japanese,True),('Genre',', '.join(genres),False),('Spin-offs',', '.join(spin_off),False),('MAL link',url,False),("Synopsis:",synopsis[0:1020]+"...",False)]
    else:
      fields_manga=[('Rating',score,True),('Rank',rank,True),('Popularity',popularity,True),('Status',status,True),('English Title',title_english,True),('Japanese Title',title_japanese,True),('Genre',', '.join(genres),False),('MAL link',url,False),("Synopsis:",synopsis[0:1020]+"...",False)]

    if(volumes!=None):
      fields_manga.insert(len(fields_manga)-3,('Volumes',volumes,True)
      )
    
    if(chapters!=None):
      fields_manga.insert(len(fields_manga)-3,('Chapters',chapters,True)
      )

    for name, value, inline in fields_manga:
      embed_manga.add_field(name = name , value = value, inline = inline)
    
    await ctx.send(embed = embed_manga)

  except:
    await ctx.send("Sorry could'nt find that anime in the database")
  
#morse to text, text to morse conversion
@client.command()
async def morse(ctx, *, arg):
  def encrypyt(a):
        global MORSE_CODE_DICT
        a=' '.join(a.split()).upper()
        M=''
        for x in a:
            if(x==' '):
              M+='/ '
            else:
              M+=MORSE_CODE_DICT[x]+' '
        return M
    
  def decrypt(a):
      global MORSE_CODE_DICT1
      a=a.split()
      M=''
      for x in a:
        if(x=='/'):
          M+=' '
        else:
          M+=MORSE_CODE_DICT1[x]
      return M
  A=' '.join(arg.split())
  if(A.startswith('.') or A.startswith('-')):
      await ctx.channel.send(decrypt(A))
  else:
      await ctx.channel.send(encrypyt(A))

#command description
@client.command()
async def pokedex(ctx, *, arg):
  pokemon_input=' '.join(arg.split())
  print(pokemon_input)
  pokemon = pypokedex.get(name = pokemon_input)
  pokemon_name = pokemon.name
  pokemon_pokedex_number = pokemon.dex
  pokemon_sprites = pokemon.sprites
  pokemon_sprites_dictionary =pokemon_sprites[0]
  pokemon_sprites_img = pokemon_sprites_dictionary["default"]
  embed_randompokemon = discord.Embed(title = pokemon_name)
  embed_randompokemon.set_image(url = pokemon_sprites_img)
  fields_randompokemon = [("Pokemon Name", pokemon_name, False), ("Pokedex Number", pokemon_pokedex_number, False)]
  for name, value, inline in fields_randompokemon:
    embed_randompokemon.add_field(name = name , value = value, inline = inline)

  await ctx.send(embed = embed_randompokemon)

#command description
@client.command()
async def randompokemon(ctx):
  randompokemon = random.randint(1,898)
  pokemon = pypokedex.get(dex=randompokemon)
  pokemon_name = str(pokemon.name).title()
  pokemon_pokedex_number = pokemon.dex
  pokemon_sprites = pokemon.sprites
  pokemon_sprites_dictionary =pokemon_sprites[0]
  pokemon_sprites_img = pokemon_sprites_dictionary["default"]
  embed_randompokemon = discord.Embed(title = pokemon_name)
  embed_randompokemon.set_image(url = pokemon_sprites_img)
  fields_randompokemon = [("Pokemon Name", pokemon_name, False), ("Pokedex Number", pokemon_pokedex_number, False)]
  for name, value, inline in fields_randompokemon:
    embed_randompokemon.add_field(name = name , value = value, inline = inline)

  await ctx.send(embed = embed_randompokemon)

#command description
@client.command()
async def randomcolour(ctx):
    randomred = random.randint(0,255)
    randomblue = random.randint(0,255)
    randomgreen = random.randint(0,255)
    rgb = discord.Colour.from_rgb(randomred, randomgreen, randomblue)
    await ctx.send("**R: **" + str(randomred) +", **G: **" + str(randomgreen)+" ,** B: **" + str(randomblue))
    embed_rgb= discord.Embed(title= "Here is a random generated colour", colour= rgb)
    await ctx.send(embed = embed_rgb)

#command description
@client.command()
async def hello(ctx):
  a="Hello "+str(ctx.author.name)
  await ctx.send(a)

#command description
@client.command()
async def inspire(ctx):
  a=get_quote()
  await ctx.send(a)

#command description
@client.command()
async def ping(ctx):
  await ctx.send(f'`Pong!!!! Time taken: {round(client.latency * 1000)}ms`')

#anonymous confession
@client.command()
async def confess(ctx, *, arg):
  if isinstance(ctx.channel, discord.channel.DMChannel):
    global confflag
    conf= discord.Embed()
    conf.add_field(name= "anon's confession", value= arg, inline= True)
    if confch== None:
      await ctx.author.send("Looks like a confession channel has not been set!")
    elif confflag==False:
      await confch.send(embed= conf)
    confflag= False
  else:
    await ctx.message.delete()
    await ctx.send("Oops! Send your confession through my DM!")

#set confession channel
@client.command()
async def setconf(ctx, arg):
  if ctx.author.permissions_in(ctx.channel).administrator== True:
    global confch
    confch= client.get_channel(int(arg))
    setm= discord.Embed(title= "All confessions will be sent here!")
    await confch.send(embed= setm)
  else:
    await ctx.send("You don't have enough permissions to use this command")



@client.command(aliases= ['TRIVIA'])
async def trivia(ctx):

  Dict=dict()
  global counter
  if(ctx.author.id not in Dictionary.keys()):
    Dictionary[ctx.author.id]=[0,[]]
  
  correct=''
  def Run():
    Dict.clear()
    n=1
    response=html.unescape(requests.get("https://opentdb.com/api.php?amount=50&difficulty=easy&type=multiple"))
    json_data=json.loads(response.text)
    A=random.choice(json_data['results'])
    Question=html.unescape(A['question'])
    correct=html.unescape(A['correct_answer'])
    incorrect=html.unescape(A['incorrect_answers'])
    total=set(incorrect+[correct])
    
    n=1
    Embed=discord.Embed(title=Question,description='')
    for x in total:
        Dict[n]=x
        n+=1
    fields=[]
    if(Question in Dictionary[ctx.author.id][1]):
      return Embed,correct
    Dictionary[ctx.author.id][1].append(Question)
    for x,y in Dict.items():
      fields.append((str(x)+'. '+html.unescape(y),False))
    for category, category_inline in fields:
      Embed.add_field(name = category, value ='‎ ', inline =    category_inline)
    return Embed, correct
  Embed, correct= Run()
  await ctx.send(embed= Embed)
  try:
    INPUT= await client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30)
    INPUT=int(INPUT.content)
  except asyncio.TimeoutError:
    await ctx.send("Time out! Your score:"+str(Dictionary[ctx.author.id][0]))
    del Dictionary[ctx.author.id]
  except ValueError:
    if (INPUT.content.lower()== "$stop" or INPUT.content.lower()== "stop"):
      await ctx.send("Stopped. Your score= "+str(Dictionary[ctx.author.id][0]))
      del Dictionary[ctx.author.id]
      Dictionary[ctx.author.id]=0
    elif(INPUT.content.lower()== "$score" or INPUT.content.lower()== "score"):
      await ctx.send("Score: "+str(Dictionary[ctx.author.id][0]))
      await asyncio.sleep(1)
      await trivia(ctx)
    else:
      await ctx.send('Invalid option\n'+'Correct answer is '+correct)
      await asyncio.sleep(1)
      await trivia(ctx)
  else:
    if(INPUT not in Dict.keys()):
      await ctx.send('Invalid option\n'+'Correct answer is '+correct)
      await asyncio.sleep(1)
      await trivia(ctx)
    elif(Dict[INPUT]==correct):
      await ctx.send('Right answer')
      Dictionary[ctx.author.id][0]+=1
      await asyncio.sleep(1)
      await trivia(ctx)
    elif(Dict[INPUT]!=correct):
      await ctx.send('Wrong answer\n'+' Correct answer is '+correct)
      await asyncio.sleep(1)
      await trivia(ctx)

@client.command()
async def welcomemessage(ctx, *, arg):
  arg= arg[2:-1]
  channel_input=' '.join(arg.split())

  print(arg)
  @client.event
  async def on_member_join(member):
    #if not member.bot:
    print("event triggered")
    welch= client.get_channel(channel_input)
    await welch.send(f'Welcome {member.mention}! Check the rules at <#818566075595358270>')
    rank = discord.utils.get(member.guild.roles, name='member')
    await member.add_roles(rank)
      # autoroles = member.guild.get_role(819239399706591253)
      # await member.add_roles(autoroles)
      #else:
    print("skipped", member.bot)

@client.event
async def on_member_remove(member):
  print("leave triggered")
  await client.get_channel(819233804081561601).send(f"{member.mention} left the server <:pepehands:818544074445291581>  !")

@client.command()
async def verify(ctx):
  role= ctx.guild.get_role(819239399706591253)
  await ctx.author.add_roles(role)

def np(user):
  userA= list(user.activities)
  nonef= True
  try:
    for a in userA:
      if "Spotify"==a.name:
        return (str(a.title)+" by "+str(a.artist))
        nonef= False
  except:
    pass
  if nonef:
    return "No song playing"

def game(user):
  userA= list(user.activities)
  nonef = True
  try:
    for a in userA:
      if a.name!="Spotify" and a.type!=discord.ActivityType.custom:
        return (str(a.name))
        nonef= False
  except:
    pass
  if nonef:
    return "None"


def getrole(roles):
  rolename= ""
  for a in range(len(roles)-1):
    rolename+= str(roles[a].mention)+", "
  rolename+=str(roles[-1].mention)
  return rolename

@client.command(name = "user", aliases = ["userinfo"])
async def user(ctx, target: Optional[discord.Member]):
  target = target or ctx.author
  embed_user = discord.Embed(title = "User Info")
  embed_user.set_thumbnail(url = target.avatar_url)
  embed_user.set_author(name=target , icon_url = target.avatar_url)
  spotify= np(target)
  game_activity = game(target)
  userroles= getrole(list(target.roles))
  fields_user = [("Name",target, True),
  ("Server Nickname", target.nick, True),
  ("Bot", target.bot, True),
  ("User ID", target.id, True),
  ("Game activity", game_activity, True),
  ("Online/Do Not Disturb/Idle/Offline Status",
  str(target.status).title(), True),
  ("Spotify", spotify, True),
  ("No. of roles", len(target.roles) - 1, True),
  ("List of roles", userroles, True),
  ("Discord joined on",str(target.created_at)[0:10], True),
  ("Server joined at", str(target.joined_at)[0:10], True),
  ("On mobile", target.is_on_mobile(), True)]
  
  for name, value, inline in fields_user:
    embed_user.add_field(name = name , value = value, inline = inline)

  await ctx.send(embed = embed_user) 

@client.command(name = "server", aliases = [("serverinfo"), ("guild"), ("guildinfo")])
async def server(ctx):
  embed_server = discord.Embed(title = "Server Info")
  embed_server.set_thumbnail(url=ctx.guild.icon_url)
  embed_server.set_author(name=ctx.guild.name, icon_url = ctx.guild.icon_url)
  serverroles= getrole(list(ctx.guild.roles))

  statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
	len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
	len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
	len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

  fields_server = [("Name", ctx.guild.name,True),
  ("ID",ctx.guild.id, True),
  ("Region", str(ctx.guild.region).title(), True),
  ("Owner Name",ctx.guild.owner,True),
  ("Owner ID", ctx.guild.owner_id, True),
  ("Created at", str(ctx.guild.created_at)[0:10],True),
  ("Total Members", len(ctx.guild.members), True),
  ("No. of Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
  ("No. of Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
	("No. of text channels", len(ctx.guild.text_channels), True),
	("No. of voice channels", len(ctx.guild.voice_channels), True),
	("No. of categories", len(ctx.guild.categories), True),
	("No. of roles", len(ctx.guild.roles), True),
  ("List of roles", serverroles, True),
  ("Status", f'Online: {statuses[0]}\n Idle: {statuses[1]}\n Do Not Disturb: {statuses[2]}\n Offline: {statuses[3]}', True)]

  for name, value, inline in fields_server:
    embed_server.add_field(name = name , value = value, inline = inline)

  await ctx.send(embed = embed_server) 

#===================== more moderation stuff =========================
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  if staffch== None:
      await ctx.send(f'User {member} has been banned!')
  else:
    await staffch.send(f'User{member} has been banned!')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  if staffch== None:
    await ctx.send(f'User {member} has been banned!')
  else:
    await staffch.send(f'User {member} has been banned!')

client.run(os.getenv('TOKEN'))