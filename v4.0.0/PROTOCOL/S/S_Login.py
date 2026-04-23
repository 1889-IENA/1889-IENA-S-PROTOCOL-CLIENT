# v4.0.0 ✠
# S PROTOCOL COMPONENT




import os
import time
import sys
import json





from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




from PROTOCOL.S import S_Redirect
from PROTOCOL.CONNECTOR import S_Connection




def Clear_Terminal():
    os.system('cls' if os.name == 'nt' else 'clear')




def Loading_Animation(Duration):
    Console().print("[bold red]Loading...[/bold red]")
    for _ in tqdm(range(Duration), bar_format="{l_bar}{bar}|", colour='red'):
        time.sleep(0.010)
    Clear_Terminal()




def Display_Banner():
    
    Banner_Content = """
    [bold white]
╺┓ ┏━┓┏━┓┏━┓   ╻ ┏━╸ ┏┓╻ ┏━┓
 ┃ ┣━┫┣━┫┗━┫   ┃ ┣╸  ┃┗┫ ┣━┫
╺┻╸┗━┛┗━┛┗━┛   ╹╹┗━╸╹╹ ╹╹╹ ╹[/bold white]

[bold white]S PROTOCOL LOGIN[/bold white]

[bold white]Owner License : 1889 I.E.N.A |  Author : Vsevolod Yetzen |  Version : v4.0.0[/bold white] [bold red]✠[/bold red]"""

    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




def Display_Menu():

    Login_Panel = Panel(
        "[bold red][ ENTER ][/bold red] [bold white]Login to S Protocol[/bold white]\n\n"
        "[bold red]Enable [bold white]VPN[/bold white] or [bold white]TOR[/bold white] for anonymity before usage[/bold red]",
        title="[bold red]S PROTOCOL - LOGIN[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Login_Panel)

    System_Panel = Panel(
        "[bold red][ E ][/bold red]  [bold white]Exit Client[/bold white]",
        title="[bold red]SYSTEM COMMANDS[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(System_Panel)




def Get_User_Input():
    
    Input_Panel = Panel(
        "[bold red]══[/bold red] [bold white]Enter Command[/bold white]",
        border_style="red",
        padding=(0, 2),
        expand=True
    )

    Console().print(Input_Panel)
    
    Choice = Console().input("").strip().lower()
    
    return Choice




def Load_Client_Config():

    Config_Path = "v4.0.0/IENA_Client_Config.json"
    
    if not os.path.exists(Config_Path):
        Console().print("\n[bold red]IENA_Client_Config.json not found[/bold red]")
        return None

    try:
        with open(Config_Path, 'r', encoding='utf-8') as File:
            return json.load(File)
    
    except Exception:
        return None




def Try_Connect():

    try:

        Username = Console().input("\n[bold red]Username[/bold red] ").strip()

        if not Username:
            Console().print("\n[bold red]Username cannot be empty[/bold red]")
            time.sleep(1.5)
            return None

        Password = Console().input("\n[bold red]Password[/bold red] ").strip()

        if not Password:
            Console().print("\n[bold red]Password cannot be empty[/bold red]")
            time.sleep(1.5)
            return None

        Host = Console().input("\n[bold red]Server Address[/bold red] ").strip()

        if not Host:
            Console().print("\n[bold red]Server address cannot be empty[/bold red]")
            time.sleep(1.5)
            return None

        Port_Input = Console().input("\n[bold red]Server Port[/bold red] ").strip()

        if not Port_Input or not Port_Input.isdigit():
            Console().print("\n[bold red]Enter a valid port number[/bold red]")
            time.sleep(1.5)
            return None
        
        Port = int(Port_Input)

    except (EOFError, KeyboardInterrupt):
        Console().print("\n[bold red]Login cancelled[/bold red]")
        time.sleep(1.5)
        return None

    Config = Load_Client_Config()

    if not Config:
        return None

    Connection = S_Connection.S_Connection(Host, Port, Config)

    try:
    
        Console().print(f"\n[bold red]Connecting via Mutual TLS to {Host}/{Port}[/bold red]")

        Auth_Request = f"10|{Username}|{Password}\n"

        Response = Connection.Execute(Auth_Request)

        if not Response or not Response.startswith("10|OK|"):

            if Response and "LOCKED" in Response:
                Console().print("\n[bold red]Account locked[/bold red]")

            elif Response and "FAILED" in Response:
                Console().print("\n[bold red]Authentication failed[/bold red]")
            
            elif Response and "RATE_LIMIT" in Response:
                Console().print("\n[bold red]Rate limit exceeded[/bold red]")
            
            else:
                Console().print("\n[bold red]Login rejected or connection error[/bold red]")
            
            time.sleep(1.5)
            return None

        Parts = Response.split("|")

        if len(Parts) < 3:
            Console().print("\n[bold red]Invalid login response format[/bold red]")
            time.sleep(1.5)
            return None

        Session_Token = Parts[2]

        Console().print(f"\n[bold red]Login Successful[/bold red] - [bold green]{Username}[/bold green]")

        Connection_Data = {
            "username": Username,
            "session_token": Session_Token,
            "host": Host,
            "port": Port,
            "connected": True,
            "connection": Connection
        }

        return Connection_Data

    except Exception as Exception_Object:
        Console().print(f"\n[bold red]Unexpected error[/bold red] - [bold white]{Exception_Object}[/bold white]")
        time.sleep(1.5)
        return None





def Main():
    
    while True:

        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal() 

        Display_Banner()

        Display_Menu()

        Choice = Get_User_Input()
        
        if Choice == 'e':
            Clear_Terminal()
            Console().print("[bold red]Exited[/bold red]")
            sys.exit(0)
        
        if Choice != '':
            Console().print("[bold red]Invalid selection[/bold red]")
            continue

        Clear_Terminal()

        Display_Banner()

        Connection_Data = Try_Connect()

        if Connection_Data:
            time.sleep(1.5)
            S_Redirect.Main(Connection_Data)
        else:
            Console().input("\n[bold red]Press Enter to return to main menu[/bold red]")




if __name__ == "__main__":
    Main()
