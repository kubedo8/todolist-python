from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from CategoryDao import CategoryDao
from TodoDao import TodoDao
from datetime import datetime


class Design:
    def __init__(self):
        self.ctdao = CategoryDao()
        self.tddao = TodoDao()
        self.tk = Tk()

        self.tk.title('Todo List by JR')
        self.tk.geometry('840x400')
        self.tk.minsize(840, 400)

        for c in range(20):
            self.tk.rowconfigure(c, weight=1)
        for c in range(12):
            self.tk.columnconfigure(c, weight=1)

        self.category_frame = Frame(self.tk, borderwidth=5, relief=GROOVE).grid(row=0, column=0, columnspan=3,
                                                                                rowspan=20,
                                                                                sticky=W + E + N + S)
        self.todo_frame = Frame(self.tk).grid(row=0, column=3, columnspan=9, rowspan=20, sticky=W + E + N + S)

        Label(self.category_frame, text='Categories').grid(row=0, column=0, columnspan=3)
        Button(self.category_frame, text='Add', command=lambda: self.on_add_category()).grid(row=1, column=0,
                                                                                             columnspan=1)
        Button(self.category_frame, text='Update', command=lambda: self.on_update_category()).grid(row=1, column=1,
                                                                                                   columnspan=1)
        Button(self.category_frame, text='Delete', command=lambda: self.on_delete_category()).grid(row=1, column=2,
                                                                                                   columnspan=1)

        Label(self.todo_frame, text="Todo's").grid(row=0, column=3, columnspan=6)
        Button(self.todo_frame, text='Import', command=lambda: self.on_import()).grid(row=0, column=9, columnspan=1)
        Button(self.todo_frame, text='Export', command=lambda: self.on_export()).grid(row=0, column=10, columnspan=1)
        Button(self.todo_frame, text='Add', command=lambda: self.on_add_todo()).grid(row=1, column=3, columnspan=1)
        Button(self.todo_frame, text='Update', command=lambda: self.on_update_todo()).grid(row=1, column=4,
                                                                                           columnspan=1)
        Button(self.todo_frame, text='Complete', command=lambda: self.on_complete_todo()).grid(row=1, column=5,
                                                                                               columnspan=1)

        Label(self.todo_frame, text='Sort by:').grid(row=1, column=6, columnspan=1)
        self.sort_by_value = StringVar()
        self.sort_combo = Combobox(self.todo_frame, textvariable=self.sort_by_value, values=self.tddao.sort_by_keys,
                                   state='readonly', width=10)
        self.sort_combo.current(0)
        self.sort_combo.bind('<<ComboboxSelected>>', self.on_sort_change)
        self.sort_combo.grid(row=1, column=7, columnspan=1)

        Label(self.todo_frame, text='Filter:').grid(row=1, column=8, columnspan=1)
        self.find_by_value = StringVar()
        self.filter_combo = Combobox(self.todo_frame, textvariable=self.find_by_value, values=self.tddao.find_by_keys,
                                     state='readonly', width=10)
        self.filter_combo.current(0)
        self.filter_combo.bind('<<ComboboxSelected>>', self.on_filter_attr_change)
        self.filter_combo.grid(row=1, column=9, columnspan=1)

        self.category_list = Listbox(self.category_frame, selectmode=SINGLE)
        self.category_list.bind('<<ListboxSelect>>', self.on_category_select)
        self.category_list.configure(exportselection=False)

        self.actualize_category_list()
        self.category_list.select_set(0)
        self.category_list.grid(row=2, column=0, rowspan=18, columnspan=3, sticky=W + E + N + S)

        self.filter_entry = Entry(self.todo_frame, width=10)
        self.filter_entry.bind('<KeyRelease>', self.on_filter_change)
        self.filter_entry.grid(row=1, column=10, columnspan=1)

        self.todo_list = Listbox(self.todo_frame, selectmode=SINGLE)
        self.todo_list.configure(exportselection=False)
        self.actualize_todo_list()
        self.todo_list.grid(row=2, column=3, rowspan=18, columnspan=9, sticky=W + E + N + S)

        self.tk.mainloop()

    def on_category_select(self, event):
        self.actualize_todo_list()

    def on_sort_change(self, event):
        self.tddao.set_sort(self.sort_combo.get())
        self.actualize_todo_list()

    def on_filter_attr_change(self, event):
        self.actualize_todo_list()

    def on_filter_change(self, event):
        self.actualize_todo_list()

    def actualize_category_list(self):
        self.category_list.delete(0, END)
        for index, category in enumerate(self.ctdao.get_categories()):
            self.category_list.insert(index, category)

    def actualize_todo_list(self):
        self.todo_list.delete(0, END)
        if len(self.category_list.curselection()) < 1:
            return
        if len(self.filter_entry.get()) == 0:
            self.set_todo_list(self.tddao.get_todos(self.selected_category()))
        else:
            self.set_todo_list(
                self.tddao.find_todos(self.selected_category(), self.filter_combo.get(), self.filter_entry.get()))

    def set_todo_list(self, todos):
        for index, todo in enumerate(todos):
            self.todo_list.insert(index, todo)

    def on_add_category(self):
        self.show_category_dialog(None)

    def on_update_category(self):
        if len(self.category_list.curselection()) < 1:
            messagebox.showerror('Error', 'Select category to update')
            return
        self.show_category_dialog(self.selected_category())

    def selected_category(self):
        return self.ctdao.get_categories()[self.category_list.curselection()[0]]

    def show_category_dialog(self, category):
        dialog = Toplevel(self.tk)

        Label(dialog, text='Title').grid(row=0, columnspan=2, sticky=E)
        title_entry = Entry(dialog)
        title_entry.delete(0, END)

        func = None
        if category is not None:
            title_entry.insert(END, category.title)
            func = lambda: self.update_category(dialog, category, title_entry.get())
        else:
            func = lambda: self.add_category(dialog, title_entry.get())
        title_entry.grid(row=0, column=2, columnspan=3)

        Button(dialog, text='OK', command=func).grid(row=1, columnspan=2, sticky=E)
        Button(dialog, text='Close', command=lambda: dialog.destroy()).grid(row=1, column=2, columnspan=3, sticky=E)

    def on_import(self):
        if len(self.category_list.curselection()) < 1:
            messagebox.showerror('Error', 'Select category for import')
            return
        self.show_import_export_dialog('Import')

    def on_export(self):
        if len(self.category_list.curselection()) < 1:
            messagebox.showerror('Error', 'Select category for export')
            return
        category = self.selected_category()
        if len(self.tddao.get_todos(category)) == 0:
            messagebox.showerror('Error', 'Nothing to export')
            return
        self.show_import_export_dialog('Export')

    def show_import_export_dialog(self, flag):
        dialog = Toplevel(self.tk)
        title_entry = Entry(dialog)
        title_entry.delete(0, END)
        title_entry.grid(row=0, columnspan=3, sticky=E)
        Label(dialog, text='.xml').grid(row=0, column=3, columnspan=1)

        func = None
        if flag == 'Import':
            func = lambda: self.import_todos(dialog, title_entry.get())
        else:
            func = lambda: self.export_todos(dialog, title_entry.get())

        Button(dialog, text='OK', command=func).grid(row=1, columnspan=2, sticky=E)
        Button(dialog, text='Close', command=lambda: dialog.destroy()).grid(row=1, column=2, columnspan=3, sticky=E)

    def import_todos(self, dialog, file_name):
        if len(file_name) == 0:
            messagebox.showerror('Error', 'File name can not be empty')
            return
        num = self.tddao.import_todos(self.selected_category(), file_name)
        self.actualize_todo_list()
        dialog.destroy()
        messagebox.showinfo('Import', 'Imported {} todos'.format(num))

    def export_todos(self, dialog, file_name):
        if len(file_name) == 0:
            messagebox.showerror('Error', 'File name can not be empty')
            return

        self.tddao.export_todos(self.selected_category(), file_name)
        dialog.destroy()
        messagebox.showinfo('Export', 'Successfuly exported todos')

    def update_category(self, dialog, category, new_name):
        try:
            self.ctdao.update_category(category, new_name)
            self.actualize_category_list()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def add_category(self, dialog, new_name):
        try:
            self.ctdao.add_category(new_name)
            self.actualize_category_list()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def on_delete_category(self):
        if len(self.category_list.curselection()) < 1:
            messagebox.showerror('Error', 'Select category to delete')
            return
        category = self.ctdao.get_categories()[self.category_list.curselection()[0]]
        self.ctdao.remove_category(category)
        self.actualize_category_list()

    def on_add_todo(self):
        if len(self.category_list.curselection()) < 1:
            messagebox.showerror('Error', 'Select category to add todo')
            return
        self.show_todo_dialog(None)

    def on_update_todo(self):
        if len(self.todo_list.curselection()) < 1:
            messagebox.showerror('Error', 'Select todo to update')
            return
        self.show_todo_dialog(self.selected_todo())

    def selected_todo(self):
        return self.tddao.get_todos(self.selected_category())[self.todo_list.curselection()[0]]

    def show_todo_dialog(self, todo):
        dialog = Toplevel(self.tk)

        Label(dialog, text='Title').grid(row=0, columnspan=2, sticky=E)
        title_entry = Entry(dialog)
        title_entry.delete(0, END)

        Label(dialog, text='Description').grid(row=1, columnspan=2, sticky=E)
        description_entry = Entry(dialog)
        description_entry.delete(0, END)

        Label(dialog, text='Duedate').grid(row=2, columnspan=2, sticky=E)
        duedate_entry = Entry(dialog)
        duedate_entry.delete(0, END)

        Label(dialog, text='Priority').grid(row=3, columnspan=2, sticky=E)
        priority_spinbox = Spinbox(dialog, from_=1, to=5)

        func = None
        if todo is not None:
            title_entry.insert(END, todo.title)
            description_entry.insert(END, todo.description)
            date_string = "%s.%s.%s" % (todo.duedate.day, todo.duedate.month, todo.duedate.year)
            duedate_entry.insert(END, date_string)
            priority_spinbox.delete(0, END)
            priority_spinbox.insert(0, todo.priority)

            func = lambda: self.update_todo(dialog, todo, title_entry.get(), description_entry.get(),
                                            int(priority_spinbox.get()), duedate_entry.get())
        else:
            func = lambda: self.add_todo(dialog, title_entry.get(), description_entry.get(),
                                         int(priority_spinbox.get()), duedate_entry.get())
        title_entry.grid(row=0, column=2, columnspan=3)
        description_entry.grid(row=1, column=2, columnspan=3)
        duedate_entry.grid(row=2, column=2, columnspan=3)
        priority_spinbox.grid(row=3, column=2, columnspan=3)

        Button(dialog, text='OK', command=func).grid(row=4, columnspan=2, sticky=E)
        Button(dialog, text='Close', command=lambda: dialog.destroy()).grid(row=4, column=2, columnspan=3, sticky=E)

    def add_todo(self, dialog, title, description, priority, duedate):
        try:
            duedate = datetime.strptime(duedate, '%d.%m.%Y').date()
        except ValueError:
            messagebox.showinfo('Error', "Correct format of date is d.m.yyyy")
            return
        try:
            self.tddao.add_todo(title, description, duedate, self.selected_category(), priority)
            self.actualize_todo_list()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def update_todo(self, dialog, todo, title, description, priority, duedate):
        try:
            duedate = datetime.strptime(duedate, '%d.%m.%Y').date()
        except ValueError:
            messagebox.showinfo('Error', "Correct format of date is d.m.yyyy")
            return
        try:
            self.tddao.update_todo(todo, title, description, duedate, priority)
            self.actualize_todo_list()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def on_complete_todo(self):
        if len(self.todo_list.curselection()) < 1:
            messagebox.showerror('Error', 'Select todo to complete')
            return
        self.tddao.remove_todo(self.selected_todo().id)
        self.actualize_todo_list()
