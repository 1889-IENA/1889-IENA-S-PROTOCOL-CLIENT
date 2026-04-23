# v4.0.0 ✠
# S PROTOCOL COMPONENT




import os
import json
import time




from tqdm import tqdm
from rich.console import Console
from rich.table import Table
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

[bold white]MISSIONS[/bold white]

[bold white]Owner License : 1889 I.E.N.A |  Author : Vsevolod Yetzen |  Version : v4.0.0[/bold white] [bold red]✠[/bold red]"""

    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




def Fetch_Missions_Data(Connection_Data):

    if not Connection_Data or 'connection' not in Connection_Data:
        return None

    Connection = Connection_Data['connection']

    try:

        Request = f"30|{Connection_Data['session_token']}\n"
        
        Response = Connection.Execute(Request)
        
        if Response and "|" in Response:
            Parts = Response.split("|", 2)
            
            if len(Parts) >= 3 and Parts[0] == "30" and Parts[1] == "OK":
                return json.loads(Parts[2])

        return None

    except Exception as Exception_Object:
        Console().print(f"\n[bold red]Unexpected error[/bold red] - [bold white]{Exception_Object}[/bold white]")
        time.sleep(1.5)
        return None




def Get_User_Input():
    
    Input_Panel = Panel(
        "[bold red]══[/bold red] [bold white]Press Enter to Return[/bold white]",
        border_style="red",
        padding=(0, 2),
        expand=True
    )

    Console().print(Input_Panel)
    
    Console().input("")




def Main(Connection_Data=None):

    Clear_Terminal()

    Loading_Animation(100)

    Clear_Terminal() 

    Display_Banner()

    Missions_Raw = Fetch_Missions_Data(Connection_Data)

    if Missions_Raw and "Missions" in Missions_Raw:
        
        Missions_List = Missions_Raw["Missions"]

        if not Missions_List:
            Console().print("\n[bold white]No missions available[/bold white]\n")
        
        for Mission_Item in Missions_List:
            
            M_Class = Mission_Item.get("Mission_Class", "N/A")
            M_Color = Mission_Item.get("Mission_Color", "white")
            M_Data = Mission_Item.get("Mission", {})

            M_Table = Table(show_header=False, box=None, padding=(0, 1))
            M_Table.add_row(f"[bold {M_Color}]NAME[/bold {M_Color}]", f"[bold white]{M_Data.get('Mission_Name', 'N/A')}[/bold white]")
            M_Table.add_row(f"[bold {M_Color}]CODE[/bold {M_Color}]", F"[bold white]{M_Data.get('Mission_Code', 'Unverified mission')}[/bold white]")
            M_Table.add_row(f"[bold {M_Color}]EARN[/bold {M_Color}]", f"[bold green]{M_Data.get('Score_Earn', '0')} Score [bold {M_Color}]/[/bold {M_Color}] {M_Data.get('Money_Earn', '0')}[/bold green]")
            M_Table.add_row(f"[bold {M_Color}]INFO[/bold {M_Color}]", f"[white]{M_Data.get('Mission_Info', 'No information provided')}[/white]")

            Mission_Panel = Panel(
                M_Table,
                title=f"[bold {M_Color}]{M_Class}[/bold {M_Color}]",
                border_style=M_Color,
                padding=(1, 2),
                expand=True
            )

            Console().print(Mission_Panel)

    else:
        Console().print("\n[bold red]Failed to fetch missions[/bold red]\n")

    Get_User_Input()
    
    time.sleep(1.5)




if __name__ == "__main__":
    Main()
