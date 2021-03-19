import discord
import selenium
import requests
import json
import random
from discord.ext import tasks
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import hashlib
import urllib
import urllib.request
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime
import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from keep_alive import keep_alive
print("Running Program...")

class CleverBot:
	def __init__(self):
		global cleverBotActive
		cleverBotActive = False
		print("Creating CleverBot...")
		self.element = None
		options = Options()
		options.add_argument("--headless")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--no-sandbox")
		print("Starting Firefox")
		self.wd = webdriver.Firefox(options=options)
		self.wd.set_page_load_timeout(15)
		print("CleverBot Created")
		cleverBotActive = True
	def init(self):
		global cleverBotActive
		cleverBotActive = False
		print("Starting CleverBot....")
		self.wd.get("https://www.cleverbot.com/")
		print("At CleverBot.com")
		self.fastrack = WebDriverWait(self.wd, 1.5).until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div/form/input")))
		self.wd.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/form/input").click()
		self.fastrack = WebDriverWait(self.wd, 1.5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "input.stimulus")))
		self.textbox = self.wd.find_element_by_css_selector("input.stimulus")
		cleverBotActive = True
		print("CleverBot is Now Running")
	def getResponse(self, text):
		global cleverBotActive
		self.textbox.send_keys(text)
		self.textbox.submit()
		time.sleep(0.5)
		self.textField = self.wd.find_element_by_css_selector("#line1 > span.bot")
		WebDriverWait(self.wd, 6).until(lambda wd: len(wd.find_element_by_css_selector("#line1 > span.bot").text) > 1)
		time.sleep(3)
		return self.textField.text
	def close(self):
		global cleverBotActive
		cleverBotActive = False
		self.wd.quit()
		print("Bot Shut Down")
	def reset(self):
		global cleverBotActive
		cleverBotActive = False
		self.wd.refresh()
		self.fastrack = WebDriverWait(self.wd, 1.5).until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div/form/input")))
		self.wd.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/form/input").click()
		self.fastrack = WebDriverWait(self.wd, 1.5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "input.stimulus")))
		self.textbox = self.wd.find_element_by_css_selector("input.stimulus")
		cleverBotActive = True
		print("Bot Restarted")
ttt = None
class TicTacToe:
	def __init__(self, Pl1, Pl2):
		self.tttGridNums = ['Page1:810960373082750976', 'Page2:810960372857045052', 'Page3:810960372877230171', 'Page4:810960372898070548', 'Page5:810960372902658048', 'Page6:810960373041594428', 'Page7:810960372973961248', 'Page8:810960373128757258', 'Page9:810960372991000596']
		self.tttCross = "<:PageX:810960373103722496>"
		self.tttCircle = "<:PageO:810960373066104892>"
		self.reset()
		self.tttPlCross = Pl1
		self.tttPlCircle = Pl2
	async def join(self, Pl2, message):
		self.tttPlCircle = Pl2
		self.tttCur = self.tttCircle
		self.tttCurPl = self.tttPlCircle
		self.tttNextPl = self.tttPlCross
		self.tttNext = self.tttCross
		self.embed = self.updateGrid()
		self.tttGrid = await message.channel.send(embed=self.embed)
		for i in range(len(self.tttGridArr)):
			await self.tttGrid.add_reaction(self.tttGridNums[i])
	def reset(self):
		self.tttPlCross = None
		self.tttPlCircle = None
		self.tttGrid = None
		self.tttTurn = 0
		self.tttGridArr = self.tttGridNums
		for i in range(len(self.tttGridArr)):
			self.tttGridArr[i] = "<:"+self.tttGridNums[i]+">"
	async def update(self, reaction, user):
		if reaction.message == self.tttGrid:
			if (self.tttTurn % 2 == 0 and self.tttPlCross == user.id) or (
					self.tttTurn % 2 == 1 and self.tttPlCircle == user.id):
				self.tttCurPl = self.tttPlCross
				self.tttCur = self.tttCross
				self.tttNextPl = self.tttPlCircle
				self.tttNext = self.tttCircle
				if self.tttTurn % 2 == 0:
					self.tttCur = self.tttCross
					self.tttCurPl = self.tttPlCross
					self.tttNextPl = self.tttPlCircle
					self.tttNext = self.tttCircle
				else:
					self.tttCur = self.tttCircle
					self.tttCurPl = self.tttPlCircle
					self.tttNextPl = self.tttPlCross
					self.tttNext = self.tttCross
				for i in range(len(self.tttGridArr)):
					if str(self.tttGridNums[i]) == str(reaction):
						self.tttGridArr[i] = str(self.tttCur)
						self.tttTurn += 1
				self.embed = self.updateGrid()
				self.tttGrid = await reaction.message.channel.send(embed=self.embed)
				for i in range(3):
					if self.tttGridArr[0 + i * 3] == self.tttGridArr[1 + i * 3] and self.tttGridArr[0 + i * 3] == \
							self.tttGridArr[2 + i * 3]:
						await self.win(reaction.message, f"{self.tttCur} <@{self.tttCurPl}> Won!")
						return
				for i in range(3):
					if self.tttGridArr[0 * 3 + i] == self.tttGridArr[1 * 3 + i] and self.tttGridArr[0 * 3 + i] == \
							self.tttGridArr[2 * 3 + i]:
						await self.win(reaction.message, f"{self.tttCur} <@{self.tttCurPl}> Won!")
						return
				if (self.tttGridArr[0] == self.tttGridArr[4] and self.tttGridArr[0] == self.tttGridArr[8]) or (
						self.tttGridArr[2] == self.tttGridArr[4] and self.tttGridArr[2] == self.tttGridArr[6]):
					await self.win(reaction.message, f"{self.tttCur} <@{self.tttCurPl}> Won!")
					return
				q = 0
				for i in range(len(self.tttGridArr)):
					if self.tttGridArr[i] != self.tttCross and self.tttGridArr[i] != self.tttCircle:
						q += 1
						await self.tttGrid.add_reaction(self.tttGridNums[i])
					elif i >= 8 and q == 0:
						await self.win(reaction.message, f"No More Moves Can be Made! Tie!")
						return
	def updateGrid(self):
		embed = discord.Embed(title="Tic Tac Toe",
							description=f"{self.tttGridArr[0]}{self.tttGridNums[1]}{self.tttGridArr[2]}\n{self.tttGridArr[3]}{self.tttGridArr[4]}{self.tttGridArr[5]}\n{self.tttGridArr[6]}{self.tttGridArr[7]}{self.tttGridArr[8]}\n\n{self.tttNext} <@{self.tttNextPl}>'s Move",
							color=0xffffff)
		return embed
	async def win(self, message, message_str):
		await message.channel.send(message_str)
		self.reset()
