# v4.0.0 ✠
# S PROTOCOL COMPONENT




import os
import time
import sys




from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




from PROTOCOL.S import S_Chat
from PROTOCOL.S import S_Missions

from PROTOCOL.S import S_Profile
from PROTOCOL.S import S_Admin




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

[bold white]S PROTOCOL[/bold white]

[bold white]Owner License : 1889 I.E.N.A |  Author : Vsevolod Yetzen |  Version : v4.0.0[/bold white] [bold red]✠[/bold red]"""

    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




def Display_Menu():

    Communication_Panel = Panel(
        "[bold cyan][ 1 ][/bold cyan] [bold white]Chat Center[/bold white]\n\n"
        "[bold cyan]v4.0.0[/bold cyan]",
        title="[bold cyan]COMMUNICATION[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
        expand=True
    )

    Console().print(Communication_Panel)

    File_Panel = Panel(
        "[bold red][ 2 ][/bold red] [bold white]MISSIONS[/bold white]\n\n"
        "[bold red]v4.0.0[/bold red]",
        title="[bold red]MISSIONS[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(File_Panel)

    Admin_Panel = Panel(
        "[bold red][ 3 ][/bold red] [bold white]MY PROFILE[/bold white]\n"
        "[bold red][ 4 ][/bold red] [bold white]MY ADMIN[/bold white]\n\n"
        "[bold red]v4.0.0[/bold red]",
        title="[bold red]ADMIN[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Admin_Panel)

    System_Panel = Panel(
        "[bold red][ B ][/bold red]  [bold white]Back[/bold white]        [bold red](Disconnect)[/bold red]\n"
        "[bold red][ E ][/bold red]  [bold white]Exit Client[/bold white] [bold red](Disconnect)[/bold red]",
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




def Secure_Logout(Connection_Data):
    
    if not Connection_Data or 'connection' not in Connection_Data:
        return

    Connection = Connection_Data['connection']

    try:

        Logout_Message = f"11|{Connection_Data['session_token']}\n"
        
        Response = Connection.Execute(Logout_Message)
            
        if Response == "11|OK":
            Console().print("\n[bold red]Disconnected successfully[/bold red]")
        
        else:
            Console().print("\n[bold red]Disconnected but the server was not notified or connection failed[/bold red]")

    except Exception as Exception_Object:
        Console().print(f"\n[bold red]Unexpected error during logout[/bold red] - [bold white]{Exception_Object}[/bold white]")
        time.sleep(1.5)




def Select_Communication_Target(Connection_Data):

    while True:

        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal()

        Display_Banner()
    
        Target_Panel = Panel(
            "[bold cyan][ 1 ][/bold cyan] [bold white]#GEREN[/bold white]\n"
            "[bold cyan][ 2 ][/bold cyan] [bold white]#ERSIV[/bold white]\n"
            "[bold cyan][ 3 ][/bold cyan] [bold white]#YETZEN[/bold white]\n",
            title="[bold cyan]SELECT CHANNEL[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
            expand=True
        )

        Console().print(Target_Panel)

        Dm_Panel = Panel(
            "[bold cyan][ 4 ][/bold cyan] [bold white]@username[/bold white]\n",
            title="[bold cyan]DIRECT MESSAGE[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
            expand=True
        )
    
        Console().print(Dm_Panel)

        C_System_Panel = Panel(
            "[bold red][ B ][/bold red] [bold white]Back[/bold white]\n"
            "[bold red][ E ][/bold red] [bold white]Exit Client[/bold white] [bold red](Disconnect)[/bold red]",
            title="[bold red]SYSTEM COMMANDS[/bold red]",
            border_style="red",
            padding=(1, 2),
            expand=True
        )

        Console().print(C_System_Panel)

        Choice = Get_User_Input()

        if Choice == 'b':
            return None, None

        if Choice == 'e':
            time.sleep(1.5)
            Secure_Logout(Connection_Data)
            Clear_Terminal()
            Console().print("[bold red]Exited[/bold red]")
            sys.exit(0)
    
        if Choice in ['1', '2', '3']:
            Channels = {'1': '#GEREN', '2': '#ERSIV', '3': '#YETZEN'}

            Selected_Channel = Channels[Choice]
        
            Clear_Terminal()
            Display_Banner()
        
            Password = Console().input(f"\n[bold red]Enter Password for {Selected_Channel} [/bold red]").strip()
        
            return Selected_Channel, Password

        if Choice == '4':
            Username = Console().input("\n[bold red]Enter Username [/bold red]").strip()

            if not Username.startswith("@"):
                continue
            
            return Username, None




def Main(Connection_Data=None):
    
    while True:

        Clear_Terminal()

        Loading_Animation(100)

        Clear_Terminal() 

        Display_Banner()

        Display_Menu()

        Choice = Get_User_Input()

        if Choice == '1':
            time.sleep(1.5)
            Target, Password = Select_Communication_Target(Connection_Data)
            if Target:
                S_Chat.Main(Connection_Data, Target, Password)
            continue
        
        if Choice == '2':
            time.sleep(1.5)
            S_Missions.Main(Connection_Data)
            continue
        
        if Choice == '3':
            time.sleep(1.5)
            S_Profile.Main(Connection_Data)  
            continue

        if Choice == '4':
            time.sleep(1.5)
            S_Admin.Main(Connection_Data)
            continue

        if Choice == 'b':
            time.sleep(1.5)
            Secure_Logout(Connection_Data)
            return
        
        if Choice == 'e':
            time.sleep(1.5)
            Secure_Logout(Connection_Data)
            Clear_Terminal()
            Console().print("[bold red]Exited[/bold red]")
            sys.exit(0)




if __name__ == "__main__":
    Main()
