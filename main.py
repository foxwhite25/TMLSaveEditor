from tkinter import Tk, filedialog

from pywebio import config

from lib import *
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *

style = ''''''


@config(css_style=style)
def main():
    root = Tk()
    root.withdraw()
    file = SaveFile()
    put_text("选择你要编辑的东西")
    put_select("module", ["基本属性", "食材", "酒水"])
    set_scope("options")
    toast(f'加载档案成功，上次保存日期为{file.data["realSaveTimeCode"]}', position='center', color='#2188ff')

    op = BasicOption(file)
    while True:
        changed = pin_wait_change('module')
        op.saves()
        toast(f'修改成功', position='center', color='#2188ff')
        if changed['value'] == '基本属性':
            op = BasicOption(file)
        elif changed['value'] == '食材':
            op = IngOption(file)
        elif changed['value'] == '酒水':
            op = BevOption(file)


if __name__ == '__main__':
    main()
