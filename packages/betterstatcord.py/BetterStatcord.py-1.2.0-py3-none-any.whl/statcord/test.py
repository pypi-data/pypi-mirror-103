from client import StatcordClient
from discord.ext import commands


def main():
    bot = commands.Bot(command_prefix="!")

    bot.statcord_client = StatcordClient(bot, "statcord.com-ILBdvQm95oHZuv3jXVyo")

    bot.run("NzEyNzI3Mjk2MTQxNjg4OTIy.XsVxBQ.rhXPoB9Xp-AvbeS9cePItKLkDtU")


if __name__ == "__main__":
    main()
