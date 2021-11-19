import threading
from functools import partial
from tkinter import filedialog
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
import ujson as json


class SaveFile:
    def __init__(self):
        self.op = None
        self.file_location: str = filedialog.askopenfilename(filetypes=[("Memory file", "*.memory")])
        with open(self.file_location, encoding='utf-8') as f:
            self.data: dict = json.load(f)

    def save(self):
        self.op.saves()
        for n, m in self.data['storagePartial']['ingredients'].items():
            self.data['storagePartial']['ingredients'][n] = int(m)
        with open(self.file_location, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
        toast(f'保存成功！', position='center', color='#2188ff')


class IngOption:
    def __init__(self, save: SaveFile):
        self.save = save
        self.ingredients = self.save.data['storagePartial']['ingredients']
        self.pin = [f'ing_{i}' for i in range(39)]
        self.construct()
        self.thread = threading.Thread(target=self.monitor)
        self.thread.start()

    def monitor(self):
        while True:
            changed = pin_wait_change(*self.pin)
            iid = changed['name'].removeprefix('ing_')
            count = changed['value']
            self.ingredients[iid] = int(count)

    def del_item(self, msg):
        msg = msg.replace("删除", "")
        self.ingredients.pop(msg)
        self.construct()

    def add_item(self, _):
        iid = pin['item_id']
        count = pin['item_count']
        print(f"Add item {iid}x{count}")
        if count is None or iid is None:
            toast(f'食材数量或者ID未填写', position='center', color='#FF0000')
            return
        if not iid.isnumeric():
            toast(f'{iid} 不是一个合法的食材ID', position='center', color='#FF0000')
            return
        if iid in self.ingredients:
            toast(f'该食材已经存在，请直接修改数量', position='center', color='#FF0000')
            return
        self.ingredients[iid] = int(count)
        self.construct()

    def construct(self):
        with use_scope('options', clear=True):
            ingredients_table = [['ID', '图标', '名称', '数量', '删除']] + \
                                [[i, put_image(open(f'./Sprite/Ingredient_{i}.png', 'rb').read()), 'PlaceHolder',
                                  put_input(f'ing_{i}', value=j), put_buttons([f"删除{i}"], onclick=partial(self.del_item))] for i, j in self.ingredients.items()]
            put_table(ingredients_table)
            put_text("添加食材:")
            put_row([
                put_input('item_id', placeholder='食材ID', type=TEXT), None,
                put_input('item_count', placeholder='食材数量', type=NUMBER)
            ])

            put_buttons(['确认添加'], onclick=partial(self.add_item))

    def saves(self):
        for i, j in self.ingredients.items():
            self.ingredients[i] = int(pin[f'ing_{i}'])
        self.save.data['storagePartial']['ingredients'] = self.ingredients
        return self.save


class BevOption:
    def __init__(self, save: SaveFile):
        self.save = save
        self.beverages = self.save.data['storagePartial']['beverages']
        self.pin = [f'bev_{i}' for i in range(29)]
        self.construct()
        self.thread = threading.Thread(target=self.monitor)
        self.thread.start()

    def monitor(self):
        while True:
            changed = pin_wait_change(*self.pin)
            iid = changed['name'].removeprefix('bev_')
            count = changed['value']
            self.beverages[iid] = int(count)

    def del_item(self, msg):
        msg = msg.replace("删除", "")
        self.beverages.pop(msg)
        self.construct()

    def add_item(self, _):
        iid = pin['item_id']
        count = pin['item_count']
        if count is None or iid is None:
            toast(f'酒水数量或者ID未填写', position='center', color='#FF0000')
            return
        if not iid.isnumeric():
            toast(f'{iid} 不是一个合法的酒水ID', position='center', color='#FF0000')
            return
        if iid in self.beverages:
            toast(f'该酒水已经存在，请直接修改数量', position='center', color='#FF0000')
            return
        self.beverages[iid] = int(count)
        self.pin.append(f'bev_{iid}')
        self.construct()

    def construct(self):
        with use_scope('options', clear=True):
            beverages_table = [['ID', '图标', '名称', '数量', '删除']] + \
                              [[i, put_image(open(f'./Sprite/Beverages_{i}.png', 'rb').read()), 'PlaceHolder',
                                put_input(f'bev_{i}', value=j, type=NUMBER), put_buttons([f"删除{i}"], onclick=partial(self.del_item))] for i, j in self.beverages.items()]
            put_table(beverages_table)
            put_text("添加酒水:")
            put_row([
                put_input('item_id', placeholder='酒水ID', type=TEXT), None,
                put_input('item_count', placeholder='酒水数量', type=NUMBER)
            ])

            put_buttons(['确认添加'], onclick=partial(self.add_item))

    def saves(self):
        for i, j in self.beverages.items():
            self.beverages[i] = int(pin[f'bev_{i}'])
        self.save.data['storagePartial']['beverages'] = self.beverages
        return self.save


class BasicOption:
    def __init__(self, save: SaveFile):
        self.save = save
        self.construct()

    def construct(self):
        with use_scope('options', clear=True):
            put_row([
                put_input('fund', label="金钱:", value=self.save.data['playerPartial']['fund']), None,
                put_input('level', label="等级:", value=self.save.data['playerPartial']['level']), None,
                put_input('exp', label="经验:", value=self.save.data['playerPartial']['exp'])
            ])

    def saves(self):
        self.save.data['playerPartial']['fund'] = pin['fund']
        self.save.data['playerPartial']['level'] = pin['level']
        self.save.data['playerPartial']['exp'] = pin['exp']
        return self.save

    def monitor(self):
        _ = pin_wait_change('fund', 'level', 'exp')
        self.saves()


class ButtonsOption:
    def __init__(self, save: SaveFile):
        self.save = save
        self.construct()

    def give_ing(self):
        toast("成功添加", color='#2188ff')
        for n, m in self.save.data['storagePartial']['ingredients'].items():
            self.save.data['storagePartial']['ingredients'][n] += 50

    def give_bev(self):
        toast("成功添加", color='#2188ff')
        for n, m in self.save.data['storagePartial']['beverages'].items():
            if n == '0':
                continue
            self.save.data['storagePartial']['beverages'][n] += 50

    def construct(self):
        with use_scope('options', clear=True):
            put_button("所有现有的食材给我来五十份！", onclick=self.give_ing)
            put_button("所有现有的酒水给我来五十份！", onclick=self.give_bev)

    def saves(self):
        return self.save


class RecipesOption:
    def __init__(self, save: SaveFile):
        self.save = save
