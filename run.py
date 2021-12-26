import os
from colorama import Fore, Style
import requests

with open("ascii.txt") as f:
    print(Fore.CYAN + f.read())

print(Fore.YELLOW + Style.BRIGHT + "A Discord bot that lets you play space invaders"
      + Style.RESET_ALL)

if not os.path.isfile(".env"):
    print(Fore.CYAN + "Looks like you're running the bot for first time.")
    print("Before continuing the configuration step, I need your token" + Style.RESET_ALL)
    token = None
    while True:
        try:
            token = input("Your Discord bot token: ")
            print(Fore.BLUE + "Checking the token...")
            r = requests.get("https://discord.com/api/v9/users/@me",
                             headers={"Authorization": f"Bot {token}"})
            js = r.json()
            if js["message"]:
                print(
                    Fore.RED + f"Your token is invalid! Error code: {js['message']}" + Style.RESET_ALL)
                continue
        except KeyError:
            break
    print(Fore.GREEN + "Your token is valid!")
    prefix = input(
        Fore.WHITE + "Your bot's prefix (leave empty to default prefix): ")
    if not prefix:
        prefix = "$"
    print(Fore.BLUE + "Configuring...")
    with open('.env', 'x') as env:
        env.write(f"# This is generated configuration. Don't try to edit unless if you know what are you doing\nDISCORD_TOKEN={token}\nDISCORD_PREFIX={prefix}\nDEBUGGING=0")
        env.close()
    print(Fore.GREEN + "Finished!")

if __name__ == "__main__":
    print(f"{Fore.CYAN}The bot is now running! Press {Style.BRIGHT}Ctrl+C{Style.NORMAL} to stop!{Style.RESET_ALL}")
    import src.main
