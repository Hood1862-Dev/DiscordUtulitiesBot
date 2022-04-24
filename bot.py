import discord 
import asyncio
import discord.utils
from discord.ext import commands 
from discord import utils
from discord import Activity, ActivityType
from discord.utils import get 
from discord.ext.commands import has_permissions, MissingPermissions 
from asyncio import sleep
 
BOT_PREFIX = r'.' #prefix
 
bot = commands.Bot(command_prefix=BOT_PREFIX) 
bot.remove_command('help')
@bot.event
async def on_ready():
          await bot.change_presence(status=discord.Status.online,activity=discord.Streaming(name="discord.gg/dqnN2knpsZ", url="https://www.twitch.tv/scpsl_official"))
            print("Бот включен: " + bot.user.name + "\n") #twitch stats
            
#create private room
@bot.event
async def on_voice_state_update(member,befor,after):
    if after.channel.id == 915144957453561867:     #channel id(when user is join to this channel, a personal channel is created for this user)
        for guild in bot.guilds:
            maincategory = discord.utils.get(guild.categories, id=872013756165652511)
            channel2 = await guild.create_voice_channel(name=f'Комната {member.display_name}',category = maincategory)
            await channel2.set_permissions(member,connect=True,mute_members=True,move_members=True,manage_channels=True)
            await member.move_to(channel2)
            def check(x,y,z):
                return len(channel2.members) == 0
            await bot.wait_for('voice_state_update',check=check)
            await channel2.delete()   

#auto channel message reaction
@bot.event
async def on_message(message):
  channel = message.channel
  if channel.id == 812280979359531030: #channel1
    await message.add_reaction("👍")  
    await message.add_reaction("👎")
  if channel.id == 826144443274362931: #channel2
    await message.add_reaction("👍")  
    await message.add_reaction("👎")
  if channel.id == 741338493900554351: #channel3
    await message.add_reaction("👍")  
    await message.add_reaction("👎")
  if channel.id == 741319609558237314: #channel4
    await message.add_reaction("👍")   
    await message.add_reaction("👎")
  if channel.id == 799874030672543764: #channel5
    await message.add_reaction("👋")  

  pred = ['', '', '', '', '', '']
  for x in pred:
      if x in message.content:
          await message.add_reaction("👍")   
          await message.add_reaction("👎")    
  await bot.process_commands(message)

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
        deleted = await ctx.message.channel.purge(limit=amount + 1)

#mute
@bot.command()
@commands.has_permissions(view_audit_log=True)
async def muteall(ctx,member:discord.Member,time,*,reason=None):
    muterole = discord.utils.get(ctx.guild.roles,id=826395150196277289)
    unit = time[-1]
    if unit == 's':
        duration= int(time[:-1])
        longunit = 'секунд'
    elif unit == 'm':
        duration= int(time[:-1]) * 60
        longunit = 'минут'
    elif unit == 'h':
        duration= int(time[:-1]) * 60 * 60
        longunit = 'часов'
    else:
        await ctx.send('Неправильное время! Используйте `s`, `m` или `h` на конце сообщения.')
    await member.add_roles(muterole)
    await ctx.send(f"Вы замутили {member.mention} во всех каналах на **{time}** причина: **{reason}**")
    await asyncio.sleep(duration )
    await member.remove_roles(muterole)
    await ctx.send(f'{member.mention}, вы были размучены по истечению времени во всех каналах.')

@bot.command()
@commands.has_permissions(view_audit_log=True)
async def mutechannel(ctx, member:discord.Member, channel:discord.TextChannel, time, *, reason):
    await channel.set_permissions(member, send_messages=False)
    unit = time[-1]
    if unit == 's':
        duration= int(time[:-1])
        longunit = 'секунд'
    elif unit == 'm':
        duration= int(time[:-1]) * 60
        longunit = 'минут'
    elif unit == 'h':
        duration= int(time[:-1]) * 60 * 60
        longunit = 'часов'
    else:
        await ctx.send('Неправильное время! Используйте `s`, `m` или `h` на конце сообщения.')
    await ctx.send(f"Вы замутили {member.mention} в канале {channel.mention} на **{time}** причина: **{reason}**")
    await asyncio.sleep(duration)
    await ctx.send(f'{member.mention}, вы были размучены по истечению времени в канале {channel.mention}.')
    await channel.set_permissions(member, overwrite=None)

#error
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Вы не указали аргументы, {ctx.author.mention}!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, у вас нет доступа к этой команде!")

