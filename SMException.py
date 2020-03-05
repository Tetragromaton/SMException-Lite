from listeners import OnServerOutput
from core import OutputReturn
from commands.typed import TypedClientCommand
from players._base import *
from messages import SayText2
from messages import *
from commands.client import ClientCommand
from commands.typed import TypedServerCommand
from commands.typed import filter_str
from commands.say import SayCommand
from weapons.entity import Weapon
from weapons import *
from config.manager import ConfigManager
ExceptionStreak = 0
ListingException = 0
SystemAdminSTEAMID = ""#YOUR STEAMID HERE !!!
ExceptionData = ""

if SystemAdminSTEAMID == "":
    print("No steamid provided ! You will be unable use in game client commands.")

'''
                                        [SM] Exception Lite v1.0
                                Github repo: github.com/Tetragromaton/SMException-Lite
                 Get rid of the mass flood in your console, enjoy management of your console !
        This plugin hides all [SM] Exception messages in the server console and makes it's navigation a little easier.
        
        -Commands:
            Server commands:
                exceptions - Displays a counter of how much exceptions was captured since this plugin loaded.
                lastexception - Displays the last captured exceptions in server console.
            Client commands(prints in console):
                exceptions - Displays the same amount of captured exceptions.
                lastexception - Unstable because output of the command prints the log in game console of the player,
                that causes buffer overflow on his side.
                
        !!Please define the system admin STEAMID above in variable SystemAdminSTEAMID, because only this steamID can
        use in game commands !!
            
        
'''


def AreException():
    global ListingException
    return ListingException
def BuildExceptionString(Value=""):
    global ExceptionData
    ExceptionData = ExceptionData + "\n" + Value

def StartListeningException(Value=0):
    global ListingException
    ListingException = Value

def IncrementExceptionStreak():
    global ExceptionStreak
    ExceptionStreak = ExceptionStreak + 1

@TypedServerCommand('exceptions')
def ShowExceptionStreak(command_info):
    print("Exceptions since plugin loaded: " + str(ExceptionStreak) + ". To print last exception data, print ->lastexception<-")

@TypedServerCommand('lastexception')
def ShowExceptionStreak(command_info):
    print("======================THE LAST EXCEPTION CAPTURED======================")
    print(str(ExceptionData))
    print("======================END OF THE CAPTURED EXCEPTION======================")

@ClientCommand('exceptions')
def ShowExceptionStreak(command_info, pindex):
    client = Player(pindex)
    if client.steamid == SystemAdminSTEAMID:
        SayText2('\x04 Counting \x02' + str(ExceptionStreak) + '\x04 exceptions').send(client.index)
    else:
        SayText2('\x02[SMException] You have no access(Not a system admin)').send(client.index)

@ClientCommand('lastexception')
def ShowExceptionStreak(command_info, pindex):
    client = Player(pindex)
    if client.steamid == SystemAdminSTEAMID:
        client.client_command("echo " + str(ExceptionData))
        SayText2('\x03 [SMException] Exception printed in your console(maybe)').send(client.index)
    else:
        SayText2('\x02 [SMException] You have no access(Not a system admin)').send(client.index)

@OnServerOutput
def on_server_output(severity, msg):
    if "Exception reported" in msg:
        StartListeningException(1)
        #SayText2('\x02 [Exception thrown]').send()
        IncrementExceptionStreak()
        BuildExceptionString(msg)
        return OutputReturn.BLOCK
    if AreException() > 0:
        if ": [SM]" in msg:
            gg = 0
            gg + 1
            BuildExceptionString(msg)
            return OutputReturn.BLOCK
        else:
            StartListeningException(0)
    return OutputReturn.CONTINUE