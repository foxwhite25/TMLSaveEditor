import threading
from tkinter import Tk

from lib import *
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *


def option_update(file):
    file.op = BasicOption(file)
    while True:
        changed = pin_wait_change('module')
        file.op.saves()
        if changed['value'] == '基本属性':
            file.op = BasicOption(file)
        elif changed['value'] == '食材':
            file.op = IngOption(file)
        elif changed['value'] == '酒水':
            file.op = BevOption(file)


def main():
    root = Tk()
    root.withdraw()
    file = SaveFile()
    put_text("选择你要编辑的东西")
    put_select("module", ["基本属性", "食材", "酒水"])
    set_scope("options")
    set_scope("save")
    toast(f'加载档案成功，上次保存日期为{file.data["realSaveTimeCode"]}', position='center', color='#2188ff')
    with use_scope('save'):
        put_text('保存选项:')
        put_button('保存至原路径，请确保你已经备份了存档', onclick=file.save)
    option_update(file)


if __name__ == '__main__':
    main()