#say embed command
@bot.command()
@commands.has_any_role(741317540990419078, 741318739605323777) #roles, which can using this command
async def content(ctx,msg:int):
    msg = await ctx.channel.fetch_message(msg)
    prefix = r'\\'
    if len(msg.embeds) > 0:
        ds = t = f = c = a =img = thm = None
        embed = msg.embeds[0]
        if embed.description != discord.Embed.Empty:
            ds = f'$d {embed.description}'
        else:
            ds = ''
        if embed.title != discord.Embed.Empty:
            t = f'$t {embed.title}'
        else:
            t = ''
        if embed.thumbnail.url != discord.Embed.Empty:
            thm = f'$thumb {embed.thumbnail.url}'
        else: 
            thm = ''
        if embed.image.url != discord.Embed.Empty:
            img = f'$image {embed.image.url}'
        else:
            img = ''
        if embed.footer.text != discord.Embed.Empty:
            f = f'$f {embed.footer.text}'
        else:
            f = '$f -'
        if embed.author.name != discord.Embed.Empty:
            a = f'$a @{embed.author.name}'
        else:
            a = f'$a -'
        if embed.colour != discord.Embed.Empty:
            c = f'$c {embed.colour}'
        else:
            c = f''
        if embed.footer.icon_url != discord.Embed.Empty:
            fu = f'$fu {embed.footer.icon_url}'
        else:
            fu = ''
        
        await ctx.send(f'\n```{prefix}say {c} {a} {t} {ds} {f} {img} {thm} {fu}```')

