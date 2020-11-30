import requests
import urllib
from bs4 import BeautifulSoup
import os

def getTier(Summoner):
    Tier = []
    name = urllib.parse.quote(Summoner)
    url = "https://www.op.gg/summoner/userName=" + name
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    Tier.append(soup.select('div.TierRank')[0].get_text().replace('\n', '').replace('\t', ''))
    Tier.append(soup.select('div.sub-tier__rank-tier')[0].get_text().replace('  ', '').replace('\n', ''))
    return Tier

import discord, asyncio, os
from discord.ext import commands

class chatbot(discord.Client):
    # 프로그램이 처음 실행되었을 때 초기 구성
    async def on_ready(self):
        self.command = ["!자기소개", "!info", "!add", "!del", "!reset", "!li", "!div", "!나쁜말", "!말"]
        self.civilWarPersonnel = []
        self.userTier = []
        self.friend  = []#["성은이", "민학이", "수빈이", "휘명이", "태영이"]
        self.stimulation = []
        self.reaction = []
        self.switch = False
        self.change = False
        self.changeIndex = 0
        self.pilter = False
        self.badWord = []

        # 상태 메시지 설정
        # 종류는 3가지: Game, Streaming, CustomActivity
        game = discord.Game("!자기소개")

        # 계정 상태를 변경한다.
        # 온라인 상태, game 중으로 설정
        await client.change_presence(status=discord.Status.online, activity=game)

        # 준비가 완료되면 콘솔 창에 "READY!"라고 표시
        print("READY")

    # 봇에 메시지가 오면 수행 될 액션
    async def on_message(self, message):
        # SENDER가 BOT일 경우 반응을 하지 않도록 한다.
        if message.author.bot:
            return None

        # message.content = message의 내용
        if message.content[0] == "!":
            if message.content[1::] in self.friend:
                channel = message.channel
                msg = message.content[1::] + " 바보"
                await channel.send(msg)
                return None

        if self.pilter:
            for i in self.badWord:
                if message.content.find(i) >= 0:
                    for i in self.stimulation:
                        if i.find(message.content) >= 0:
                            msg = "그 말은 배운 말이라 삭제할 수 없엉.."
                            channel = message.channel
                            await channel.send(msg)
                            return None
                    channel = message.channel
                    msg = "그 말 쓰면 나빠!"
                    await channel.send(msg)
                    await message.delete()
                    return None


        #await bot.process_commands(message)



        if message.content == "!나쁜말":
            if self.pilter == False:
                self.pilter = True
                channel = message.channel
                msg = "나쁜말 필터링 ON!"
                await channel.send(msg)
            elif self.pilter == True:
                self.pilter = False
                channel = message.channel
                msg = "나쁜말 필터링 OFF!"
                await channel.send(msg)
            return None

        elif message.content.startswith("!나쁜말"):
            if message.content[len(message.content) - 2::] == "삭제":
                self.badWord.remove(message.content[5:len(message.content) - 3])
                channel = message.channel
                msg = "나쁜말 까먹었다!"
                await channel.send(msg)
            else:
                if not message.content in self.stimulation and self.command[7].find(message.content[5::]) == -1:
                    self.badWord.append(message.content[5::])
                    channel = message.channel
                    msg = "나쁜말 배웠어요!"
                    await channel.send(msg)
                else:
                    channel = message.channel
                    msg = "그 말은 이미 배운 말이거나 명령어라 나쁜말로 배울 수 없어요.."
                    await channel.send(msg)
            return None

        if message.content.startswith("!자기소개"):
            embed=discord.Embed(title="명령어 모음", description="돌멍이 설명서입니다.", color=0x00ff56)
            embed.set_author(name="돌멍이", url="https://seoneun.github.io/", icon_url="https://support.discord.com/system/photos/3619/7737/4794/profile_image_423727170454_678183.jpg")
            embed.set_thumbnail(url="https://p4.wallpaperbetter.com/wallpaper/205/130/329/malphite-poro-wallpaper-preview.jpg")
            embed.add_field(name="!자기소개", value="사용가능한 명령어를 알려줍니다.", inline=True)
            embed.add_field(name="!info 소환사명.", value="소환사의 정보를 알려줍니다.", inline=True)
            embed.add_field(name="!add 소환사명.", value="내전에 참가할 소환사를 추가합니다", inline=True)
            embed.add_field(name="!del 소환사명.", value="내전목록에서 제거할 소환사를 추가합니다", inline=True)
            embed.add_field(name="!reset", value="내전목록을 초기화합니다.", inline=True)
            embed.add_field(name="!li", value="내전에 참가한 소환사 목록을 불러옵니다.", inline=True)
            embed.add_field(name="!div", value="밸런스에 맞게 팀을 나눕니다.", inline=True)
            embed.add_field(name="!가르친말 수정", value="가르친 말 뒤에 수정을 붙이면 가르쳤던 말을 수정시킬 수 있습니다.", inline=True)
            embed.add_field(name="!가르친말 삭제", value="가르친 말 뒤에 삭제를 붙이면 가르쳤던 말을 삭제시킬 수 있습니다.", inline=True)
            embed.add_field(name="!나쁜말", value="나쁜말을 필터링 하는 기능을 On/OFF 합니다. 뒤에 말을 붙이면 그 말을 나쁜말로 등록할 수 있습니다.", inline=True)
            embed.add_field(name="!나쁜말 말 삭제", value="등록된 나쁜말을 삭제합니다.", inline=True)
            embed.add_field(name="!말", value="가르친 말들을 보여줍니다.", inline=True)
            embed.set_footer(text="ver 1.0.2")
            await message.channel.send(embed=embed)

        try:
            if message.content.startswith("!info"):
                name = message.content[6::]
                SummonerName = urllib.parse.quote(name)
                url = "https://www.op.gg/summoner/userName=" + SummonerName
                res = requests.get(url)
                soup = BeautifulSoup(res.content, 'html.parser')
                icon_url = "https:" + soup.select('div.ProfileIcon img')[0]["src"]
                embed=discord.Embed(title = "소환사 정보", color=0x00ff56)
                embed.set_thumbnail(url=icon_url)
                embed.add_field(name = name, value= "개인/2인전 랭크: " + getTier(name)[0] + "\n 자유랭크: " + getTier(name)[1], inline=True)
                await message.channel.send(embed=embed)
        except:
            print("error_code(info)")
            channel = message.channel
            msg = "그딴 소환사는 없어요!"
            await channel.send(msg)
            return None
        try:
            if message.content.startswith("!add"):
                name = message.content[5::]
                if name in self.civilWarPersonnel:
                    channel = message.channel
                    msg = "이미 참가되어 있는 소환사에요!"
                    await channel.send(msg)
                    return None
                self.civilWarPersonnel.append(name)
                self.userTier.append(getTier(name))
                embed=discord.Embed(title= "내전 참가자 (현재인원: " + str(len(self.civilWarPersonnel)) + "명)", color=0x00ff56)
                embed.add_field(name = name, value= "개인/2인전 랭크: " + self.userTier[len(self.civilWarPersonnel) - 1][0] + "\n 자유랭크: " + self.userTier[len(self.civilWarPersonnel) - 1][1], inline=True)
                await message.channel.send(embed=embed)
        except:
            print("error_code(add)")

        if message.content.startswith("!del"):
            name = message.content[5::]
            if not name in self.civilWarPersonnel:
                print("error_code(del)")
                channel = message.channel
                msg = "참가되어있지 않는 소환사입니당 ㅎ"
                await channel.send(msg)
                return None

            user = self.civilWarPersonnel.index(name)
            del self.userTier[user]
            del self.civilWarPersonnel[user]
            embed=discord.Embed(title = name + "님을 내전 목록에서 제거합니다. (현재인원: " + str(len(self.civilWarPersonnel)) + "명)", color=0x00ff56)
            embed.add_field(name = name, value= "개인/2인전 랭크: " + getTier(name)[0] + "\n 자유랭크: " + getTier(name)[1], inline=True)
            await message.channel.send(embed=embed)

        if message.content.startswith("!reset"):
            del self.civilWarPersonnel[:]
            embed=discord.Embed(title = "내전 목록을 초기화합니다.", color=0x00ff56)
            await message.channel.send(embed=embed)

        if message.content.startswith("!li"):
            name = message.content[5::]
            embed=discord.Embed(title = name + "내전 참가자 목록 (현재인원: " + str(len(self.civilWarPersonnel)) + "명)", color=0x00ff56)
            for i in range(len(self.civilWarPersonnel)):
                embed.add_field(name = self.civilWarPersonnel[i], value= "개인/2인전 랭크: " + self.userTier[i][0] + "\n 자유랭크: " + self.userTier[i][1], inline=True)
            await message.channel.send(embed=embed)

        if message.content.startswith("!div"):
            print(self.userTier)
            balance_name = self.civilWarPersonnel[::]
            balance_tier = []
            balance = []
            for tier in self.userTier:
                if tier[0] == "Unranked":
                    balance_tier.append(0)
                elif tier[0].startswith("Iron"):
                    if tier[0][5] == "5":
                        balance_tier.append(1)
                    if tier[0][5] == "4":
                        balance_tier.append(2)
                    if tier[0][5] == "3":
                        balance_tier.append(3)
                    if tier[0][5] == "2":
                        balance_tier.append(4)
                    if tier[0][5] == "1":
                        balance_tier.append(5)
                elif tier[0].startswith("Bronze"):
                    if tier[0][7] == "5":
                        balance_tier.append(10)
                    if tier[0][7] == "4":
                        balance_tier.append(15)
                    if tier[0][7] == "3":
                        balance_tier.append(20)
                    if tier[0][7] == "2":
                        balance_tier.append(25)
                    if tier[0][7] == "1":
                        balance_tier.append(30)
                elif tier[0].startswith("Silver"):
                    if tier[0][7] == "5":
                        balance_tier.append(40)
                    if tier[0][7] == "4":
                        balance_tier.append(50)
                    if tier[0][7] == "3":
                        balance_tier.append(60)
                    if tier[0][7] == "2":
                        balance_tier.append(70)
                    if tier[0][7] == "1":
                        balance_tier.append(80)
                elif tier[0].startswith("Gold"):
                    if tier[0][5] == "5":
                        balance_tier.append(95)
                    if tier[0][5] == "4":
                        balance_tier.append(110)
                    if tier[0][5] == "3":
                        balance_tier.append(125)
                    if tier[0][5] == "2":
                        balance_tier.append(140)
                    if tier[0][5] == "1":
                        balance_tier.append(155)
                elif tier[0].startswith("Platinum"):
                    if tier[0][9] == "5":
                        balance_tier.append(175)
                    if tier[0][9] == "4":
                        balance_tier.append(195)
                    if tier[0][9] == "3":
                        balance_tier.append(215)
                    if tier[0][9] == "2":
                        balance_tier.append(235)
                    if tier[0][9] == "1":
                        balance_tier.append(255)
                elif tier[0].startswith("Diamond"):
                    if tier[0][8] == "5":
                        balance_tier.append(280)
                    if tier[0][8] == "4":
                        balance_tier.append(305)
                    if tier[0][8] == "3":
                        balance_tier.append(330)
                    if tier[0][8] == "2":
                        balance_tier.append(355)
                    if tier[0][8] == "1":
                        balance_tier.append(380)
                elif tier[0].startswith("Master"):
                    if tier[0][7] == "5":
                        balance_tier.append(410)
                    if tier[0][7] == "4":
                        balance_tier.append(440)
                    if tier[0][7] == "3":
                        balance_tier.append(470)
                    if tier[0][7] == "2":
                        balance_tier.append(500)
                    if tier[0][7] == "1":
                        balance_tier.append(530)
                elif tier[0].startswith("Grandmaster"):
                    balance_tier.append(600)
                elif tier[0].startswith("Challenger"):
                    balance_tier.append(700)
            print(balance_tier)
            for i in range(len(balance_name)):
                balance.append([balance_name[i], balance_tier[i]])
            balance.sort(key=lambda x:x[1])
            embed=discord.Embed(title = "블루팀", color=0x00ff56)
            for i in range(int(len(self.civilWarPersonnel) / 2)):
                embed.add_field(name = balance[2*i][0], value= "개인/2인전 랭크: " + self.userTier[self.civilWarPersonnel.index(balance[2*i][0])][0] + "\n 자유랭크: " + self.userTier[self.civilWarPersonnel.index(balance[2*i][0])][1], inline=True)
            await message.channel.send(embed=embed)
            embed=discord.Embed(title = "레드팀", color=0x00ff56)
            for i in range(int(len(self.civilWarPersonnel) / 2)):
                embed.add_field(name = balance[2*i+1][0], value= "개인/2인전 랭크: " + self.userTier[self.civilWarPersonnel.index(balance[2*i+1][0])][0] + "\n 자유랭크: " + self.userTier[self.civilWarPersonnel.index(balance[2*i+1][0])][1], inline=True)
            await message.channel.send(embed=embed)

        if self.switch:
            self.switch = False
            self.reaction.append(message.content)
            channel = message.channel
            msg = "좋은 말을 배웠어요! 감사해요!"
            await channel.send(msg)
            return None

        if self.change:
            channel = message.channel
            self.change = False
            self.reaction[self.changeIndex] = message.content
            msg = "바꿨어요!"
            await channel.send(msg)
            return None


        elif message.content.startswith("!"):
            if not (message.content.startswith("!info") or message.content.startswith("!add") or message.content.startswith("!del") or message.content.startswith("!reset") or message.content.startswith("!li") or message.content.startswith("!div") or message.content.startswith("!자기소개") or message.content.startswith("!말") or message.content.startswith("!나쁜말")):
                channel = message.channel
                if not message.content in self.stimulation:
                    if message.content[len(message.content) - 2::] == "수정" and message.content[0:len(message.content)-3] in self.stimulation:
                        msg = "어떻게 바꿀까요?"
                        await channel.send(msg)
                        self.change = True
                        self.changeIndex = self.stimulation.index(message.content[0:len(message.content)-3])
                        return None
                    elif message.content[len(message.content) - 2::] == "삭제" and message.content[0:len(message.content)-3] in self.stimulation:
                        msg = "돌멍이 까먹었다!"
                        await channel.send(msg)
                        del self.reaction[self.stimulation.index(message.content[0:len(message.content)-3])]
                        self.stimulation.remove(message.content[0:len(message.content)-3])
                        return None
                    self.stimulation.append(message.content)
                    msg = "모르는 말인 것이와요... 가르쳐주세오!"
                    await channel.send(msg)
                    self.switch = True
                    return None
                else:
                    msg = self.reaction[self.stimulation.index(message.content)]
                    await channel.send(msg)
                    return None

        if message.content.startswith("!말"):
            embed=discord.Embed(title="가르친 말 모음", description="나 이 말 안다!", color=0x00ff56)
            for i in range(len(self.stimulation)):
                embed.add_field(name=self.stimulation[i], value=self.reaction[i], inline=True)
            await message.channel.send(embed=embed)
            embed=discord.Embed(title="가르친 나쁜말 모음", description="이 말 나쁘다!", color=0x00ff56)
            for i in range(len(self.badWord)):
                embed.add_field(name=self.badWord[i], value="이 말 하지마라..", inline=True)
            await message.channel.send(embed=embed)
            return None


# 프로그램이 실행되면 제일 처음으로 실행되는 함수
if __name__ == "__main__":
    # 객체를 생성
    client = chatbot()
    # TOKEN 값을 통해 로그인하고 봇을 실행
    client.run(os.environ['token'])