cycle_embed = None
class Embed:
	def __init__(self, arrow_left, arrow_right):
		self.arrow_left = arrow_left
		self.arrow_right = arrow_right
		self.index = 0
		self.embed = None
	async def cycle(self, reaction):
		if reaction.message == self.embed:
			if str(reaction) == "<:"+self.arrow_left+">":
				self.index -= 1
				if self.index < self.min_index:
					self.index = self.max_index
				await self.func(self.message, self.new_message, self.index)
			elif str(reaction) == "<:"+self.arrow_right+">":
				self.index += 1
				if self.index > self.max_index:
					self.index = self.min_index
				await self.func(self.message, self.new_message, self.index)
	async def naruto(self, message, new_message, index):
		argument = new_message.partition("naruto ")[2]
		character = argument
		village = ""
		page = 1
		villages = ["cloud", "grass", "springs", "leaf", "mist", "flower", "rain", "sand", "sound", "star", "rock", "waterfall", "tides"]
		for i in range(len(villages)):
			if argument.startswith(villages[i]):
				village = villages[i]
				character = ""
		if argument == "" or argument == " " or argument == "random":
			character = ""
			village = ""
			page = random.randint(1, 12)
		query = '''
{
  characters(page: 1, filter: {name: "pain", village: "leaf"}) {
    results {
      name
      avatarSrc
      description
      rank
      village
      age
    }
  }
}
					'''
		query = query.replace("pain", character)
		query = query.replace("leaf", village)
		query = query.replace("1", str(page))
		query = gql(query)
		transport = RequestsHTTPTransport(url="https://narutoql.com/graphql", use_json=True)
		client = Client(transport=transport, fetch_schema_from_transport=True)
		response_query = client.execute(query)
		self.max_index = len(response_query["characters"]["results"]) - 1
		if argument == "" or argument == " " or argument == "random":
			index = random.randint(0, self.max_index)
			self.index = index
		name = response_query["characters"]["results"][index]["name"]
		description = response_query["characters"]["results"][index]["description"]
		picture = response_query["characters"]["results"][index]["avatarSrc"]
		rank = response_query["characters"]["results"][index]["rank"]
		village = response_query["characters"]["results"][index]["village"].title()
		age = response_query["characters"]["results"][index]["age"]
		if age == "" or age == None:
			age = "No Data"
		if rank == "" or rank == None:
			rank = "No Data"
		if self.embed != None:
			await self.embed.delete()
		embed = discord.Embed(title=name,
							  description=description,
							  color=0xea9828)
		embed.set_author(name=village)
		embed.set_thumbnail(url=picture)
		embed.add_field(name="Age", value=age, inline=True)
		embed.add_field(name="Rank", value=rank, inline=True)
		embed.set_footer(text="Naruto and Naruto Shippuden")
		embed_sent = await message.channel.send(embed=embed)
		self.message = message
		self.new_message = new_message
		self.func = self.naruto
		self.min_index = 0
		self.embed = embed_sent
		self.embed_to_send = embed
		if self.max_index > 0:
			await embed_sent.add_reaction(self.arrow_left)
			await embed_sent.add_reaction(self.arrow_right)
	async def pokemon(self, message, new_message, index):
		if index != 0:
			argument = str(index)
		else:
			argument = new_message.replace(" ", "").partition("okemon")[2]
		base_url = "https://pokeapi.co/api/v2/pokemon/"
		lastPokemon = 898
		url = base_url
		if (argument == "" or argument == "random"):
			ranMon = random.randrange(1, lastPokemon)
			url = base_url + str(ranMon)
		else:
			url = base_url + argument
		response = requests.get(url)
		json_data = json.loads(response.text)
		gamesprite = json_data['sprites']['front_default']
		sprite = json_data['sprites']['other']['official-artwork'][
			'front_default']
		name = json_data['name'].capitalize()
		pokeid = json_data['id']
		self.index = pokeid
		poketype1 = json_data['types'][0]['type']['name'].capitalize()
		poketype2 = " "
		if (len(json_data['types']) == 2):
			poketype2 = json_data['types'][1]['type']['name'].capitalize()
			poketype2 = ", " + poketype2
		hp = json_data['stats'][0]['base_stat']
		attack = json_data['stats'][1]['base_stat']
		defense = json_data['stats'][2]['base_stat']
		special_attack = json_data['stats'][3]['base_stat']
		special_defense = json_data['stats'][4]['base_stat']
		speed = json_data['stats'][5]['base_stat']
		total = hp + attack + defense + special_attack + special_defense + speed
		if self.embed != None:
			await self.embed.delete()
		embed = discord.Embed(title=name + " #" + str(pokeid), description=poketype1 + poketype2, color=0xffffff)
		embed.set_thumbnail(url=sprite)
		embed.add_field(name="HP", value=hp, inline=True)
		embed.add_field(name="Attack", value=attack, inline=True)
		embed.add_field(name="Defense", value=defense, inline=True)
		embed.add_field(name="Sp. Atk", value=special_attack, inline=True)
		embed.add_field(name="Sp. Def", value=special_defense, inline=True)
		embed.add_field(name="Speed", value=speed, inline=True)
		embed.add_field(name="Total", value=total, inline=False)
		embed_sent = await message.channel.send(embed=embed)
		self.message = message
		self.new_message = new_message
		self.func = self.pokemon
		self.min_index = 1
		self.max_index = lastPokemon
		self.embed = embed_sent
		self.embed_to_send = embed
		await embed_sent.add_reaction(self.arrow_left)
		await embed_sent.add_reaction(self.arrow_right)