@bot.command()
@commands.has_any_role(741317540990419078, 741318739605323777) 
async def edit(ctx,msg1:int, *, msg: str = None):
    msg12 = await ctx.channel.fetch_message(msg1)
    role = discord.utils.get(ctx.guild.roles,id=741317540990419078)
    role1 = discord.utils.get(ctx.guild.roles,id=741318739605323777)
    roler = [741317540990419078, 741318739605323777]
    if msg:
        ptext = title = description = image = thumbnail = url = footer = author = color = simple = channel = foothericon = None
        img = thm = ds = t = u = fo = au = colo = smpl = None
        if len(msg12.embeds) > 0:
            old_em = msg12.embeds[0]
        if old_em.description != discord.Embed.Empty:
            ds = old_em.description
        if old_em.title != discord.Embed.Empty:
            t = old_em.title
        if old_em.thumbnail.url != discord.Embed.Empty:
            thm = old_em.thumbnail.url
        if old_em.image.url != discord.Embed.Empty:
            img = old_em.image.url
        if old_em.url != discord.Embed.Empty:
            u = old_em.url
        if old_em.author.name != discord.Embed.Empty:
            a = old_em.author.name
        if old_em.author.icon_url != discord.Embed.Empty:
            ai = old_em.author.icon_url
        if old_em.footer.text != discord.Embed.Empty:
            fo = old_em.footer.text
        if msg12.content is not None:
            smpl = msg12.content
        embed_values = msg.split('$')
        for i in embed_values:
            if i.strip().lower().startswith('msg '):
                ptext = i.strip()[3:].strip()
            elif i.strip().lower().startswith('t '):
                title = i.strip()[2:].strip()
            elif i.strip().lower().startswith('d '):
                description = i.strip()[2:].strip()
            elif i.strip().lower().startswith('image '):
                image = i.strip()[6:].strip()
            elif i.strip().lower().startswith('thumb '):
                thumbnail = i.strip()[6:].strip()
            elif i.strip().lower().startswith('url '):
                url = i.strip()[2:].strip()
            elif i.strip().lower().startswith('f '):
                footer = i.strip()[2:].strip()
            elif i.strip().lower().startswith('a '):
                author = i.strip()[2:].strip()
            elif i.strip().lower().startswith('c '):
                color = i.strip()[2:].strip()
            elif i.strip().lower().startswith('m '):
                simple = i.strip()[3:].strip()
            elif i.strip().lower().startswith('ch '):
                channel = i.strip()[3:].strip()
            elif i.strip().lower().startswith('fu '):
                foothericon = i.strip()[3:].strip()

        if ptext is title is description is image is thumbnail is url is footer is author is color is foothericon is None and 'field=' not in msg:
            if role in ctx.author.roles or role1 in ctx.author.roles:
                return await ctx.send(content=msg)

            else:
                return await ctx.send(content=f'{ctx.author.mention}, у вас не хватает прав!')
        if not ptext:
            if smpl:
                ptext = smpl
        if not title:
                title = t
        if not description:
            description = ds
        if color:
            if "#" in color:
                afa = color[+1] 
                bfa = color[+2]
                cfa = color[+3] 
                dfa = color[+4] 
                efa = color[+5] 
                ffa = color[+6]
                colo = afa+bfa+cfa+dfa+efa+ffa
                color = discord.Color(value=int(colo, 16))
            else:
                color = discord.Color(value=int(color, 16))
        if not color:
            color = old_em.color
        if ptext:
            if role in ctx.author.roles or role1 in ctx.author.roles:
                if ptext == 'here' or ptext == 'everyone' or ptext.startswith('<@'):
                    if ptext == 'here':
                        ptext = '@here'
                    elif ptext == 'everyone':
                        ptext = '@everyone'
                    elif ptext.startswith('<@&'):
                        role = ptext.split()
                        role = role[0]
                        role = role[3:]
                        role = role[:-1]
                        roled = discord.utils.get(ctx.guild.roles, id=int(role))

                        if str(roled.color) != '#000000':
                            color = roled.color
                        if 'color' not in locals():
                            color = 0
                        
                        ptext = f'{ptext}'
            else:
                ptext = None
        if not simple:
            em = discord.Embed(title=title, description=description, color=color)
        if not url:
            if u:
                em = discord.Embed(title=title, description=description, url=u, color=color)
        if url:
            em = discord.Embed(title=title, description=description, url=url, color=color)
        if author:
            if role in ctx.author.roles or role1 in ctx.author.roles:
                if author == '-':
                    pass
                else:
                    if author.startswith('<@!'):
                        author = author[3:]
                        author = author[:-1]
                    else:
                        author = author[2:]
                        author = author[:-1]
                    fm2 = await bot.fetch_user(int(author))
                    em.set_author(name=f"{fm2}",icon_url=f"{fm2.avatar_url}")
            else:
                em.set_author(name=f"{ctx.author}",icon_url=f"{ctx.message.author.avatar_url}")
        if not author:
            em.set_author(name=a, icon_url=ai)
        if not image:
            if img:
                em.set_image(url=img)
        if image:
            em.set_image(url=image)
        if not thumbnail:
            if thm:
                em.set_thumbnail(url=thm)
        if thumbnail:
            em.set_thumbnail(url=thumbnail)
        if footer:
            if role in ctx.author.roles or role1 in ctx.author.roles:
                if footer == '-':
                    pass
                else:
                    if foothericon:
                        if 'icon=' in footer:
                            text, icon = footer.split('icon=')
                            em.set_footer(text=text.strip()[5:], icon_url=foothericon)
                        else:
                            em.set_footer(text=f"{footer}", icon_url=foothericon)
                    else:
                        if 'icon=' in footer:
                            ext, icon = footer.split('icon=')
                            em.set_footer(text=text.strip()[5:])
                        else:
                            em.set_footer(text=f"{footer}")
            else:
                em.set_footer(text=f"FOOTER TEXT") #footer text
        if not footer:
            if foothericon:
                em.set_footer(text=fo, icon_url=foothericon)
            else:
                em.set_footer(text=fo)
        await msg12.edit(content=ptext, embed=em)

    else:
        if len(msg12.embeds) > 0:
            if msg12.content is not None:
                await msg12.edit(content=msg12.content,embed=msg12.embeds[0])
            else:
                await msg12.edit(embed=msg12.embeds[0])
        if len(msg12.embeds) == 0:
            await msg12.edit(content=msg12.content)

