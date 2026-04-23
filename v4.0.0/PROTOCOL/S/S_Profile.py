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

[bold white]MY PROFILE[/bold white]

[bold white]Owner License : 1889 I.E.N.A |  Author : Vsevolod Yetzen |  Version : v4.0.0[/bold white] [bold red]✠[/bold red]"""

    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




def Display_Profile_Table(Profile_Data):
    
    Normal = Profile_Data.get("Normal", {})
    Data_1889 = Profile_Data.get("1889", {})
    Permissions = Profile_Data.get("Look_Permissions", {})

    Info_Table = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    
    Info_Table.add_column("Key", style="bold red", ratio=1)
    Info_Table.add_column("Value", style="bold white", ratio=2)

    Info_Table.add_row("Username", f"{Normal.get('Username', 'N/A')}")

    Info_Table.add_row("Role", f"{Normal.get('Role', 'N/A')}")
    Info_Table.add_row("Account State", f"{Normal.get('Account_State', 'N/A')}")
    Info_Table.add_row("Registration", f"{Normal.get('Account_Created_At', 'N/A')}")

    Info_Table.add_row("Family", f"{Normal.get('Family', 'N/A')}")
    Info_Table.add_row("Work Style", f"{Normal.get('Work_Style', 'N/A')}")
    Info_Table.add_row("Status", f"{Normal.get('Status', 'N/A')}")
    Info_Table.add_row("Locations Within Reach", f"{Normal.get('Locations_Within_Reach', 'N/A')}")
    Info_Table.add_row("Communication", f"{Normal.get('Communication', 'N/A')}")

    Main_Panel = Panel(
        Info_Table,
        title="[bold red]IDENTITY INFORMATION[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Main_Panel)

    Table_1889 = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    
    Table_1889.add_column("Key", style="bold red", ratio=1)
    Table_1889.add_column("Value", style="bold white", ratio=2)

    Table_1889.add_row("1889 Class", f"{Data_1889.get('1889_Class', 'N/A')}")
    Table_1889.add_row("1889 Completed Mission Number", f"{Data_1889.get('1889_Completed_Mission_Number', 'N/A')}")
    Table_1889.add_row("1889 Mission Success_Rates", f"{Data_1889.get('1889_Mission_Success_Rates', 'N/A')}")
    Table_1889.add_row("1889 Score", f"{Data_1889.get('1889_Score', 'N/A')}")
    Table_1889.add_row("1889 Rank", f"{Data_1889.get('1889_Rank', 'N/A')}")
    Table_1889.add_row("1889 Contract Value", f"{Data_1889.get('1889_Contract_Value', 'N/A')}")
    Table_1889.add_row("1889 Anniversary", f"{Data_1889.get('1889_Anniversary', 'N/A')}")
    Table_1889.add_row("1889 Suspension Status", f"{Data_1889.get('1889_Suspension_Status', 'N/A')}")
    Table_1889.add_row("1889 Violation Status", f"{Data_1889.get('1889_Violation_Status', 'N/A')}")
    Table_1889.add_row("1889 Right Number", f"{Data_1889.get('1889_Right_Number', 'N/A')}")

    Panel_1889 = Panel(
        Table_1889,
        title="[bold red]1889 DOCUMENT[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Panel_1889)

    Perm_Table = Table(show_header=True, header_style="bold red", box=None, padding=(0, 2), expand=True)
    
    Perm_Table.add_column("Authority")
    Perm_Table.add_column("Status", justify="right")

    Perm_List = [
        ("Ban Authority", Permissions.get("Ban_Authority", False)),
        ("Clear Chat Authority", Permissions.get("Chat_Clear_Authority", False)),
        ("Chat Access", Permissions.get("Chat_Permission", False)),
        ("Task View", Permissions.get("View_Tasks", False)),
    ]

    for Name, Status in Perm_List:
        Status_Text = "[bold green]GRANTED[/bold green]" if Status else "[bold red]DENIED[/bold red]"
        Perm_Table.add_row(Name, Status_Text)

    Perm_Panel = Panel(
        Perm_Table,
        title="[bold red]SECURITY CLEARANCE[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Perm_Panel)

    Bio_Text = Data_1889.get('1889_Bio', 'No biography available.')
    
    Bio_Panel = Panel(
        f"[italic white]{Bio_Text}[/italic white]",
        title="[bold red]BIOGRAPHY[/bold red]",
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Bio_Panel)




def Fetch_Profile_Data(Connection_Data):
    
    if not Connection_Data or 'connection' not in Connection_Data:
        return None

    Connection = Connection_Data['connection']

    try:

        Request_Message = f"13|{Connection_Data['session_token']}\n"

        Response = Connection.Execute(Request_Message)

        if Response and "|" in Response:
            Parts = Response.split("|", 2)
            
            if len(Parts) >= 3 and Parts[0] == "13" and Parts[1] == "OK":
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

    Profile_Data = Fetch_Profile_Data(Connection_Data)

    if Profile_Data is None:
        time.sleep(1.5)
        Console().print("\n[bold red]Failed to retrieve profile data[/bold red]")
        Console().input("")
        return

    Display_Profile_Table(Profile_Data)
    
    Get_User_Input()
    
    time.sleep(1.5)




if __name__ == "__main__":
    Main()
