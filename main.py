from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

class Server_UserWords(dict):
    def __init__(self, servername) -> None:
        self.servername = servername
        self = dict()

    def add(self, username, value):
        if username in self:
            self[username] += value
        else:
            self[username] = value

    def printformat(self) -> str:
        l = list(self)
        s = self.servername +" "+ str(len(l))
        for i in range(len(l)):
            s = s +"\n"+ l[i] +" "+ str(self[l[i]])
        return s + "\n"
    
class ServerLevelManager:
    # read the article for more on reading and writing to files in python
    # https://realpython.com/read-write-files-python/
    num_servers = 0
    servers: Server_UserWords = []
    filename: str = ""
    save_counter = 0
    def __init__(self, filename: str) -> None:
        self.load_from_file(filename)
    
    def load_from_file(self, filename: str) -> None:
        self.filename = filename
        with open(filename, 'r') as file:
            self.num_servers = file.readline(1) #gets the 1st character from line 1
            for i in range(self.num_servers):
                ser = file.readline().split(" ")
                servername, users = ser[0], int(ser[1])
                ns = Server_UserWords(servername)
                self.servers.append(ns) 
                for j in range(users):
                    u = file.readline().split(" ")
                    user, level = u[0], int(u[1])
                    # TODO upon reading, check if user exists before they are added (some may have deleted their accounts from discord)
                    ns.add(user, level)

    def save_to_file(self) -> None:
        for server in self.servers:
            sorted(server)
        with open(self.filename, 'w') as file:
            for i in range(len(self.servers)):
                file.write(server.printformat())
        
    def process(self, servername: str, username: str, message: str) -> None:
        # remove all spaces from server name to make it easier to split
        servername.replace(" ", "")
        for i in range(len(self.servers)): # TODO optimize. currently runs a linear search on servers
            if self.servers[i].servername == servername:
                self.servers[i].add(username, message)
                return
        self.servers.append(Server_UserWords(servername).add(username, message))

        self.save_counter +=1
        if self.save_counter > 10: 
            #every 10 messages, the program will save the statistics to file
            self.save_to_file()

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
wordcounter: ServerLevelManager = ServerLevelManager('servers_stats.txt')

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled properly)')
        return
    if is_private := user_message[0] == '?': # returns a private message when ? is used
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

async def process_leveling(server: str, user: str, message: str):
    # TODO implement member
    pass

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    server: str = str(message.guild)
    length: int = len(user_message)
    #print(f'[{server} in # {channel}] (from {username}) "{user_message}"') #logs the incomming message in the terminal

    print(f'{username} +{length} in {server}') #logs the message statistics in the terminal

    await send_message(message, user_message)

#Step 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()