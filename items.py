list = [{
    "name": "Зелье маны",
    "description": "Конвертирует кубы в ману",
    "info": "",
    "type": "mana",
    "payload": "DTM",
    'requied': {"type": "==", "text":"2 дубликата, меньше 4" ,"dices":[[1,2,3],[1,2,3]]},
    'mana': 0,
    
    'multiple': True,


},{
    "name": "Лопата",
    "description": "Переворачивает кубик",
    "info": """Предмет "переворачивает" куб, например 5 станет 2, 6 станет 1 и так далее""",
    "type": "util",
    "payload": "RVS",
    'requied': {"type": "$","text":"Любой куб", "dices":[[]]},
    'mana': 1,
    'multiple': False,


}]


### КОНЕЦ КОНФИГА, ПРОСЬБА НЕ УДАЛЯТЬ ЭТУ СТРОЧКУ НИКОГДА! ЕСЛИ ВЫ ХОТИТЕ СОЗДАТЬ СВОЙ ПАК ПРЕДМЕТОВ ДОБАВЬТЕ ЭТУ СТРОКУ ПОСЛЕ ПЕРЕМЕННОЙ list
def error(text="", data={}): input(f"error> {text}"); data['user'].item_error = True

class DTM():
 def __init__(self,data, dice1, dice2):
  if dice1 == dice2: 
   if dice1 < 4: 
        data['user'].data['mana']+=dice1

   else: error("кубы не меньше 4", data) 
  else: error("кубы не дубликаты", data)
  



class RVS():
    def __init__(self, data, dice):
        all = data['config'].dices
        i = 0
        for d in all:
            if dice == d: data['user'].dice(f"spec_id:{(i+1)*-1}")
            i+=1
