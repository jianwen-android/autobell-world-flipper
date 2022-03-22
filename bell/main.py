# https://kantai235.github.io/UsingPythonOpenCvAdb/
from rich.progress import Console

from functions import (
    find,
    press,
    ButtonNotFound,
    FailedToJoinLobby,
    FailedToEnterGame,
    FailedToCompleteGame,
    windows,
)
from pathlib import Path
import subprocess as sp
from time import sleep

console = Console()

if Path(__file__).parent.name == "bell":
    root = Path(__file__).parent.parent.resolve()
elif Path(__file__).parent.name == "world-flipper":
    root = Path(__file__).parent.resolve()

pics = root / "src"

success = 0
joinGame = 0
failedGame = 0

if windows:
    clearCommand = ["powershell", "-command", "clear"]
else:
    clearCommand = ["zsh", "-c", "clear"]

while True:
    try:
        try:
            with console.status("[bold green]Looking for bell", spinner="bounce"):
                # wait for bell
                find(pics / "bell.png", -1, True)
                console.log("Bell [bold green]found[/bold green]!")
            with console.status("Accepting and readying", spinner="bounce"):
                # wait for accept button to show
                find(pics / "accept.png", -1, True)
                # while the ok button doesnt show, look for readyup image
                while not find(pics / "ready.png", 0, True)[0]:
                    if find(pics / "ok.png", 0, True)[0]:
                        raise FailedToJoinLobby
                console.log("Readied up")
            # while the worldFlipper logo doesnt show, look for ok error image
            while not find(pics / "worldFlipper.png", 0, False)[0]:
                if find(pics / "ok.png", 0, True)[0]:
                    raise FailedToEnterGame
            with console.status("[bold orange]Quest in progress", spinner="bounce"):
                while not bool(next := find(pics / "next.png", 0, False)[1:]):
                    if find(pics / "beads.png", 0, False)[0]:
                        raise FailedToCompleteGame
                console.log("Finished quest")
            with console.status("Exiting room", spinner="bounce"):
                for i in range(10):
                    press(*next)
                sleep(0.3)
                find(pics / "leave.png", -1, True)
        except ButtonNotFound:
            console.log("[bold red]! Timeout occured when looking for button")
        except FailedToJoinLobby:
            console.log("[bold red]![/bold red] Was not able to join room")
            joinGame += 1
            sp.run(clearCommand)
        except FailedToEnterGame:
            console.log("[bold red]![/bold red] Was not able to enter game")
            joinGame += 1
            sp.run(clearCommand)
        except FailedToCompleteGame:
            console.log("[bold red]![/bold red] You died, get good. Like actually now")
            failedGame += 1
            sp.run(clearCommand)
        else:
            console.log("Bell [bold blue]done[/bold blue]!")
            success += 1
            sp.run(clearCommand)
    except KeyboardInterrupt:
        console.log(
            f"Runs made: [bold green]{success}[/bold green], [bold orange]{joinGame}[/bold orange], [bold red]{failedGame}[/bold red]"
        )
        console.log("Exiting")
        exit()
