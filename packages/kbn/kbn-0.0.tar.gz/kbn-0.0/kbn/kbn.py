from tkinter import *
from random import randint

widty_heieght = ['430', '560']

class Ss(Frame):
    def __init__(self, root):  # конструктор
        super(Ss, self).__init__(root)
        self.startUI() # вызов функции startUI
        root.mainloop()

    def startUI(self):  # создаем нашу функцию startUI
        self.lbl = Label(root, text='Начало игры!', bg="#103d9c")
        self.lbl.place(x=150, y=25)
        btn1 = Button(root, text='Камень', command=lambda x=1: self.btn_click(x))
        btn2 = Button(root, text='Ножницы', command=lambda x=2: self.btn_click(x))
        btn3 = Button(root, text='Бумага', command=lambda x=3: self.btn_click(x))
        btn1.place(x=10, y=100, width=120, height=50)
        btn2.place(x=155, y=100, width=120, height=50)
        btn3.place(x=300, y=100, width=120, height=50)

        self.win = 0
        self.drow = 0
        self.lose = 0
        self.lbl2 = Label(root, justify='left', text=f'''Побед: {self.win} 
Проигрышей: {self.lose}
Ничей: {self.drow}''')
        self.lbl2.place(x=5, y=5)


    def btn_click(self, choise):
        comp_choise = randint(1, 3)

        if comp_choise == choise:
            self.drow += 1
            self.lbl.configure(text="Ничья")
        elif choise == 1 and comp_choise == 2 \
            or choise == 2 and comp_choise == 3 \
            or choise == 3 and comp_choise == 1:
            self.win += 1
            self.lbl.configure(text="Победа")
        else:
            self.lose += 1
            self.lbl.configure(text="Проигрыш")
        self.lbl2.configure(text=f'''Побед: {self.win}
Проигрышей: {self.lose}
Ничей: {self.drow}''')
        del comp_choise


if __name__ == '__main__':
    root = Tk()
    root.geometry(widty_heieght[0]+'x'+widty_heieght[1])
    root.title('Камень, ножницы, бумана')
    app = Ss(root)







