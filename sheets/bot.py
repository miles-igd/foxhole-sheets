import csv, cv2
import discord
import io
import logging
import numpy as np
import json

from collections import defaultdict
from discord.ext import commands
from sheets.core import process

pic_ext = ['.jpg','.png','.jpeg']

class DataBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def to_csv(self, data):
        '''
        Inputs: 
        data: dict

        Of the type {str: str}

        Outputs:
        discord.File
        '''
        items = sorted([(k, v) for k, v in data.items()], key=lambda x: x[0])
        csv_io = io.StringIO()
        writer = csv.writer(csv_io)
        writer.writerows(items)
        csv_bytes = csv_io.getvalue().encode("utf-8")
        csv_io = io.BytesIO(csv_bytes)
        csv_file = discord.File(csv_io, filename="stockpile.csv")

        return csv_file

    async def to_json(self, data):
        '''
        Inputs: 
        data: dict

        Of the type {str: str}

        Outputs:
        discord.File
        '''
        json_str = json.dumps(data, indent=4, sort_keys=True)
        json_bytes = json_str.encode("utf-8")
        json_io = io.BytesIO(json_bytes)
        json_file = discord.File(json_io, filename="stockpile.json")

        return json_file

    @commands.command()
    async def sp(self, ctx, *args):
        '''
        Main command to parse a stockpile image using this bot. 
        1st argument can be 'csv' which outputs a .csv file, otherwise a .json file is used
        '''
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                for ext in pic_ext:
                    if attachment.filename.endswith(ext):
                        obj = await attachment.read()
                        nparr = np.frombuffer(obj, np.uint8)
                        im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        data, out, found_unidentified = process(im)

                        for k, v in data.items():
                            data[k] = v.replace("k+", "000")

                        if args:
                            if args[0] == "csv":
                                data_file = await self.to_csv(data)
                            else:
                                data_file = await self.to_json(data)
                        else:
                            data_file = await self.to_json(data)

                        success, buffer = cv2.imencode(".jpg", out)
                        image_io = io.BytesIO(buffer)
                        image_file = discord.File(image_io, filename="stockpile.jpg")
                        
                        if found_unidentified:
                            await ctx.send(
                                "Unidentified items found - Highlighted in red",
                                files=[image_file, data_file])
                        else:
                            await ctx.send(
                                files=[data_file])

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