cb = CleverBot()
bot = discord.Client()
bot_name = "name"
bot_id = "id"
bot_id_full = "<@!id>"

def write_doc(_directory, _id, _type, _sender, _message, _date):
	file1_name = str(_type) + ".txt"
	if not os.path.exists(defaultPath):
		os.makedirs(defaultPath)
	path1 = f"{defaultPath}/{str(_directory)}"
	if not os.path.exists(path1):
		os.makedirs(path1)
	path1 = f"{path1}/{str(_id)}"
	if not os.path.exists(path1):
		os.makedirs(path1)
	file1 = open(f"{path1}/{file1_name}", "a")
	date_time = datetime.fromtimestamp(time.time())
	if _date:
		file1.write(str(date_time) + ": " + str(_sender) + ": " + str(_message))
		file1.write('\n')
	else:
		file1.write('\n')
		file1.write(str(_message))
	file1.close()
def read_doc(_directory, _id, _type, _sender, _default_setting):
	file1_name = str(_type) + ".txt"
	if not os.path.exists(defaultPath):
		os.makedirs(defaultPath)
	path1 = f"{defaultPath}/{str(_directory)}"
	if not os.path.exists(path1):
		os.makedirs(path1)
	path1 = f"{path1}/{str(_id)}"
	if not os.path.exists(path1):
		os.makedirs(path1)
	try:
		with open(f"{path1}/{file1_name}", 'r') as f:
			lines = f.read().splitlines()
			last_line = lines[-1]
			return last_line
	except: 
		file1 = open(f"{path1}/{file1_name}", "a")
		file1.write(_default_setting)
		return _default_setting
