from tkinter import *
from tkinter.ttk import *
from CategoryDao import CategoryDao
from TodoDao import TodoDao


class Design:
    def __init__(self):
        self.ctdao = CategoryDao()
        self.tddao = TodoDao()
        self.tk = Tk()

        self.tk.title('Todo List by JR')
        self.tk.geometry('720x400')
        self.tk.minsize(720, 400)

        for c in range(20):
            self.tk.rowconfigure(c, weight=1)
        for c in range(12):
            self.tk.columnconfigure(c, weight=1)

        self.category_frame = Frame(self.tk, borderwidth=5, relief=GROOVE).grid(row=0, column=0, columnspan=3,
                                                                                rowspan=20,
                                                                                sticky=W + E + N + S)
        self.todo_frame = Frame(self.tk).grid(row=0, column=3, columnspan=9, rowspan=20, sticky=W + E + N + S)

        Label(self.category_frame, text='Categories').grid(row=0, column=0, columnspan=3)
        Button(self.category_frame, text='Add').grid(row=1, column=0, columnspan=1)
        Button(self.category_frame, text='Update').grid(row=1, column=1, columnspan=1)
        Button(self.category_frame, text='Delete').grid(row=1, column=2, columnspan=1)

        Label(self.todo_frame, text="Todo's").grid(row=0, column=3, columnspan=9)
        Button(self.todo_frame, text='Add').grid(row=1, column=3, columnspan=1)
        Button(self.todo_frame, text='Update').grid(row=1, column=4, columnspan=1)
        Button(self.todo_frame, text='Complete').grid(row=1, column=5, columnspan=1)

        Label(self.todo_frame, text='Sort by:').grid(row=1, column=6, columnspan=1)
        self.sort_by_value = StringVar()
        cmb = Combobox(self.todo_frame, textvariable=self.sort_by_value, values=self.tddao.sort_by_keys,
                       state='readonly', width=10)
        cmb.current(0)
        cmb.grid(row=1, column=7, columnspan=1)

        Label(self.todo_frame, text='Filter:').grid(row=1, column=8, columnspan=1)
        self.find_by_value = StringVar()
        cmb2 = Combobox(self.todo_frame, textvariable=self.find_by_value, values=self.tddao.find_by_keys,
                        state='readonly', width=10)
        cmb2.current(0)
        cmb2.grid(row=1, column=9, columnspan=1)

        self.category_list = Listbox(self.category_frame, selectmode=SINGLE)

        for index, category in enumerate(self.ctdao.get_categories()):
            self.category_list.insert(index, category)
        self.category_list.grid(row=2, column=0, rowspan=18, columnspan=3, sticky=W + E + N + S)

        self.todo_list = Listbox(self.todo_frame, selectmode=SINGLE)
        self.todo_list.grid(row=2, column=3, rowspan=18, columnspan=9, sticky=W + E + N + S)

        Entry(self.todo_frame, width=10).grid(row=1, column=10, columnspan=1)

        self.tk.mainloop()
