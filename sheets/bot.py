import cv2
import discord
import io
import logging
import numpy as np
import json

from collections import defaultdict
from discord.ext import commands
from sheets.prepare import process

pic_ext = ['.jpg','.png','.jpeg']

class DataBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sp(self, ctx):
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                for ext in pic_ext:
                    if attachment.filename.endswith(ext):
                        obj = await attachment.read()
                        nparr = np.frombuffer(obj, np.uint8)
                        im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        data, out = process(im)

                        j_io = io.BytesIO()
                        json_str = json.dumps(data, indent=4, sort_keys=True)
                        json_bytes = json_str.encode("utf-8")
                        j_io.write(json_bytes)
                        j_io.seek(0)
                        j_file = discord.File(j_io, filename="stockpile.json")

                        success, buffer = cv2.imencode(".jpg", out)
                        i_io = io.BytesIO(buffer)
                        i_file = discord.File(i_io, filename="stockpile.jpg")
                        
                        await ctx.send(
                            "Highlighted red was not able to be identified",
                            files=[i_file, j_file])

                        return

def run():
    logging.basicConfig(handlers = [logging.FileHandler('_bot.log', 'w', 'utf-8')],
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    bot = DataBot(command_prefix='!', description='Data Core Bot.')
    @bot.event
    async def on_ready():
        print(f'{bot.user.name}: {bot.user.id}')

    with open('_bot.creds', 'r') as file:
        creds = file.read()

    bot.add_cog(Main(bot))
    bot.run(creds)

if __name__ == '__main__':
    run()