async def change_activity(_status):
	rand = random.randrange(0,3)
	if rand == 0:
		movies = ["Shrek", "'the hub'","Bee Movie", "My Glass of Milk", "Sonic the Hedgehog but with the Original Design", "Cats the Musical", "My Stonks, Stressfully","Emoji Movie", "the Endless Abyss", "Killer Bean", "Whale's Videos", "Смешарики (funny balls)", "Hedgehog Sneezing", "monkes eatin banananas", "my nuggets spin in the microwave", "you from your closet", "XIA Tech, SolidState is Silly", "Veggie Tales", "Intersting Pictures on DeviantArt", "Human Centipede"]
		rand = random.randrange(0,len(movies))
		await bot.change_presence(status=_status, activity=discord.Activity(type=discord.ActivityType.watching, name=movies[rand]))
	elif rand == 1:
		games = ["Minceraft", "Minecraft", "Roblox", "Happy Wheels", "In Silence", "Drums", "Saxaphone", "Otamatone", "Cards with Papa Stalin", "Breath of the Wild", "Ur mom","a Theme of a Funny Skeleton", "Russian Roulette", "Operation Cobra", "on PC 2", "Plague Inc. on a Cursed Computer I Found in a Dumpster", "18+ Truth or Dare with Children", "Free For All", "Tower Defense with HOLES", "Rock Paper Scissors Against Myself in the Mirror. I'm lossing :(", "Forknife", "Shrek Smash n' Crash Racing on PSP", "Twitter"]
		rand = random.randrange(0,len(games))
		await bot.change_presence(status=_status, activity=discord.Game(name=games[rand]))
	elif rand == 2:
		music = ["Revenge", "Loonboon", "Bonetrousle", "Паровозик тыр-тыр-тыр", "Mr.Bean Theme Song", "Christian Cat", "Diamonds are Unbreakable", "Shreksaphone", "Brother Screaming", " the silence in my empty lifeless room", "Nothing, I am Crying Under my Table", "a̴̢̬̕ş̵͇̅͠d̵̨̔n̵̪͋k̸̰̍̓j̶̞̍f̷̩̻̒n̷̙̼̊a̶̭͕͐͆k̸̛̻̚j̶͍̏̃f̴̨̊̕k̸̥͍̒̉", "Africa by Toto", "10 Hours of Walking Polar Bear", "[K A R L S O N V I B E]", "Tech Pit Podcasts", "Metal Crusher, i honestly feel like i am not even a human sometimes 😂", "1700s Sea Shanties", "BattleBlock Theater Music", "cat by C418", "Guardian Battle while running to Hyrule Castle", "Monopoly"]
		rand = random.randrange(0,len(music))
		await bot.change_presence(status=_status, activity=discord.Activity(type=discord.ActivityType.listening, name=music[rand]))
@tasks.loop(seconds=300)
async def testCleverBotConnection():
	global cleverBotActive
	global cb
	try:
		print("Testing CleverBot Connection")
		write_doc("CleverBot", bot.user.id, "Status", "", "\n", True)
		write_doc("CleverBot", bot.user.id, "Status", "", "Testing CleverBot Connection", True)
		response = cb.getResponse("hello")
	except:
		print("Test Failed")
		write_doc("CleverBot", bot.user.id, "Status", "", "Test Failed", True)
		cleverBotActive=False
		await change_activity(discord.Status.idle)
		try:
			cb.init()
		except TimeoutException:
			print("Could Not Start CleverBot, Connection TimeOut")
			write_doc("CleverBot", bot.user.id, "Status", "", "Could Not Start CleverBot, Connection TimeOut", True)
			await change_activity(discord.Status.idle)
		except WebDriverException:
			print("Could Not Start CleverBot, WebDriverException")
			write_doc("CleverBot", bot.user.id, "Status", "", "Could Not Start CleverBot, WebDriverException, Creating New CleverBot", True)
			await change_activity(discord.Status.idle)
			try:
				cb = CleverBot()
			except:
				print("Creation Failed")
				write_doc("CleverBot", bot.user.id, "Status", "", "Creation Failed", True)
			else:
				print("Creation Succeeded, Launching CleverBot")
				write_doc("CleverBot", bot.user.id, "Status", "", "Creation Succeeded, Launching ", True)
		else:
			write_doc("CleverBot", bot.user.id, "Status", "", "CleverBot Started", True)
			write_doc("CleverBot", bot.user.id, "Status", "", "Could Not Start CleverBot, Connection TimeOut", True)
			await change_activity(discord.Status.online)
	else:
		print("Test Succeeded")
		write_doc("CleverBot", bot.user.id, "Status", "", "Test Succeeded", True)
		cleverBotActive=True
		await change_activity(discord.Status.online)
