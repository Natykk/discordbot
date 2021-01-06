import random
import webpage
import discord
from discord.ext import tasks, commands
from discord import File
import os
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
async def random_gex(ctx):
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
list_débat=["Beurre Doux ou Demi-sel","Céréal Avant ou Après le lait","Pain au Chocolat ou Chocolatine","Les jeux vidéos rendent-ils violent?","Les utilisateurs de trotinettes sont-ils des connards?","En Politique Plutôt Gauche ou droite","pour ou contre Le mariage gay ?","Les Illuminatis sont ils un complot ?","Star Wars contre Star Trek ?","disney contre pixar","qui est le plus fort entre batman ou superman ?","les films en 3D au cinema pour ou contre","pour ou contre la serie lost ? ","est ce que sucer c'est tromper ?","doit on peter devant son conjoint","Tu préfère pleurer en ferrari ou rire sur un velo","Tupac ou Biggie ?","Pas de sujet dite ce que vous voulez","tu prefere savoir comment tu vas mourrir ou quand tu vas mourrir ?","en nage synchronisée, si une nageuse se noie, les autres se noient-elles aussi?"]
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
  compteur = 0
  random.shuffle(list_débat)
  random.shuffle(list_joueur)
  target = await bot.fetch_user(list_joueur[-1])
  await target.send("Tu est l'intru !")
  for x in list_joueur[:-1]:
    print(compteur)
    player = await bot.fetch_user(list_joueur[compteur])
    print(player)
    await player.send("Le Débat est : "+list_débat[2] )
    compteur += 1
    print(compteur)
  await ctx.channel.send("DM Envoyé")
  compteur = 0
  print(compteur)

#----------------------------------------------------------
@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))
#----------------------------------------------------------



#-------------------------------------
@bot.command()
async def test(ctx):
    await ctx.send('Salut ! {0}'.format(ctx.author))


webpage.keep_alive()
bot.run(os.getenv('TOKEN'))
