import discord
import requests
from class_manager import ClassManager
from npc_manager import NpcManager
import json


class MyClient(discord.Client):
    async def on_ready(self):
        print('AE CARALHO {0} TA ONLINE!'.format(self.user))

    async def on_message(self, message):
        PRE_MESSAGE = '/'
        HELP = "Lista de Comandos disponiveis:\n" \
               "\nComandos de Roll:\n" \
               "roll X - Onde X é o número máximo\n" \
               "roll XdY - Onde X é o número de roll e Y é o número máxido de cada roll\n" \
               "\nComandos de Classe:\n" \
               "addclass|NOME|TIPO DE ARMADURA|TIPO DE ARMA|EQUIP INICIAL|PERKS - Adiciona uma classe com os atributos indicados\n" \
               "getclass NOME - Retorna os detalhes de uma classe\n" \
               "allclass - Retorna uma lista de todas classes\n" \
               "delclass NOME - Exclui uma classe com o nome escolhido\n" \
               "\nComandos de NPC:\n" \
               "addnpc|NOME|IDADE|ALIAS|NACIONALIDADE|POSIÇÃO|ESPECIALIZAÇÃO|LINK DO DOCS\n" \
               "getnpc|NOME - Retorna os detalhes de um NPC" \
               "allnpc - Retorna uma lista com nome de todos npcs"
        if message.author == client.user:
            return
        if message.content.startswith(PRE_MESSAGE + 'hello'):
            await message.channel.send('Oi caralho')
        if message.content.startswith(PRE_MESSAGE + 'salute'):
            await message.channel.send('Saudações seu porra')
        if message.content.startswith(PRE_MESSAGE + 'corona'):
            cases = self.get_corona_details()
            await message.channel.send('Então, o mundo ta uma merda, estamos com {} casos globais, com {} mortes e {} pessoas curadas.\nSendo no Brasil {} casos, com {} mortes e {} pessoas curadas.'.format(
                cases[0]['cases'], cases[0]['deaths'], cases[0]['recovered'], cases[1]['cases'], cases[1]['deaths'], cases[1]['recovered'], 
            ))

        elif message.content.startswith(PRE_MESSAGE + 'roll'):
            import random

            cheat = self.read_cheat()["cheat"]

            try:
                number = message.content.split(' ')
                if 'd' in message.content:
                    numbers = number[1].split('d')
                    roll_list = [random.randint(1, int(numbers[1])) for number in range(int(numbers[0]))]
                    numbers_sum = sum(roll_list)
                    roll_list = [str(i) for i in roll_list]
                    numbers = ' + '.join(roll_list)
                    await message.channel.send(str(numbers) + ' = ' + str(numbers_sum))
                elif cheat:
                    if 0 < cheat <= int(number[1]):
                        await message.channel.send(self.generate_roll_message(cheat))
                    else:
                        await message.channel.send(self.generate_roll_message(number[1]))
                    self.set_cheat(False)
                else:
                    random = random.randint(1, int(number[1]))
                    await message.channel.send(self.generate_roll_message(random))
            except:
                await message.channel.send('Mano ta errado isso ai')
                
        elif message.content.startswith(PRE_MESSAGE + 'cuck morreu'):
            with open('mortes_cuck.txt', 'r+') as mortes_file:
                data = mortes_file.read()
                mortes_cuck = int(data) + 1
            with open('mortes_cuck.txt', 'w') as mortes_file:
                mortes_file.write(str(mortes_cuck))
            await message.channel.send('contador de mortes do cuck = ' + str(mortes_cuck))
        elif message.content.startswith(PRE_MESSAGE + 'addclass'):
            text = self.add_class(message.content)
            await message.channel.send(text)
        elif message.content.startswith(PRE_MESSAGE + 'getclass'):
            text = self.get_class(message.content)
            await message.channel.send(text)
        elif message.content.startswith(PRE_MESSAGE + 'allclass'):
            text = self.get_all_classes()
            await message.channel.send(text)
        elif message.content.startswith(PRE_MESSAGE + 'delclass'):
            text = self.delete_class(message.content)
            await message.channel.send(text)
        elif message.content.startswith(PRE_MESSAGE + 'addnpc'):
            text = self.add_npc(message.content)
            await message.channel.send(text)
        elif message.content.startswith(PRE_MESSAGE + 'getnpc'):
            text = self.get_npc(message.content)
            await message.channel.send(text)
        elif message.content.startswith(PRE_MESSAGE + 'allnpc'):
            text = self.get_all_npc()
            await message.channel.send(text)
        elif message.content.startswith(PRE_MESSAGE + 'ajudagalileu'):
            if str(message.author) == 'Seytheir#7880':
                try:
                    number = message.content.split(' ')
                    self.set_cheat(int(number[1]))
                    await message.channel.send(":sunglasses: :ok_hand: :point_right: {} :point_left: :ok_hand: :sunglasses:".format(number[1]))
                except:
                    self.set_cheat(20)
                    await message.channel.send("Mano, sei que porra é essa não, vou deixar como 20 mesmo")
            else:
                await message.channel.send("Ado ado ado quem usa cheat é viado")

        elif message.content.startswith(PRE_MESSAGE + 'help'):
            await message.channel.send('Uma lista de comandos foi enviada pelo privado')
            await message.author.send(HELP)

    @staticmethod
    def add_class(message):
        try:
            arguments = message.split('|')
            class_name = arguments[1]
            armor_type = arguments[2]
            weapon_type = arguments[3]
            initial_equip = arguments[4]
            perks = arguments[5]
            db = ClassManager('classes.sqlite')
            db.add_class(class_name, armor_type, weapon_type, initial_equip, perks)
            return class_name + ' adicionada com sucesso'
        except:
            return 'Erro ao adicionar classe'

    @staticmethod
    def get_class(message):
        db = ClassManager('classes.sqlite')
        get_class = db.get_class(message.split(' ')[1])
        if get_class is None:
            return 'Classe não achada'
        get_class = get_class.to_dict()
        text = '{}\n\nTipo de Armadura: {}\nTipo de Arma: {}\nEquipamento Inicial: {}\nPerks: {}'.format(
            get_class['class_name'], get_class['armor_type'], get_class['weapon_type'], get_class['initial_equip']
            , get_class['perks'])
        return text

    @staticmethod
    def get_all_classes():
        db = ClassManager('classes.sqlite')
        all_class = db.get_all_classes()
        cyberclasses = [i.class_name for i in all_class]
        return ', '.join(cyberclasses)

    @staticmethod
    def delete_class(message):
        try:
            db = ClassManager('classes.sqlite')
            del_class = message.split(' ')[1]
            db.delete_class(del_class)
            return 'Classe removida com sucesso'
        except:
            return 'Erro ao remover classe'

    @staticmethod
    def add_npc(message):
        try:
            arguments = message.split('|')
            name = arguments[1]
            age = arguments[2]
            alias = arguments[3]
            country = arguments[4]
            position = arguments[5]
            specialization = arguments[6]
            docs_link = arguments[7]
            db = NpcManager('npcs.sqlite')
            db.add_npc(name, age, alias, country, position, specialization, docs_link)
            return name + ' adicionado(a) com sucesso'
        except:
            return 'Erro ao adicionar npc'

    @staticmethod
    def get_npc(message):
        db = NpcManager('npcs.sqlite')
        get_npc = db.get_npc(message.split('|')[1])
        if get_npc is None:
            return 'Npc não encontrado'
        get_npc = get_npc.to_dict()
        text = '{}\n\nIdade: {} anos\nAlias: {}\nNacionalidade: {}\nEspecialização: {}\nDetalhes: {}'.format(get_npc['name'],
                get_npc['age'], get_npc['alias'], get_npc['country'], get_npc['specialization'], get_npc['docs_link'])
        return text

    @staticmethod
    def get_all_npc():
        db = NpcManager('npcs.sqlite')
        get_npc = db.get_all_npc()
        npcs = [i.name for i in get_npc]
        return ', '.join(npcs)

    @staticmethod
    def get_corona_details():
        responseAll = requests.get('https://coronavirus-19-api.herokuapp.com/all')
        responseBrazil = requests.get('https://coronavirus-19-api.herokuapp.com/countries/Brazil')
        total = responseAll.json()
        brazil = responseBrazil.json()
        cases = [total, brazil]
        return cases

    @staticmethod
    def invert_boolean(bool):
        return not bool

    @staticmethod
    def set_cheat(cheat):
        data_file = open("data.json", "r")
        data = json.load(data_file)
        data_file.close()
        data["cheat"] = cheat
        data_file = open("data.json", "w")
        json.dump(data, data_file)
        data_file.close()
        return data["cheat"]

    @staticmethod
    def read_cheat():
        data_file = open("data.json", "r")
        data = json.load(data_file)
        data_file.close()
        return data
    
    @staticmethod
    def generate_roll_message(random_number):
        random_number = str(random_number)
        if random_number == '20':
            return random_number + ' :ok_hand:'
        elif random_number == '1':
            return random_number + ' :middle_finger:'
        else:
            return random_number

client = MyClient()
client.run(process.env.DISCORD_KEY)



