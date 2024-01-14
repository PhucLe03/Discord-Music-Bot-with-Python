# from ast import alias
import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
# import asyncio

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio'}
        # self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'options': '-vn'}

        self.vc = None

     #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            print(item)
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False
        # return {'source': info['formats'][0]['url'], 'title': info['title']}
        return {'source': info['url']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))#, after=lambda e: self.play_next())
            # ctx.voice_client.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        # print('playyyy')
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            # print (m_url)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))#, after=lambda e: self.play_next())
            # ctx.voice_client.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))
        else:
            self.is_playing = False

    @commands.command(name="join", aliases=['j'], help="Join voice")
    async def hairu(self, ctx):
        # print('jjjj')
        voice = ctx.author.voice
        if voice is None or voice.channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("You need to be connected to a voice channel!")
        if ctx.voice_client is None:
            self.vc = await voice.channel.connect()
        else:
            await ctx.voice_client.move_to(voice)
            self.vc = ctx.voice_client

    @commands.command(name="play", aliases=['p'], help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = " ".join(args)
        
        voice = ctx.author.voice
        if voice is None or voice.channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("You need to be connected to a voice channel!")
        else:
            if (self.vc == "" or self.vc == None or not self.vc.is_connected()):
                self.vc = await voice.channel.connect()
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice.channel])
                
                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue", aliases=['q'], help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="skip", aliases=['s'], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music()
            
    @commands.command(name="disconnect", aliases=['d'], help="Disconnecting bot from VC")
    async def dc(self, ctx):
        await self.vc.disconnect()
        # await ctx.voice_client.disconnect()