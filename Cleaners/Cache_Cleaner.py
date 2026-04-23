# v4.0.0 ✠
# MAIN COMPONENT




import os
import shutil
from rich.console import Console
from rich.panel import Panel
from rich.align import Align




def Clear_Terminal():
    os.system('cls' if os.name == 'nt' else 'clear')




def Clear_Pycache():

    for Dirpath, Dirnames, Filenames in os.walk('.'):

        if '__pycache__' in Dirnames:

            Pycache_Path = os.path.join(Dirpath, '__pycache__')

            try:
                shutil.rmtree(Pycache_Path)
            except Exception:
                pass




def Display_Banner():
    
    Banner_Content = """[bold white]Cache Cleaned[/bold white]"""
    Banner_Panel = Panel(
        Align.center(Banner_Content),
        border_style="red",
        padding=(1, 2),
        expand=True
    )

    Console().print(Banner_Panel)




if __name__ == "__main__":

    Clear_Terminal()

    Clear_Pycache()

    Display_Banner()
