# v4.0.0 ✠
# S PROTOCOL COMPONENT




import os
import time
import json
import threading
import curses
import locale




from tqdm import tqdm
from rich.console import Console




locale.setlocale(locale.LC_ALL, '')

Chat_Active: bool = True
Auto_Scroll: bool = True

Message_Scroll_Offset: int = 999999

Current_Messages: list = []
Messages_Lock: threading.Lock = threading.Lock()

Current_Target: str = "#GEREN"
Current_Target_Password: str | None = None

Connection_Error_Count: int = 0
Cursor_Position: int = 0

Last_Error_Message: str = ""
Current_Input: str = ""




def Clear_Terminal():
    os.system('cls' if os.name == 'nt' else 'clear')




def Loading_Animation(Duration):
    Console().print("[bold red]Loading...[/bold red]")
    for _ in tqdm(range(Duration), bar_format="{l_bar}{bar}|", colour='red'):
        time.sleep(0.010)
    Clear_Terminal()




def Fetch_Messages_Action(Connection_Data):

    global Connection_Error_Count, Last_Error_Message

    if not Connection_Data or 'connection' not in Connection_Data:
        Last_Error_Message = "Connection missing"
        return []

    Connection = Connection_Data['connection']

    try:

        Request_Payload = f"21|{Connection_Data['session_token']}|{Current_Target}|{Current_Target_Password or ''}\n"
        
        Raw_Response = Connection.Execute(Request_Payload)

        if not Raw_Response:
            Connection_Error_Count += 1
            Last_Error_Message = "No response"
            return []
        
        Parts = Raw_Response.split("|", 2)

        if len(Parts) >= 3 and Parts[0] == "21" and Parts[1] == "OK":
            Connection_Error_Count = 0
            Last_Error_Message = ""
            return json.loads(Parts[2])
        
        elif len(Parts) >= 3 and Parts[1] == "FAILED":
            Error_Code = Parts[2] if len(Parts) > 2 else "UNKNOWN"
            Last_Error_Message = f"Server error {Error_Code}"
            Connection_Error_Count += 1
            return []

        return []

    except Exception as Exception_Object:
        Connection_Error_Count += 1
        Last_Error_Message = f"Error {str(Exception_Object)[:50]}"
        return []




def Send_Message_Action(Connection_Data, Message):

    global Last_Error_Message

    if not Connection_Data or 'connection' not in Connection_Data:
        Last_Error_Message = "Connection missing"
        return False

    Connection = Connection_Data['connection']

    try:
        
        Request_Payload = f"20|{Connection_Data['session_token']}|{Current_Target}|{Message}|{Current_Target_Password or ''}\n"

        Raw_Response = Connection.Execute(Request_Payload)

        if Raw_Response and "OK" in Raw_Response:
            Last_Error_Message = ""
            return True
        
        elif Raw_Response and "FAILED" in Raw_Response:
            Parts = Raw_Response.split("|")
            Error_Code = Parts[2] if len(Parts) > 2 else "UNKNOWN"
            Last_Error_Message = f"Send failed {Error_Code}"
            return False

        return False

    except Exception as Exception_Object:
        Last_Error_Message = f"Send error {str(Exception_Object)[:50]}"
        return False




