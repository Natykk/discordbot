import random
from coinbase.wallet.client import Client
import upload
import discord
from discord.ext import commands
from discord import File
import os
import youtube_dl
import asyncio
players = {}
musics = {}
ytdl = youtube_dl.YoutubeDL()
bot = commands.Bot(command_prefix='!')
import sentry_sdk

def traces_sampler(sampling_context):
    # ...
    # return a number between 0 and 1 or a boolean

  sentry_sdk.init(
    dsn="https://4a3128ca40f849b7b6cbc81853d8e399@o530942.ingest.sentry.io/5650980",

    # To set a uniform sample rate
    traces_sample_rate=1.0,

    # Alternatively, to control sampling dynamically
    traces_sampler=traces_sampler
)

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
for fName in os.listdir('./cogs'):
  if fName.endswith('.py'):
    bot.load_extension(f"cogs.{fName[:-3]}")
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
    embed.add_field(name='!help', value='Donne ce message', inline=False)
    embed.add_field(name='!roll', value='Exemple: !roll <nombre> | Lance un dé ', inline=False)
    embed.add_field(name='!play', value='Exemple: !play <youtube_url> | Joue une video youtube', inline=False)
    embed.add_field(name='!ping', value='Exemple: !ping | Test le temps de reponse', inline=False)
    embed.add_field(name='!addplayer', value='Exemple: !addplayer @nomdujoueur | Ajoute un joueur au jeux du débat', inline=False)
    embed.add_field(name='!intru', value='Exemple: !intru | Lance le jeux du Débat', inline=False)
    embed.add_field(name='!randoom', value='Exemple: !randoom'+"|Tire une image au hasard dans la bibliothèque d\'image", inline=False)
    embed.add_field(name='!ajoutdebat', value='Exemple: !ajoutdebat <debat> | Ajoute un débat dans la liste', inline=False)
    embed.add_field(name='!pfc', value='Exemple: !pfc <0-1-2> | Joué a Pierre-Feuille-Ciseaux en Choisissant un chiffre 0 , 1 ou 2  ', inline=False)
    embed.add_field(name='!gages', value='Exemple: !gages | Tire un gages au hasard dans la liste', inline=False)
    embed.add_field(name='!addgages', value='Exemple: !addgages <le_gages> | Ajoute un gages dans la liste de gages', inline=False)
    embed.add_field(name='!addplayerbmg', value='Exemple: !addplayer @nomdujoueur | Ajoute un joueur au Blanc manger coco', inline=False)    
    embed.add_field(name='!newbmg', value='Exemple: !newbmg | Lance la partie de Blanc manger coco ', inline=False)
    embed.add_field(name='!bmg', value='Exemple: !bmg | Tire une nouvelle carte noir ', inline=False)
    embed.add_field(name='!piochebmg', value='Exemple: !piochebmg <nombre_carte> | Pioche le nombre de carte indiqué ', inline=False)
    embed.add_field(name='!listplayerbmg', value='Exemple: !listplayerbmg | Liste tout les jeux inscrit ', inline=False)
    embed.add_field(name='!listcrypto', value='Example: !listcrypto | affiche la liste des Cryptomonnaie suporté', inline=False)
    embed.add_field(name='!prixcrypto', value='Example: "!prixcrypto <crypto> | Affiche le prix d\'achat et de vente de la Cryptomonnaie"', inline=False)
    embed.add_field(name='!tauxchange', value='Example: "!tauxchange <crypto1> <crypto2> | Affiche de taux de change d\'une Cryptomonnaie par rapport a l\'autre',inline=False)
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


#------------------------------------Gages-----------------------------------------
@bot.command()
async def gages(ctx):
    print("Commande gages Effectué")
    if os.path.exists('gages.txt'):
        lines = open('gages.txt', encoding='utf-8').read().splitlines()
        text = random.choice(lines)
    await ctx.send(text)

@bot.command()
async def addgages(ctx,db=None):
  if db !=None:
    f = open('gages.txt',"a")
    f.write("\n")
    f.write(str(db))
    f.close
  else:
    await ctx.channel.send("Ba alors on arrive pas a écrire ?")

#---------------------------Blanc Manger Coco---------------------------



list_joueur_bmg=[]

@bot.command()
async def addplayerbmg(ctx,user_id=None):
  if user_id != None:
    try:
      target = await bot.fetch_user(user_id)
      list_joueur_bmg.append(int(user_id))
      await ctx.channel.send("Le Joueur: "+target.name+" a été ajouté")
    except:
      await ctx.channel.send("Le joueur n'a pas pu être envoyé.")
  else:
    await ctx.channel.send("Ta pas oublié un truc ?")

