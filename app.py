#только хардкор го на одном из следующих релизов уберу коменты)
# └ │ ┘  ┌ ─ ┐  ├ ┤  → 

import json, random, os
import items as item_storage #можно импортировать свои базы предметов, импортировать несколько нельзя, но если вы кодите лучше чем я то прикрутите сами
multicommand = False

def error(text=""): 
    global w,h,multicommand
    if multicommand: tr="├"
    else: tr = "└"
    input(f"   {tr}─ {text}")
def resolution(): 
    global w,h
    w,h = os.get_terminal_size()
    aw, ah = 60,30
    if w < aw or h < ah:print("\n"*h); input(f"Разрешение вашего терминала не подходит! \nИгра будет корректно работать при разрешении {aw}x{ah} или выше\nПопробуйте изменить размер окна, или уменьшить шрифт\nВаше разрешение: {w}x{h}\n\nНажмите ENTER что-бы продолжить")
    return w,h
def i(text=""): return input(text)

# Конфигурация
class Settings():
    def __init__(self):
        self.dices = [1,2,3,4,5,6]      #разрешенные кубы лучше оставить как есть
        self.dice_icons = ["[1]","[2]","[3]","[4]","[5]","[6]"] #["⚀","⚁","⚂","⚃","⚄","⚅"]                    #иконки кубов
        self.new_dice_cost = 2  #сколько маны стоит новый куб через команду G
        self.auto_use = False   #использовать предмет без подтверждения
        self.game = {           #основные значения
            'hp':10,
            'max-hp':10,
            'mana': 7,
            'coin': 0,
        }                       



class UserData():
    def __init__(self):
        self.data = {
            'max_dices': 2,     #кубов в начале хода
            'hp':c.game['hp'],
            'mana':c.game['mana'],
            'coin':c.game['coin'],
            }
        self.choosed = {
            'dice': [],
            'dice-ids': [],
            'item': [],
        }
        self.dices = []
        self.items = item_storage.list
        self.item_error = False
        self.items_used = []
        self.effects = []

    def selecting(self,obj,id):
        if obj == "d":
            try: id = int(id)
            except ValueError: self.choosed['dice'] = [];self.choosed['dice-ids'] = []; return
            try:
             if id < 1: self.dices[99999999]
             if id not in self.choosed['dice-ids']:
              self.choosed['dice'].append(self.dices[id-1])
              self.choosed['dice-ids'].append(id)
             else: error("вы уже выбраи этот куб")
            except IndexError or ValueError: error("вы выбраи куб которого несуществует")
        if obj == "dr":
            try: id = int(id)
            except ValueError: self.choosed['dice'] = [];self.choosed['dice-ids'] = []; return
            try:
             if id < 1: self.dices[99999999]
             self.choosed['dice'].remove(self.choosed['dice'][id-1])
             self.choosed['dice-ids'].remove(self.choosed['dice-ids'][id-1])
            except IndexError or ValueError: error("вы выбраи куб которого несуществует")

    def show_choosed(self):
        ischs = ""
        res = ""
        if self.choosed['dice'] != []: 
            ischs = "│  Выбранно │"; 
            dc = ""
            for i in range(0,len(self.choosed['dice'])):
                dc +=f"{self.choosed['dice'][i][1]} "
            res=f"{dc} "
            res = f"{ischs+res}"
            if res == "":...
            else: print(res)

    def show_items(self, info=False):
     if info == False:
        res = ""
        i = 1
        for item in self.items:

            descr = item['description']
            if item in self.items_used: descr = "ПРЕДМЕТ НЕДОСТУПЕН"
            res += f"├ {item['name']} ({descr})\n"
            i+=1
        print(res[:-1])
     else:
        if info == "": res = "\nВаши предметы: \n"
        else: res="\n"
        i = 1
        for item in self.items:
          if info=="" or i == int(info): 
            res += f"{i}. {item['name']} ({item['description']})\n"
            try: 
                if item['info']!= "":  res += f"   Информация: {item['info']}\n"
            except: pass
            res += f"   Мана: {item['mana']}\n   Требуется: {item['requied']['text']}\n"
            if item['multiple'] == False: 
                if item in self.items_used: res+="   ПРЕДМЕТ УЖЕ ИСПОЛЬЗОВАН И НЕДОСТУПЕН В ЭТОМ ХОДУ!\n"
                else:
                
                 res+=f"   Вы можете использовать предмет один раз за ход\n"
            else: 
                 res+=f"   Вы можете использовать предмет несколько раз за ход\n"
            res+="\n"
          i+=1
        if res == "\n": error("у вас нет карты с таким номером"); return
        input(res[:-2])
         
            

    def use_item(self, item_id):
        item_id = int(item_id)-1
        dices = ""
        
        for d in self.choosed['dice']:
            dices += f"{d[0]},"
        dices = dices[:-1]
        i = self.items[item_id]
        if i in self.items_used: error("пердмет недоступен"); return
        if len(self.choosed['dice']) != len(i['requied']['dices']): 
            error(f"у вас выбрано неверное количество кубов. нужно: {len(i['requied']['dices'])}") ; return

        if self.data['mana']-i['mana'] < 0: return error("недостаточно маны")
        
        if c.auto_use != True:
            usragr = input(f'''Вы действительно хотите использовать "{i['name']}"? (y/n) ''')
            if usragr == "" or usragr.startswith("y"): pass
            else: error("отменено"); return
        exec(f"item_storage.{i['payload']}("+"{'user': u, 'config':c}"+f",{dices})")
        if self.item_error: return

        self.data['mana']-=i['mana']
        if i['multiple'] == False: self.items_used.append(i)
        self.choosed['dice-ids'] = []
        for d in self.choosed['dice']:
            self.dices.remove(d)
        self.choosed['dice'] = [] 

            



    def dice(self, act="get"):
        if act=="get":
            if u.data['mana'] < c.new_dice_cost: error("недостаточно маны")
            else:
                u.data['mana'] -= c.new_dice_cost
                if self.effects == []:
                    d = random.randint(0,len(cfg.dices)-1)
                    r = [cfg.dices[d],cfg.dice_icons[d]]
                    self.dices.append(r)
                return r

        if act=="end":
            r = []
            self.items_used = []
            self.choosed['dice'] = []; self.choosed['dice-ids'] =[]
            self.data['mana'] = c.game['mana']
            for i in range(0,self.data['max_dices']):
                if self.effects == []:
                    d = random.randint(0,len(cfg.dices)-1)
                    r.append([cfg.dices[d],cfg.dice_icons[d]])
                    self.dices = r
            return r
        
        if "spec_id:" in act:
            d = int(act.replace("spec_id:", ""))
            r = [cfg.dices[d],cfg.dice_icons[d]]
            self.dices.append(r)



        if act=="show":
            res = ""
            for i in range(0,len(self.dices)):
                res+= self.dices[i][1]+" "
            return res
            




