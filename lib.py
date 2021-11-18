from functools import partial
from tkinter import filedialog
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
import ujson as json


class SaveFile:
    def __init__(self):
        self.file_location: str = filedialog.askopenfilename(filetypes=[("Memory file", "*.memory")])
        with open(self.file_location, encoding='utf-8') as f:
            self.data: dict = json.load(f)


class IngOption:
    def __init__(self, save: SaveFile):
        self.save = save
        self.ingredients = self.save.data['storagePartial']['ingredients']
        self.construct()

    def add_item(self, _):
        iid = pin['item_id']
        count = pin['item_count']
        if count is None or iid is None:
            toast(f'食材数量或者ID未填写', position='center', color='#FF0000')
            return
        if count < 1:
            toast(f'食材数量必须大于一', position='center', color='#FF0000')
            return
        if not iid.isnumeric():
            toast(f'{iid} 不是一个合法的食材ID', position='center', color='#FF0000')
            return
        if iid in self.ingredients:
            toast(f'该食材已经存在，请直接修改数量', position='center', color='#FF0000')
            return
        self.ingredients[iid] = count
        self.construct()

    def construct(self):
        with use_scope('options', clear=True):
            ingredients_table = [['ID', '图标', '名称', '数量']] + \
                                [[i, put_image(open(f'./Sprite/Ingredient_{i}.png', 'rb').read()), 'PlaceHolder',
                                  put_input(f'ing_{i}', value=j)] for i, j in self.ingredients.items()]
            put_table(ingredients_table)
            put_text("添加食材:")
            put_row([
                put_input('item_id', placeholder='食材ID', type=TEXT),None,
                put_input('item_count', placeholder='食材数量', type=NUMBER)
            ])

            put_buttons(['确认添加'], onclick=partial(self.add_item))

    def saves(self):
        for i, j in self.ingredients.items():
            self.ingredients[i] = pin[f'ing_{i}']
        self.save.data['storagePartial']['ingredients'] = self.ingredients
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