@bot.command()
async def clearplayerbmg(ctx):
  list_joueur_bmg.clear()
  print(list_joueur)
  await ctx.channel.send("La Liste de Joueur a été vider")

@bot.command()
async def listplayerbmg(ctx):
  cmp = 0
  for a in list_joueur_bmg[:]:
    listpj = await bot.fetch_user(list_joueur_bmg[cmp])
    await ctx.channel.send(listpj)
    print(list_joueur_bmg)
    cmp +=1

@bot.command()
async def bmg(ctx):
  print("Commande Blanc manger Coco Effectué")
  random.shuffle(list_joueur_bmg) 
  if os.path.exists('./bmg/noir/'):
          image = os.listdir('./bmg/noir/')
          imgString = random.choice(image)
          path = "./bmg/noir/" + imgString
          await ctx.send(file=File(path))
  

@bot.command()
async def newbmg(ctx):
  print("Commande newbmg effectué")
  bmg()
  compteur = 0
  for x in list_joueur_bmg[:]:
    deck = 0
    while deck != 5:
      player = await bot.fetch_user(list_joueur_bmg[compteur])
      image = os.listdir('./bmg/blanc/')
      imgString = random.choice(image)
      path = "./bmg/blanc/" + imgString
      await player.send(file=File(path))
      print("a")
      deck+=1
    compteur += 1
  await ctx.channel.send("Carte Distribué")

@bot.command()
async def piochebmg(ctx,args):
  print("commande Piochebmg effectué")
  for _ in args:
    image = os.listdir('./bmg/blanc/')
    imgString = random.choice(image)
    path = "./bmg/blanc/" + imgString
    await ctx.author.send(file=File(path))

#-------------------------------Crypto Command---------------------------------

client = Client('z05oObIt9hGp0pdC', 'UR8h1c8qxspl5mlmXcPkJrfmhHziEZED')

# build listcrypto of coinbase supported digital currencies
coins = ['BTC', 'LTC', 'BCH', 'ETH', 'ETC', 'BAT', 'ZRX', 'EURC', 'XRP',
        'EOS', 'XLM', 'LINK', 'DASH', 'ZEC', 'REP', 'DAI', 'XTZ']


@bot.command()
async def listcrypto(ctx):

    # return listcrypto of coinbase supported digital currencies
    value = ', '.join(coins)
    embed = discord.Embed(title=value)
    
    await ctx.send(embed=embed)


@bot.command()
async def prixcrypto(ctx, coin):
    # return coin prices

    try:
        coin = coin.upper()
        buy = client.get_buy_price(currency_pair = '{}-EUR'.format(coin))
        sell = client.get_sell_price(currency_pair = '{}-EUR'.format(coin))
        #spot = client.get_spot_price(currency_pair = '{}-EUR'.format(coin))
        buyAmount = buy.get('amount')
        sellAmount = sell.get('amount')
        #spotAmount = spot.get('amount') Prix spot: {2}€
        value = 'Prix d\'achat: {0}€, Prix de Vente: {1}€'.format(buyAmount, 
                                                      sellAmount)
        embed = discord.Embed(title=value)

    except:
        embed = discord.Embed(title='ERROR: Please check your syntax and' +
                                    ' try again', color=0xff0000)

    await ctx.send(embed=embed)



@bot.command()
async def tauxchange(ctx, coin_one, coin_two):
    # return exchange rate from one coin to another

    try:
        coin_one = coin_one.upper()
        coin_two = coin_two.upper()
        getRates = client.get_exchange_rates(currency=coin_one)
        rate = getRates.get('rates').get(coin_two)
        try:
            float(rate)
            value = '1 {0} vaut {1} {2}'.format(coin_one, rate, coin_two)
            embed = discord.Embed(title=value)
        except ValueError:
            embed = discord.Embed(title='Ce que tu fais n\'aucun sense')
    except:
        embed = discord.Embed(title='ERROR: Donnée d\'échange non disponible' + 
                              ' Try again',color=0xff0000)

    await ctx.send(embed=embed)


#---------------------------------------------------------------------------
@bot.command()
async def test(ctx):
    await ctx.send('Salut ! {0}'.format(ctx.author))


upload.keep_alive()
bot.run(os.getenv('TOKEN'))