def Draw_Screen(Standart_Screen, Connection_Data, Initial_Target=None, Initial_Password=None):

    global Current_Input, Cursor_Position, Chat_Active, Current_Messages, Connection_Error_Count, Last_Error_Message, Auto_Scroll, Current_Target, Current_Target_Password, Message_Scroll_Offset
    
    if Initial_Target:
        Current_Target = Initial_Target
        Current_Target_Password = Initial_Password
    
    curses.curs_set(1)
    Standart_Screen.nodelay(True)
    Standart_Screen.timeout(100)
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    Message_Scroll_Offset = 999999
    
    Data = Fetch_Messages_Action(Connection_Data)
    
    if Data:
        with Messages_Lock:
            Current_Messages = Data
    
    while Chat_Active:

        try:

            Standart_Screen.clear()

            Height, Width = Standart_Screen.getmaxyx()
            
            Banner_Content = [
                "    ╺┓ ┏━┓┏━┓┏━┓    ╻ ┏━╸ ┏┓╻ ┏━┓",
                "     ┃ ┣━┫┣━┫┗━┫    ┃ ┣╸  ┃┗┫ ┣━┫",
                "    ╺┻╸┗━┛┗━┛┗━┛    ╹╹┗━╸╹╹ ╹╹╹ ╹",
                "",
                "         S PROTOCOL CHAT",
                f"         TARGET: {Current_Target}",
                "",
                "Owner License : 1889 I.E.N.A |  Author : Vsevolod Yetzen |  Version : v4.0.0",
                "",
                "| /join #CHANNEL | /dm @USER | /on c:as | /off c:as | /back | Enter - Get Messages |",
            ]

            Row = 1
            
            for Line in Banner_Content:
                if Row < Height - 8:
                    Standart_Screen.addstr(Row, 2, Line[:Width-4], curses.color_pair(4) | curses.A_BOLD)
                Row += 1

            Row += 2
            
            if Connection_Error_Count == 0:
                Status = "● CONNECTED"
                Color = curses.color_pair(2)
            elif Connection_Error_Count < 5:
                Status = f"⚠ UNSTABLE ({Connection_Error_Count} errors)"
                Color = curses.color_pair(3)
            else:
                Status = f"⚠ CONNECTION ISSUES ({Connection_Error_Count} errors)"
                Color = curses.color_pair(1)
            
            if Row < Height - 4:
                Standart_Screen.addstr(Row, 2, Status, Color | curses.A_BOLD)
            Row += 1
            
            Row += 1

            Scroll_Status = "● Auto Scroll ON" if Auto_Scroll else "Auto Scroll OFF"
            Scroll_Color = curses.color_pair(2) if Auto_Scroll else curses.color_pair(3)
            
            if Row < Height - 3:
                Standart_Screen.addstr(Row, 2, Scroll_Status, Scroll_Color | curses.A_BOLD)
            Row += 1

            if Last_Error_Message and Row < Height - 3:
                Standart_Screen.addstr(Row, 2, f"Last error {Last_Error_Message}"[:Width-4], curses.color_pair(1))
            Row += 2
            
            Messages_Area_Height = Height - Row - 2
            
            with Messages_Lock:

                Total_Messages = len(Current_Messages)
                Max_Displayable_Messages = Messages_Area_Height // 4
                
                if Auto_Scroll:
                    Message_Scroll_Offset = max(0, Total_Messages - Max_Displayable_Messages)
                else:
                    Message_Scroll_Offset = max(0, min(
                        Message_Scroll_Offset,
                        max(0, Total_Messages - Max_Displayable_Messages)
                    ))
                
                Display_Messages = Current_Messages[Message_Scroll_Offset:Message_Scroll_Offset + Max_Displayable_Messages] if Current_Messages else []
            
            if not Display_Messages:

                if Row < Height - 2:
                    Standart_Screen.addstr(Row, 2, "No messages loaded", curses.color_pair(3))
                Row += 1
                
            else:

                for Message in Display_Messages:

                    if Row >= Height - 2:
                        break
                    
                    Sender = Message.get("Sender", "Unknown")
                    Content = Message.get("Message", "...")
                    Timestamp = Message.get("Time", "00:00")
                    
                    Header = f"[{Timestamp}] ✠ {Sender}"

                    if Row < Height - 4:
                        Standart_Screen.addstr(Row, 2, Header[:Width-4], curses.color_pair(1) | curses.A_BOLD)
                    Row += 1
                    
                    if Row < Height - 4:
                        Standart_Screen.addstr(Row, 2, Content[:Width-4], curses.color_pair(4) | curses.A_BOLD)
                    Row += 1

                    Row += 1
            
            Input_Row = Height - 4
            Input_Row += 1
            
            if Input_Row < Height:

                Prompt = ">>> "
                Standart_Screen.addstr(Input_Row, 2, Prompt, curses.color_pair(1) | curses.A_BOLD)
                
                Display_Input = Current_Input[:Width - len(Prompt) - 4]
                Standart_Screen.addstr(Input_Row, 2 + len(Prompt), Display_Input, curses.color_pair(4) | curses.A_BOLD)
                
                Cursor_X = min(2 + len(Prompt) + Cursor_Position, Width - 2)
                Standart_Screen.move(Input_Row, Cursor_X)
            
            Standart_Screen.refresh()
            
            try:
                Char_Input = Standart_Screen.get_wch()
            except curses.error:
                continue

            if Char_Input == '\x1b':
                Chat_Active = False
                break
            
            elif Char_Input == '\n' or Char_Input == '\r':
                User_Command = Current_Input.strip()

                if User_Command == "/back":
                    Chat_Active = False
                    return "REDIRECT"
                
                elif User_Command == "/off c:as":
                    Auto_Scroll = False
                    Current_Input = ""
                    Cursor_Position = 0
                    continue

                elif User_Command == "/on c:as":
                    Auto_Scroll = True
                    Current_Input = ""
                    Cursor_Position = 0
                    continue

                elif User_Command.startswith("/join "):

                    Target = User_Command.split(" ")[1]

                    if Target.startswith("#"):
                        Current_Target = Target.upper()
                        
                        Standart_Screen.addstr(Height - 2, 2, f"Enter Password for {Current_Target} ", curses.color_pair(1) | curses.A_BOLD)
                        Standart_Screen.refresh()

                        curses.echo()

                        Current_Target_Password = Standart_Screen.getstr(Height - 2, 2 + 25).decode('utf-8')
                        
                        curses.noecho()
                        
                        Current_Messages = []
                        Message_Scroll_Offset = 999999

                        Data = Fetch_Messages_Action(Connection_Data)

                        if Data:
                            with Messages_Lock:
                                Current_Messages = Data

                    Current_Input = ""
                    Cursor_Position = 0
                    continue

                elif User_Command.startswith("/dm "):

                    Target = User_Command.split(" ")[1]

                    if Target.startswith("@"):
                        Current_Target = Target
                        Current_Target_Password = ""
                        Current_Messages = []
                        Message_Scroll_Offset = 999999
                        
                        Data = Fetch_Messages_Action(Connection_Data)

                        if Data:
                            with Messages_Lock:
                                Current_Messages = Data
                        
                    Current_Input = ""
                    Cursor_Position = 0
                    continue

                if Current_Input.strip():
                    Send_Message_Action(Connection_Data, Current_Input.strip())
                    Current_Input = ""
                    Cursor_Position = 0
                    
                    Data = Fetch_Messages_Action(Connection_Data)

                    if Data:
                        with Messages_Lock:
                            Current_Messages = Data
                else:
                    Data = Fetch_Messages_Action(Connection_Data)
                    if Data:
                        with Messages_Lock:
                            Current_Messages = Data
            
            elif Char_Input == curses.KEY_BACKSPACE or Char_Input == '\x7f' or Char_Input == '\x08':

                if Cursor_Position > 0:
                    Current_Input = Current_Input[:Cursor_Position-1] + Current_Input[Cursor_Position:]
                    Cursor_Position -= 1
            
            elif Char_Input == curses.KEY_LEFT:

                if Cursor_Position > 0:
                    Cursor_Position -= 1
            
            elif Char_Input == curses.KEY_RIGHT:

                if Cursor_Position < len(Current_Input):
                    Cursor_Position += 1
            
            elif Char_Input == curses.KEY_UP:

                if Message_Scroll_Offset > 0:
                    Message_Scroll_Offset -= 1
            
            elif Char_Input == curses.KEY_DOWN:

                with Messages_Lock:
                    Max_Offset = max(0, len(Current_Messages) - Max_Displayable_Messages)
                if Message_Scroll_Offset < Max_Offset:
                    Message_Scroll_Offset += 1
            
            elif isinstance(Char_Input, str) and Char_Input.isprintable():
                Current_Input = Current_Input[:Cursor_Position] + Char_Input + Current_Input[Cursor_Position:]
                Cursor_Position += 1
        
        except KeyboardInterrupt:
            Chat_Active = False
            break
        
        except curses.error:
            pass




def Main(Connection_Data=None, Initial_Target=None, Initial_Password=None):

    Clear_Terminal()

    Loading_Animation(100)

    Clear_Terminal() 

    global Chat_Active, Connection_Error_Count, Last_Error_Message, Current_Messages, Current_Input, Cursor_Position, Current_Target_Password
    
    Chat_Active = True

    Connection_Error_Count = 0
    Cursor_Position = 0

    Current_Messages = []
    Current_Target_Password = Initial_Password
    
    try:
        curses.wrapper(Draw_Screen, Connection_Data, Initial_Target, Initial_Password)

    finally:
        Chat_Active = False
        time.sleep(1.5)




if __name__ == "__main__":
    Main()