@bot.event
async def on_ready():
	print("Logged on as {0.user}".format(bot))
	global bot_name
	global bot_id
	global bot_id_full
	bot_name = "{0.user}".format(bot)
	bot_id = str(bot.user.id)
	bot_id_full = "<@!"+bot_id+">"
	global tttPlCircle
	global tttGrid
	tttPlCircle = None
	tttGrid = None
	print("Bot's ID: " + bot_id_full)
	#cb.init()
	try:
		testCleverBotConnection.start()
		print("TestCleverBotConnection Task is Now Running")
		write_doc("CleverBot", bot.user.id, "Status", "", "TestCleverBotConnection Task is Now Running", True)
	except RuntimeError:
		print("Tried to Launch testCleverBotConnection.start() Again")
		write_doc("CleverBot", bot.user.id, "Status", "", "Tried to Launch testCleverBotConnection.start() Again", True)
@bot.event
async def on_reaction_add(reaction, user):
	if user.bot:
		return
	if ttt != None:
		await ttt.update(reaction, user)
	if cycle_embed != None:
		await cycle_embed.cycle(reaction)
@bot.event
async def on_message(message):
	write_doc("Channels", message.channel.id, "General", message.author.name + " (<@" + str(message.author.id)+">)", message.content, True)
	write_doc("Users", str(message.author.id)+" - " + message.author.name, "General", message.author.name, message.content, True)
	global prefix
	global cleverBotActive
	global cleverBotEnabled
	global cycle_embed
	prefix = read_doc("Channels", message.channel.id, "Prefix", "", "!")
	cleverBotEnabled = read_doc("Channels", message.channel.id, "FreeSpeech", "", "True")
	if message.author.bot:
		return
	_new_message = message.content
	new_message = _new_message.lower()
	print(message.author.name + " (<@" + str(message.author.id)+">): " + _new_message)
	if(new_message.startswith(bot_id_full)):
		new_message = new_message.replace(bot_id_full, prefix)
		_new_message = new_message
	if new_message.startswith(prefix) or prefix == "":
		write_doc("Channels", message.channel.id, "Command", message.author.name + " (<@" + str(message.author.id)+">)", _new_message, True)
		write_doc("Users", str(message.author.id)+" - " + message.author.name, "Command", message.author.name, message.content, True)
		if prefix != "":
			new_message = new_message.partition(prefix)[2]
		new_message = " ".join(new_message.split())
		if(not new_message.startswith("marvel")) and not new_message.startswith("anime") and not new_message.startswith("naruto"):
			new_message = (new_message+" ").replace(" ", "")
		if new_message == ('ping'):
			await message.channel.send('pong')
		elif new_message == ('test'):
			await message.channel.send('test...')
		elif new_message.startswith("help"):
			await message.channel.send(f"Bot's prefix is: `{prefix}`")
			await message.channel.send(f'Free Speech is Set to {cleverBotEnabled}, CleverBot Functionality is Currently Set to {cleverBotActive} (Depends on Internet Connection)')
			await message.channel.send("----List of Available Commands----")
			await message.channel.send(f"`{prefix}prefix --new prefix--` will change the prefix.")
			await message.channel.send(f"`{prefix}quote` returns a random inspirational quote.")
			await message.channel.send(f"`{prefix}joke` or `{prefix}pun` returns a random pun.")
			await message.channel.send(f"`{prefix}dog` or `{prefix}doggo` returns a random picture of a dog.")
			await message.channel.send(f"`{prefix}cat` or `{prefix}pussy` returns a random picture of a cat.")
			await message.channel.send(f"`{prefix}frog` or `{prefix}forg` returns a random picture of a forg.")
			await message.channel.send(f"`{prefix}ttt start` will start a game of Tic Tac Toe. `{prefix}ttt challenge --username--` will challenge that person to a game. To join any given game type `{prefix}ttt join` and the game will officially start.")
			await message.channel.send(f"`{prefix}trump` returns a random stupid Trump tweet.")
			await message.channel.send(f"`{prefix}anime --anime name--` searches anime by name.\nExamples: `{prefix}anime cowboy bebop` or `{prefix}anime powerpuff girls`\n`{prefix}anime` or `{prefix}anime random` will return info on random anime.")
			await message.channel.send(f"`{prefix}pokemon --pokemon name--` searches pokemon by name or id.\nExamples: `{prefix}pokemon mew` or `{prefix}pokemon 151`\n`{prefix}pokemon` or `{prefix}pokemon random` will return a random pokemon")
			await message.channel.send(f"`{prefix}jjba` or `{prefix}jojo` returns a random stand user and their stand.")
			await message.channel.send(f"`{prefix}naruto --character name--` searches naruto characters by name, clan or village.\nExamples: `{prefix}naruto uchiha` or `{prefix}naruto leaf village`\n`{prefix}naruto` or `{prefix}naruto random` will return a random naruto character.")
			await message.channel.send(f"`{prefix}smash --character name--` searches characters by name in Super Smash Bros. Ultimate.\nExamples: `{prefix}smash mario` or `{prefix}smash ridley`\n`{prefix}smash` or `{prefix}smash random` will return a random smash character.")
			await message.channel.send(f"`{prefix}marvel --character name--` searches Marvel characters by name.\nExamples: `{prefix}marvel spider-man` or `{prefix}marvel captain america`\n`{prefix}marvel` or `{prefix}marvel random` will return a random character")
		elif new_message.startswith('freespeech') or new_message == ("cleverbot"):
			cleverBotEnabled = not (read_doc("Channels", message.channel.id, "FreeSpeech", "", "True") == "True")
			write_doc("Channels", message.channel.id, "FreeSpeech", "", str(cleverBotEnabled), False)
			await message.channel.send(
				f"Bot's Free Speech is Now Set to {cleverBotEnabled}")
		elif new_message == ("stop"):
			print("All Tasks Stopped")
			await message.channel.send("All Tasks Stopped")
		elif new_message.startswith("reset"):
			write_doc("CleverBot", bot.user.id, "Status", "", f"CleverBot will Manually Reset.", True)
			await message.channel.send("CleverBot Will Now Restart")
			try:
				cb.init()
			except:
				await message.channel.send("Failied to Reset CleverBot")
				write_doc("CleverBot", bot.user.id, "Status", "", f"Failied to Reset CleverBot", True)
			else:
				await message.channel.send("CleverBot is Back Online")
				write_doc("CleverBot", bot.user.id, "Status", "", f"CleverBot was Manually Reset.", True)
		elif new_message == ("quote") or new_message == ("inspire"):
			response = requests.get("https://zenquotes.io/api/random")
			json_data = json.loads(response.text)
			quote = json_data[0]['q'] + " -" + json_data[0]['a']
			await message.channel.send(quote)
		elif new_message == "dog" or new_message == "doggo":
			response = requests.get("https://api.thedogapi.com/v1/images/search")
			json_data = json.loads(response.text)
			dog = json_data[0]['url']
			await message.channel.send(dog)
		elif new_message == "cat" or new_message == "pussy":
			response = requests.get("https://api.thecatapi.com/v1/images/search")
			json_data = json.loads(response.text)
			cat = json_data[0]['url']
			await message.channel.send(cat)
		elif new_message == "frog" or new_message == "forg":
			maxFrog = 54
			frog = random.randint(1, maxFrog)
			base_url = "http://www.allaboutfrogs.org/funstuff/random/"
			url = base_url+str(frog).zfill(4)+".jpg"
			await message.channel.send(url)
		elif new_message == "pun" or new_message == "dadjoke" or new_message == "joke":
			base_url = "https://wizardly-wing-66188a.netlify.app/.netlify/functions/server"
			response = requests.get(base_url)
			json_data = json.loads(response.text)
			print(json_data)
			joke = json_data['joke']
			punchline = json_data['punchline']
			await message.channel.send(joke)
			await message.channel.send(punchline)
		elif new_message.startswith("jojo") or new_message.startswith("jjba"):
			base_url = "https://raw.githubusercontent.com/ItzSylex/JojoAPI/master/app/data.json"
			response = requests.get(base_url)
			json_data = json.loads(response.text)
			parts = len(json_data)
			part = random.randint(0, parts - 1)
			part_names = ["StardustCrusaders","DiamondIsUnbreakable","GoldenWind"]
			part_proper_names = ["Stardust Crusaders","Diamond Is Unbreakable","Vento Aureo"]
			part_name = part_names[part]
			characters = len(json_data[part_name])
			character = random.randint(0, characters - 1)
			user = json_data[part_name][character]["user"]
			stand = json_data[part_name][character]["Stand"]
			standimg = json_data[part_name][character]["stand_image"]
			embed = discord.Embed(title="「" + stand + "」",description="User: " + user)
			embed.set_thumbnail(url=standimg)
			embed.set_footer(text="JoJo's Bizzare Adventure: "+part_proper_names[part])
			await message.channel.send(embed=embed)
		elif new_message.startswith("trump"):
			response = requests.get("https://www.tronalddump.io/random/quote")
			json_data = json.loads(response.text)
			quote = json_data['value']
			author = json_data['_embedded']["author"][0]["name"]
			time_posted = json_data["created_at"]
			embed=discord.Embed(title="@realDonaldTrump", description=quote, color=0x1da1f2)
			embed.set_author(name=author, icon_url="https://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_400x400.jpg")
			embed.set_footer(text=time_posted)
			await message.channel.send(embed=embed)
		elif new_message.startswith("prefix"):
			prefix = (new_message+" ").partition("prefix")[2].replace(" ", "")
			write_doc("Channels", message.channel.id, "Prefix", "", prefix, False)
			await message.channel.send(f'New prefix is `{prefix}`')
			print("Prefix set to: " + prefix)
		elif new_message.startswith("pokemon"):
			cycle_embed = Embed("pokearrowleft:811733481759440906", "pokearrowright:811733495071899649")
			await cycle_embed.pokemon(message=message, new_message=new_message, index=0)
		elif new_message.startswith("marvel"):
			argument = new_message.partition("marvel")[2]
			argument = urllib.parse.quote(argument.strip())
			total_characters = 1493
			base_url = "https://gateway.marvel.com:443/v1/public/characters?name="
			index = 0
			if argument == "" or argument == "random" or argument == None:
				randChar = random.randrange(1, total_characters-1)
				base_url = "https://gateway.marvel.com:443/v1/public/characters?limit=1&offset="+str(randChar)
				argument = ""
			public_key = "1145e2dad69a47534793e3f3af16754c"
			private_key = "36d5c4fa5f97081ae59824ac04556d12c60824e0"
			time_stamp = time.time()
			hash = hashlib.md5((str(time_stamp)+private_key+public_key).encode()).hexdigest()
			url = base_url+argument+"&ts="+str(time_stamp)+"&apikey="+public_key+"&hash="+hash
			response = requests.get(url)
			json_data = json.loads(response.text)
			name = json_data['data']['results'][index]['name']
			description = json_data['data']['results'][index]['description']
			picture = json_data['data']['results'][index]['thumbnail']['path']+"."+json_data['data']['results'][index]['thumbnail']['extension']
			copyright = json_data['copyright']
			embed=discord.Embed(title=name, description=description, color=0xea4343)
			embed.set_thumbnail(url=picture)
			embed.set_footer(text=copyright)
			await message.channel.send(embed=embed)
		elif new_message.startswith("anime"):
			argument = new_message.partition("anime")[2]
			argument = urllib.parse.quote(argument.strip())
			total_anime = 15990
			base_url = "https://kitsu.io/api/edge/anime?filter[text]=" + argument
			if argument == "" or argument == "random" or argument == None:
				randAnime = random.randrange(1, total_anime-1)
				base_url = "https://kitsu.io/api/edge/anime?page[limit]=1&page[offset]="+str(randAnime)
				argument = ""
			url = base_url
			response = requests.get(url)
			json_data = json.loads(response.text)
			no_data = "No Data"
			canon_name = json_data["data"][0]["attributes"]["canonicalTitle"]
			try:
				name_en = json_data["data"][0]["attributes"]["titles"]["en_jp"]
				name_jp = json_data["data"][0]["attributes"]["titles"]["ja_jp"]
			except:
				canon_name = json_data["data"][0]["attributes"]["canonicalTitle"]
			else:
				canon_name = name_en + " - "+name_jp
			description = json_data["data"][0]["attributes"]["description"]
			if len(description) > 2000:
				description = description.ljust(2000)[:2000]+"..."
			average_rating_str = json_data["data"][0]["attributes"]["averageRating"]
			average_rating = 1
			if average_rating_str == None:
				average_rating_str = "("+no_data+")"
			else:
				average_rating = round(float(average_rating_str)/10, 2)
				average_rating_str = str(round(float(average_rating_str)/10, 2))
			start_date = json_data["data"][0]["attributes"]["startDate"]
			#end_date = json_data["data"][0]["attributes"]["endDate"]
			#popularity_rank = json_data["data"][0]["attributes"]["popularityRank"]
			#rating_rank = json_data["data"][0]["attributes"]["ratingRank"]
			age_rating = json_data["data"][0]["attributes"]["ageRating"]
			age_rating_guide = json_data["data"][0]["attributes"]["ageRatingGuide"]
			if age_rating_guide == None or age_rating_guide == "":
				age_rating_guide = no_data
			#user_count = json_data["data"][0]["attributes"]["userCount"]
			#status = json_data["data"][0]["attributes"]["status"].upper()
			poster_image = json_data["data"][0]["attributes"]["posterImage"]["original"]
			episode_count = json_data["data"][0]["attributes"]["episodeCount"]
			episode_length = json_data["data"][0]["attributes"]["episodeLength"]
			embed=discord.Embed(title=canon_name, description=description)
			embed.set_image(url=poster_image)
			embed.add_field(name="Rating "+str(average_rating_str), value=("⭐"*int(average_rating)), inline=True)
			embed.add_field(name="Age Rating ("+str(age_rating)+")", value=str(age_rating_guide), inline=True)
			embed.add_field(name=str(episode_count)+" Episodes", value=str(episode_length)+"mins Length", inline=True)
			embed.set_footer(text=str(start_date))
			await message.channel.send(embed=embed)
		elif new_message.startswith("naruto"):
			cycle_embed = Embed("hiddenleafsymbolleft:811379897074712657", "hiddenleafsymbolright:811380306438389800")
			await cycle_embed.naruto(message=message, new_message=new_message, index=0)
		elif new_message.startswith("smash"):
			base_url = "https://api.kuroganehammer.com/api/characters/name/"
			argument = new_message.partition("smash")[2]
			url = base_url + argument
			response = requests.get(url)
			json_data = json.loads(response.text)
			name = json_data['DisplayName']
			stats = json_data['MainImageUrl']
			icon = json_data['ThumbnailUrl']
			color = json_data['ColorTheme']
			ownerid = json_data['OwnerId']
			movement_link = json_data['Links'][3]['Href']
			response = requests.get(movement_link)
			json_data = json.loads(response.text)
			json_size = len(json_data)
			type_name = [None] * json_size
			type_value = [None] * json_size
			for i in range(json_size):
				type_name[i] = json_data[i]['Name']
				type_value[i] = json_data[i]['Value']
			h = color.lstrip('#')
			colorh = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
			embed=discord.Embed(title=name, color=discord.Color.from_rgb(colorh[0], colorh[1], colorh[2]))
			embed.set_thumbnail(url=icon)
			embed.set_image(url=stats)
			for i in range(json_size):
				embed.add_field(name=type_name[i], value=type_value[i], inline=True)
			embed.set_footer(text="Super Smash Bros. Ultimate")
			await message.channel.send(embed=embed)
		elif new_message.startswith("ttt"):
			global ttt
			argument = new_message.partition("ttt")[2]
			if argument.startswith("start"):
				ttt = TicTacToe(message.author.id, None)
				await message.channel.send(f"Waiting For Someone to Join. `{prefix}ttt join` to Join Game!")
			elif argument.startswith("challenge"):
				tttPlCross = message.author.id
				tttPlCircle = re.findall(r'\d+', argument)[0]
				ttt = TicTacToe(tttPlCross, tttPlCircle)
				await message.channel.send(f"<@{tttPlCross}> Has Challenged <@{tttPlCircle}> to a Game of Tic Tac Toe. Type `{prefix}ttt join` to Join.")
			elif argument.startswith("join"):
				await message.channel.send(f"A Game Has Started Between <@{ttt.tttPlCross}> and <@{message.author.id}>!")
				await ttt.join(message.author.id, message)
	if not _new_message.startswith(prefix) or prefix == "":
		if (read_doc("Channels", message.channel.id, "FreeSpeech", "", "True") == "True") and cleverBotActive:
			write_doc("Channels", message.channel.id, "CleverBot", message.author.name + " (<@" + str(message.author.id)+">)", _new_message, True)
			write_doc("Users", str(message.author.id)+" - " + message.author.name, "CleverBot", message.author.name, _new_message, True)
			_new_message = re.sub('<[^>]+>', '', _new_message)
			if _new_message == "":
				return
			try:
				response = cb.getResponse(_new_message)
				print("CLEVERBOT: " + response)
				write_doc("CleverBot", str(bot.user.id), "Conversations", message.author.name + " (<@" + str(message.author.id)+">)", _new_message, True)
				write_doc("CleverBot", bot.user.id, "Conversations", "CLEVERBOT", response, True)
				write_doc("Channels", message.channel.id, "CleverBot", "CLEVERBOT", response, True)
				write_doc("Users", message.author.id, "CleverBot", "CLEVERBOT", response, True)
			except:
				await message.channel.send(f"Looks like bot's CleverBot functionality needs restarting. Run `{prefix}reset` to do that. Bot will be inactive during this time.")
				write_doc("CleverBot", bot.user.id, "Status", "", f"CleverBot Needs Restarting... Run `{prefix}reset`.", True)
				cleverBotActive=False
				await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="Shrek"))
			else:
				if response.lower().find("end") != -1 or response == "" or response == None:
					return
				await message.channel.send(response)
prefix = "!"
cleverBotEnabled = True
cleverBotActive = True
defaultPath = os.path.dirname(os.path.abspath(__file__)) + "/Logs"
#defaultPath = "Logs"
keep_alive()
bot.run("--YOUR TOKEN HERE--")
