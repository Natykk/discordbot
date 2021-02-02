import random
import upload
import music
import discord
from discord.ext import tasks, commands
from discord import File
import os
#import music
import youtube_dl
import asyncio
players = {}
musics = {}
ytdl = youtube_dl.YoutubeDL()

bot = commands.Bot(command_prefix='!')



#--------------------Message de startup et Random Image--------------------------
@bot.event
async def on_ready():
    print("Online:")
    print(bot.user.name)
    print("-------")


@bot.command(name='randoom')
async def randoom(ctx):
    print("Commande randoom Effectué")
    if os.path.exists('textlist.txt'):
        lines = open('textlist.txt', encoding='utf-8').read().splitlines()
        text = random.choice(lines)

        image = os.listdir('./images/')
        imgString = random.choice(image)
        path = "./images/" + imgString

    await ctx.send(file=File(path))
    await ctx.send(text)


#-----------------Ban - Unban - Kick - clear  ---------------------------

@bot.command()
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

@bot.command()
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} à été kick.")

@bot.command()
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()


#-----------------Musique-----------------------------------------
class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def play(ctx, url):
    print("Commande ytb play Effectué")
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        play_song(client, musics[ctx.guild], video)



#------------------------------DM Envoie et Ecoute-------------------------
#-> Envoie
@bot.command()
async def dm(ctx,user_id=None, *, args=None):
  if user_id != None and args != None:
    try:
      target = await bot.fetch_user(user_id)
      await target.send(args)

      await ctx.channel.send("'" + args + "' a été envoyé a: " + target.name)
    except:
      await ctx.channel.send("Le Dm n'a pas pu ètre envoyé.")
  else:
    await ctx.channel.send("Ta pas oublié un truc ?")
  
#-> Ecoute 
@bot.event
async def on_message(message: discord.Message):
    target_srv = bot.get_channel(795780836250091541)
    if message.guild is None and not message.author.bot:
        print(message.content,message.author)
        # if the channel is public at all, make sure to sanitize this first
        await target_srv.send(message.content)
        await target_srv.send(message.author)
    await bot.process_commands(message)
#--------------------------------Jeux Débat--------------------------

list_joueur=[]

@bot.command()
async def addplayer(ctx,user_id=None):
  if user_id != None:
    try:
      target = await bot.fetch_user(user_id)
      list_joueur.append(int(user_id))
      await ctx.channel.send("Le Joueur: "+target.name+" a été ajouté")
    except:
      await ctx.channel.send("Le joueur n'a pas pu être envoyé.")
  else:
    await ctx.channel.send("Ta pas oublié un truc ?")

@bot.command()
async def clearplayer(ctx):
  list_joueur.clear()
  print(list_joueur)
  await ctx.channel.send("La Liste de Joueur a été vider")

@bot.command()
async def listplayer(ctx):
  print(list_joueur)

@bot.command()
async def intru(ctx):
  print("Commande Jeux débat Effectué")
  compteur = 0
  #random.shuffle(list_débat)Vieille methode pour choisir le débat
  random.shuffle(list_joueur) 
  if os.path.exists('debat.txt'):
      lines = open('debat.txt', encoding='utf-8').read().splitlines()
      text = random.choice(lines)  
  target = await bot.fetch_user(list_joueur[-1])
  await target.send("Tu est l'intru !")
  for x in list_joueur[:-1]:
    player = await bot.fetch_user(list_joueur[compteur])
    
    await player.send("Le Débat est : "+str(text) )
    compteur += 1
  await ctx.channel.send("DM Envoyé")
  compteur = 0
  
@bot.command()
async def ajoutdebat(ctx,db=None):
  if db !=None:
    f = open('debat.txt',"a")
    f.write("\n")
    f.write(str(db))
    f.close
  else:
    await ctx.channel.send("Ba alors on arrive pas a écrire ?")
#----------------------Ping----------------------------
@bot.command()
async def ping(ctx):
    print("Commande Ping Effectué")
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))
#-------------------Lancé de Dé----------------------------------
@bot.command()
async def roll(ctx,de=0):
  print("Commande Roll Effectué")
  de_fin = random.randint(0,int(de))
  await ctx.channel.send("Tu est tombé sur "+ str(de_fin) ) 
#-----------------------Help----------------------------------
bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Bot Natyk', description='La liste des commandes sont:', color=0x00D0D0)
    print("Commande Help Effectué")
    #embed.add_field(name='!list', value='Retourne une liste de Cryptomonnaie supporté' + ' Cryptomonnaie', inline=False)
    #embed.add_field(name='!prix', value='Example: "!prix BTC"', inline=False)
    #embed.add_field(name='!exchange', value='Example: "!exchange BTC ETH"',inline=False)
    #embed.add_field(name='!history', value='Example: "!history BTC week."' + ' Les Période d\'utilisation sont par heure,jour,semaines,mois,année',inline=False)
    embed.add_field(name='!help', value='Donne ce message', inline=False)
    embed.add_field(name='!roll', value='Exemple: !roll <nombre> | Lance un dé ', inline=False)
    embed.add_field(name='!play', value='Exemple: !play <youtube_url> | Joue une video youtube', inline=False)
    embed.add_field(name='!ping', value='Exemple: !ping | Test le temps de reponse', inline=False)
    embed.add_field(name='!addplayer', value='Exemple: !addplayer @nomdujoueur | Ajoute un joueur au jeux du débat', inline=False)
    embed.add_field(name='!intru', value='Exemple: !intru | Lance le jeux du Débat', inline=False)
    embed.add_field(name='!randoom', value='Exemple: !randoom'+"|Tire une image au hasard dans la bibliothèque d\'image", inline=False)
    embed.add_field(name='!ajoutdebat', value='Exemple: !ajoutdebat <debat> | Ajoute un débat dans la liste', inline=False)
    embed.add_field(name='!pfc', value='Exemple: !pfc <0-1-2> | Joué a Pierre-Feuille-Ciseaux en Choisissant un chiffre 0 , 1 ou 2  ', inline=False)
    await ctx.send(embed=embed)

#-------------------Pierre feuille Ciseaux------------



@bot.command()
async def pfc(ctx,choix):

  #assign a random play to the computer
  # Pierre - Feuille - Ciseaux
  print("Commande PFC effectué")
  computer = random.randint(0,2)
  #print(computer,"<--- ORDI")
  #print(choix,"<--- choix joueur")
  if choix == computer:
      await ctx.send('Egalité !')
  elif choix == "0":#Pierre
      if computer == 1: #Feuille
          await ctx.send("Perdu ! , La Feuille couvre la Pierre")
      else:
          await ctx.send("Bravo ! ,la Pierre ECRASE les Ciseaux")
  elif choix == "1":#Feuille
      if computer == 2:#ciseaux
          await ctx.send("Et c'est un échec du joueur {0} , les Ciseaux coupent la Feuille".format(ctx.author))
      else:
          await ctx.send("Et c'est gagner ! La Feuille couvre la Pierre")
  elif choix == "2":#ciseaux
      if computer == 0:#Pierre
          await ctx.send("Oh le looser ! La Pierre ECRASE les Ciseaux")
      else:
          await ctx.send("La Win est présente, Les Ciseaux coupent *délicatement* la Feuille")
  else:
    print("On avait dis pas le Puit !")

#-------------------------------------
@bot.command()
async def test(ctx):
    await ctx.send('Salut ! {0}'.format(ctx.author))


upload.keep_alive()
bot.run(os.getenv('TOKEN'))
