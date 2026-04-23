# v4.0.0 ✠
# S PROTOCOL COMPONENT




import os
import time




from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




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

[bold white]MY ADMIN[/bold white]

[bold white]Owner License : 1889 I.E.N.A |  Author : Vsevolod Yetzen |  Version : v4.0.0[/bold white] [bold red]✠[/bold red]"""

    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




def Send_Admin_Request(Connection_Data, Op_Code, Data=""):

    if not Connection_Data or 'connection' not in Connection_Data:
        return None

    Connection = Connection_Data['connection']

    try:

        if Data:
            Request = f"{Op_Code}|{Connection_Data['session_token']}|{Data}\n"
        else:
            Request = f"{Op_Code}|{Connection_Data['session_token']}\n"
         
        Response = Connection.Execute(Request)
        
        return Response
    
    except Exception as Exception_Object:
        Console().print(f"\n[bold red]Unexpected error[/bold red] - [bold white]{Exception_Object}[/bold white]")
        time.sleep(1.5)
        return None




def Handle_Ban_Command(Connection_Data, Username):

    Response = Send_Admin_Request(Connection_Data, 40, Username)

    if not Response:
        Console().print("\n[bold red]Connection error[/bold red]")
        return

    Parts = Response.split("|")
    
    if len(Parts) >= 2 and Parts[0] == "40" and Parts[1] == "OK":
        Console().print(f"\n[bold green]{Username} Banned[/bold green]")
    
    elif len(Parts) >= 3 and Parts[1] == "FAILED":
        Console().print(f"\n[bold red]Ban failed[/bold red] - [bold white]{Parts[2]}[/bold white]")




def Handle_UnBan_Command(Connection_Data, Username):

    Response = Send_Admin_Request(Connection_Data, 41, Username)

    if not Response:
        Console().print("\n[bold red]Connection error[/bold red]")
        return

    Parts = Response.split("|")
    
    if len(Parts) >= 2 and Parts[0] == "41" and Parts[1] == "OK":
        Console().print(f"\n[bold green]{Username} Unbanned[/bold green]")
    
    elif len(Parts) >= 3 and Parts[1] == "FAILED":
        Console().print(f"\n[bold red]UnBan failed[/bold red] - [bold white]{Parts[2]}[/bold white]")




def Handle_Clear_Chat_Command(Connection_Data, Target, Password=""):

    if not Connection_Data or 'connection' not in Connection_Data:
        Console().print("\n[bold red]Connection error[/bold red]")
        return

    Connection = Connection_Data['connection']

    try:

        Request = f"42|{Connection_Data['session_token']}|{Target}|{Password}\n"
        
        Response = Connection.Execute(Request)

        if not Response:
            Console().print("\n[bold red]Connection error[/bold red]")
            return

        Parts = Response.split("|")
        
        if len(Parts) >= 2 and Parts[0] == "42" and Parts[1] == "OK":
            Console().print(f"\n[bold green]{Target} cleared successfully[/bold green]")
        
        elif len(Parts) >= 3 and Parts[1] == "FAILED":
            Console().print(f"\n[bold red]Clear failed[/bold red] - [bold white]{Parts[2]}[/bold white]")

    except Exception as Exception_Object:
        Console().print(f"\n[bold red]Unexpected error[/bold red] - [bold white]{Exception_Object}[/bold white]")
        time.sleep(1.5)




def Get_User_Input():

    Input_Panel = Panel(
        "[bold red]══[/bold red] [bold white]Enter Command[/bold white]",
        border_style="red",
        padding=(0, 2),
        expand=True
    )

    Console().print(Input_Panel)
    
    Command = Console().input("").strip()
    
    return Command




def Main(Connection_Data=None):

    while True:

        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal() 

        Display_Banner()

        Help_Panel = Panel(
            "[bold white]/ban k:username[/bold white]\n"
            "[bold white]/unban k:username[/bold white]\n"
            "[bold white]/clear chat:TARGET password:PASSWORD[/bold white]\n"
            "[bold white]/back[/bold white]",
            title="[bold red]ADMIN COMMANDS[/bold red]",
            border_style="red",
            padding=(1, 2),
            expand=True
        )

        Console().print(Help_Panel)

        Command = Get_User_Input()

        if Command == "/back":
            return Connection_Data

        if Command.startswith("/ban k:"):
            
            Target_Username = Command[7:].strip()
            
            if not Target_Username:
                Console().print("\n[bold red]Username cannot be empty[/bold red]")
                time.sleep(1.5)
                continue

            Handle_Ban_Command(Connection_Data, Target_Username)
            
            time.sleep(1.5)
            continue

        if Command.startswith("/unban k:"):
            
            Target_Username = Command[9:].strip()
            
            if not Target_Username:
                Console().print("\n[bold red]Username cannot be empty[/bold red]")
                time.sleep(1.5)
                continue

            Handle_UnBan_Command(Connection_Data, Target_Username)

            time.sleep(1.5)
            continue

        if Command.startswith("/clear chat:"):
            
            Parts = Command[12:].strip().split(" password:")
            
            Target = Parts[0].strip()
            Password = Parts[1].strip() if len(Parts) > 1 else ""
            
            if not Target:
                Console().print("\n[bold red]Target cannot be empty[/bold red]")
                time.sleep(1.5)
                continue

            if not Target.startswith("#") and not Target.startswith("@"):
                Target = "#" + Target.upper()

            Handle_Clear_Chat_Command(Connection_Data, Target, Password)

            time.sleep(1.5)
            continue

        Console().print("\n[bold red]Invalid selection[/bold red]")
        time.sleep(1.5)




if __name__ == "__main__":
    Main()