c = cfg = Settings()
u = user = UserData()
resolution()
u.dice(act='end')
while 1:
# └ │ ┘  ┌ ─ ┐  ├ ┤  →  ┬  ┴     ├──────────
    
    if resolution() == "error": continue    
    print("\n"*h)
    print(f"┌─── Ваши предметы "+"─"*(w-19))
    u.show_items()
    print(f"├───────────┬── Кубы "+"─"*(w-21))
    u.show_choosed()
    print(f"│       Все │"+u.dice(act="show"))
    print(f"├───────────┼── Статистика "+"─"*(w-27))
    print(f"│        HP │ {u.data['hp']}/{c.game['max-hp']}")
    print(f"│      Мана │ {u.data['mana']}")
    print(f"│    Монеты │ {u.data['coin']}")
    print(f"├───────────┴── Ввод команды "+"─"*(w-29))
    cms=i(f"└─ ").replace("; ", ";")
    if ";" in cms: multicommand=True
    else: multicommand=False
    for cmd in cms.split(";"):
        
        
        if cmd=="": continue
        if cmd=="get" or cmd[0]=="g": u.dice(act="get")
        if cmd=="end" or cmd[0]=="e":u.dice(act='end')
        if cmd.startswith("dice-remove") or cmd.startswith("dr"): u.selecting('dr', cmd.replace("dice-remove", "dr").replace("dr","").replace(" ",""))
        elif cmd.startswith("dice") or cmd[0]=="d": u.selecting('d', cmd.replace("dice", "d").replace("d","").replace(" ",""))
        if cmd.startswith("i"): u.show_items(info=cmd[1:])
        if cmd.startswith("u") and cmd!="u": u.use_item(cmd[1:])











