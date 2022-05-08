from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import random,discord,os,wikipedia,qrcode,requests


load_dotenv()
TOKEN = os.getenv('TOKEN')  #Load discord token from env file

bot = commands.Bot(command_prefix='!') 
client = discord.Client()

@bot.command(name='image', help='Send random image to chat')    #Command name and help for it 
async def images(ctx):
    script_dir = os.path.abspath(os.path.dirname(__file__))     #Get script directory
    filenames = os.listdir(script_dir + "\images")              #Get all files from images directory
    extensions = ['.png','.jpg','.gif']                         #Allowed file extensions
    images = []

    for i in filenames:                                         #Check if files have supported extensions
        if i.endswith(tuple(extensions)) and i not in images:   
            images.append(i)
  
    random_img = script_dir + "\\images\\" + random.choice(images)     #Choose random image and add path to it     
    await ctx.send(file=discord.File(random_img))                      #Send random image

@bot.command(name='text', help='Send random text')              #Command name and help for it 
async def text(ctx):
    script_dir = os.path.abspath(os.path.dirname(__file__))     #Get script directory
    text_file_path = script_dir + "\\text\\" + "text.txt"       #Get file path
    file = open(text_file_path, 'r')                            

    for line in file.readlines():                               #Split words by comma
        text = line.rstrip().split(',')
   
    file.close()             
    random_text = random.choice(text)                           #Choose random text
    await ctx.send(random_text)                                 #Send random text


@bot.command(name='whatis', help='Send wikipedia article about topic you wrote')    #Command name and help for it 
async def whatis(ctx,*args):
    try :
        data = " " .join(args)                                                      #Try if article exist                                                                        
        article = wikipedia.summary(data, sentences = 2)                            #Words separeted by space 
        await ctx.send(article)                                                     #Send wikipedia article                                                
   
    except:                                                                         #If article doesn't exist or if exist more articles than 1
        data = " " .join(args)                                                      #Words separeted by space                                                                  
        article = wikipedia.search(data, sentences = 2)                             #Search for articles
        
        if len(article) > 0 :                                                       #If something found
            result = str(article)[1:-1]                                             #Convert to string
            result = result.replace("'", "")                                        #Add , between results
            await ctx.send(f"{data} can be : {result}")                             #Send results
        else :                                                                      #If didn't found
            await ctx.send("The article isn't existing or you wrote it wrong") 

@bot.command(name='qrcode', help='Make your own qrcode')           #Command name and help for it 
async def qr(ctx,*args):
    script_dir = os.path.abspath(os.path.dirname(__file__))        #Get script directory
    data = " " .join(args)                                         #Words separeted by space
    img = qrcode.make(data)                                        #Make qr code
    
    filepath = script_dir + "\\qr.png"
    img.save(filepath)                                             #Save qr code 
    
    
    await ctx.send(file=discord.File(filepath))                    #Send qr code
    os.remove(script_dir + "\\qr.png")                             #Delete the qr code to save space on device

@bot.command(name='news', help="Send top 3 news")                  #Command name and help for it 
async def qr(ctx):
    url = 'https://www.bbc.com/news'                               #URL for news
    response = requests.get(url)                                   

    soup = BeautifulSoup(response.text, 'html.parser')

    links = []

    for a in soup.select("[class~=gs-c-promo-heading]",href=True):
        links.append("https://www.bbc.com"+ a['href'])              #Add links to news article

    await ctx.send(f"{links[1]}\n{links[2]}\n{links[13]}\n")        #Send 3 news 

@bot.command(name='rpas', help="Rock Paper and Scissors game")      #Command name and help for it 
async def game(ctx,arg):
   
    choices = ["rock", "paper", "scissors"]

    bot_choice = random.choice(choices)                             

    player_choice = arg                                               

    if player_choice in choices :                                   #If player writes correctly choice
        if bot_choice == player_choice :
            await ctx.send(f"Tie, you both selected {bot_choice}")

        elif bot_choice == "rock" and player_choice == "paper":
            await ctx.send(f"You win, bot selected {bot_choice}\nCongratulations :tada:")

        elif bot_choice == "rock" and player_choice == "scissors":
            await ctx.send(f"Bot win, bot selected {bot_choice}")

        elif bot_choice == "paper" and player_choice == "rock":
            await ctx.send(f"Bot win, bot selected {bot_choice}")

        elif bot_choice == "paper" and player_choice == "scissors":
            await ctx.send(f"You win, bot selected {bot_choice}\nCongratulations :tada:")

        elif bot_choice == "scissors" and player_choice == "rock":
            await ctx.send(f"You win, bot selected {bot_choice}\nCongratulations :tada:")

        elif bot_choice == "scissors" and player_choice == "paper":
            await ctx.send(f"Bot win, bot selected {bot_choice}")
    
    elif player_choice not in choices:                                 #If player writes something else 
        await ctx.send(f"Write please !rpas (rock,paper,scissors)")

@bot.listen('on_message')
async def chat(msg):

    script_dir = os.path.abspath(os.path.dirname(__file__))     #Get script directory
    text_file_path = script_dir + "\\ban words\\" + "words.txt" #Get file path
    file = open(text_file_path, 'r') 
    message = msg.author.mention + " was warned"                #Warn message

    for line in file.readlines():                               #Split words by comma
        words = line.rstrip().split(',')
   
    file.close()             

    for i in words : 
       if i in msg.content:                                     #If ban words is send
            await msg.delete()                                  #Delete the message if contains baned words 
            await msg.channel.send(message)                     #Send warn message
            
bot.run(TOKEN)