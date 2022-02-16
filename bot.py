import os
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='$')


uri = "mongodb+srv://cluster0.0l7ve.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
mongoclient = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='certs\X509-cert-3743966135710659102.pem')
db = mongoclient['pokebot']
collection = db['trainers']
doc_count = collection.count_documents({})
print(doc_count)

def getTrainer(trainerId):
    #trainerId = str(trainerId)
    try:
        trainer = db.trainers.find_one({ '_id' : int(trainerId)})
        print(trainer)
    except Exception as e:
        raise
    if trainer is not None:
        return True
    else:
        return False

def registerTrainer(trainerId, dscName):
    try:
        db.trainers.insert_one( { '_id' : int(trainerId), 'dscName' : str(dscName), 'ownedMonsters' : {} } )
    except Exception as e:
        raise


def getPokemon(id):
    api_url = "https://pokeapi.co/api/v2/pokemon/" + id
    pokemon = requests.get(api_url).json()
    return pokemon

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def register(ctx):
    #check if user exists in db
    print(ctx.author.id)
    if getTrainer(ctx.author.id):
        await ctx.send('{} is already registered.'.format(ctx.author.name))
    else:
        await ctx.send('{} is not registered.'.format(ctx.author.name))
        registerTrainer(ctx.author.id, ctx.author.name)
        




@bot.command()
async def pokedex(ctx,id):
    pokemon = getPokemon(id)
    await ctx.send('#{} {} '.format(pokemon['id'], pokemon['name'].capitalize()))

bot.run(TOKEN)








print(response['name'].capitalize())