#say command
@bot.command()
async def say(ctx, *, msg: str = None):
    role = discord.utils.get(ctx.guild.roles,id=741317540990419078) 
    role1 = discord.utils.get(ctx.guild.roles,id=741318739605323777) 
    roler = [741317540990419078, 741318739605323777]
    if msg:
        ptext = title = description = image = thumbnail = url = footer = author = color = simple = channel = foothericon = None
        embed_values = msg.split('$')
        for i in embed_values:
            if i.strip().lower().startswith('msg '):
                ptext = i.strip()[3:].strip()
            elif i.strip().lower().startswith('t '):
                title = i.strip()[2:].strip()
            elif i.strip().lower().startswith('d '):
                description = i.strip()[2:].strip()
            elif i.strip().lower().startswith('image '):
                image = i.strip()[6:].strip()
            elif i.strip().lower().startswith('thumb '):
                thumbnail = i.strip()[6:].strip()
            elif i.strip().lower().startswith('url '):
                url = i.strip()[4:].strip()
            elif i.strip().lower().startswith('f '):
                footer = i.strip()[2:].strip()
            elif i.strip().lower().startswith('a '):
                author = i.strip()[2:].strip()
            elif i.strip().lower().startswith('c '):
                color = i.strip()[2:].strip()
            elif i.strip().lower().startswith('m '):
                simple = i.strip()[3:].strip()
            elif i.strip().lower().startswith('ch '):
                channel = i.strip()[3:].strip()
            elif i.strip().lower().startswith('fu '):
                foothericon = i.strip()[3:].strip()

        if ptext is title is description is image is thumbnail is url is footer is author is color is foothericon is None and 'field=' not in msg:
            if role in ctx.author.roles or role1 in ctx.author.roles:
                return await ctx.send(content=msg)

            else:
                return await ctx.send(content='Отсутствуют аргументы :/')
        if color:
            if "#" in color:
                afa = color[+1] 
                bfa = color[+2]
                cfa = color[+3] 
                dfa = color[+4] 
                efa = color[+5] 
                ffa = color[+6]
                colo = afa+bfa+cfa+dfa+efa+ffa
                color = discord.Color(value=int(colo, 16))
            else:
                color = discord.Color(value=int(color, 16))
        if not color:
            color = 0x2f3136
        if ptext:
            if role in ctx.author.roles or role1 in ctx.author.roles:
                if ptext == 'here' or ptext == 'everyone' or ptext.startswith('<@'):
                    if ptext == 'here':
                        ptext = '@here'
                    elif ptext == 'everyone':
                        ptext = '@everyone'
                    elif ptext.startswith('<@&'):
                        role = ptext.split()
                        role = role[0]
                        role = role[3:]
                        role = role[:-1]
                        roled = discord.utils.get(ctx.guild.roles, id=int(role))

                        if str(roled.color) != '#000000':
                            color = roled.color
                        if 'color' not in locals():
                            color = 0
                        
                        ptext = f'{ptext}'
            else:
                ptext = None
        if not simple:
            em = discord.Embed(title=title, description=description, color=color)
        else:
            await ctx.message.delete()
            if not channel:
                await ctx.send(simple)
            else:
                if role in ctx.author.roles or role1 in ctx.author.roles:
                    channel = channel[2:]
                    channel = channel[:-1]
                    channel = bot.get_channel(int(channel))
                    await channel.send(simple)
                    return
                else:
                    await ctx.send(content=ptext, embed=em)
        if url:
            em = discord.Embed(title=title, description=description, url=url, color=color)
        if author:
            print(len(author))
            if role in ctx.author.roles or role1 in ctx.author.roles:
                if author == '-':
                    pass
                else:
                    if author.startswith('<@!'):
                        author = author[3:]
                        author = author[:-1]
                    else:
                        author = author[2:]
                        author = author[:-1]
                    fm2 = await bot.fetch_user(int(author))
                    em.set_author(name=f"{fm2}",icon_url=f"{fm2.avatar_url}")
            else:
                em.set_author(name=f"{ctx.author}",icon_url=f"{ctx.message.author.avatar_url}")
        if not author:
            em.set_author(name=f"{ctx.author}",icon_url=f"{ctx.message.author.avatar_url}")
        if image:
            em.set_image(url=image)
        if thumbnail:
            em.set_thumbnail(url=thumbnail)
        if footer:
            if role in ctx.author.roles or role1 in ctx.author.roles:
                if footer == '-':
                    pass
                else:
                    if foothericon:
                        if 'icon=' in footer:
                            text, icon = footer.split('icon=')
                            em.set_footer(text=text.strip()[5:], icon_url=foothericon)
                        else:
                            em.set_footer(text=f"{footer}", icon_url=foothericon)
                    else:
                        if 'icon=' in footer:
                            ext, icon = footer.split('icon=')
                            em.set_footer(text=text.strip()[5:])
                        else:
                            em.set_footer(text=f"{footer}")
            else:
                em.set_footer(text=f"footer text") #footer text
        if not footer:
            if foothericon:
                em.set_footer(text=f"footer text") #footer text
            else:
                em.set_footer(text=f"footer text") #footer text
        if not channel:
            await ctx.send(content=ptext, embed=em)
        else:
            if role in ctx.author.roles or role1 in ctx.author.roles:
                channel = channel[2:]
                channel = channel[:-1]
                channel = bot.get_channel(int(channel))
                await channel.send(content=ptext, embed=em)
            else:
                await ctx.send(content=ptext, embed=em)

    else:
        await ctx.send(f"Вы не указали аргументы, {ctx.author.mention}!\nВозможный способ использование:\n```r'\\'say $a MENTION $c HEX $t TITLE TEXT $d DESC TEXT $f FOOTER TEXT $fu URL $image URL $thumb URL```")

bot.run('bot.token')
