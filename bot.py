import os
import requests
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
from pymongo import MongoClient
import asyncio



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#client = discord.Client()
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

startingPokemons = {'#1': 'Bulbasaur', '#4': 'Charmander', '#7' : 'Squirtle'}

def getPokemon(id):
    api_url = "https://pokeapi.co/api/v2/pokemon/" + id
    pokemon = requests.get(api_url).json()
    return pokemon

def randomizePokemon():
    pass

def capturePokemon():
    pass

def chooseStartingPokemon(id):
    chosenP = getPokemon(id)
    if chosenP['name'].capitalize() in startingPokemons.values():
        return chosenP
    else:
        return 'ERROR'


class PokeClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return


        if message.content.startswith('$register'):
            if getTrainer(message.author.id):
                await message.channel.send('{}, you are already registered!'.format(message.author.name) )

            else:
                await message.channel.send('Welcome {}! Please choose your first companion:\n {}'.format(message.author.name,'\n'.join('{} {}'.format(key, value) for key, value in startingPokemons.items())))

                def is_correct(m):
                    return m.author == message.author

                try:
                    option = await self.wait_for('message', check=is_correct, timeout=5.0)
                    choosenPokemon = chooseStartingPokemon(option.content)
                except asyncio.TimeoutError:
                    return await message.channel.send(f'Sorry, you took too long.')


                if choosenPokemon != 'ERROR':
                    await message.channel.send('Yay! You got a young {}'.format(choosenPokemon['name'].capitalize()))
                    print(choosenPokemon)
                else:
                    await message.channel.send('Sorry, that is not a valid Pokemon.')
                    print(choosenPokemon)
                # registerTrainer(message.author.id, message.author.name)



        if message.content.startswith('$guess'):
            await message.channel.send('Guess a number between 1 and 10.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long it was {answer}.')

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send(f'Oops. It is actually {answer}.')


@bot.command()
async def pokedex(ctx,id):
    pokemon = getPokemon(id)
    await ctx.send('#{} {} '.format(pokemon['id'], pokemon['name'].capitalize()))

client = PokeClient()
client.run(TOKEN)
