import tkinter as tk
from client import send_request
from tkinter import messagebox


def add_entry():
    add_window = tk.Toplevel(root)
    add_window.title("Добавить запись")

    #Создание элементов формы для добавления записи
    lbl_name = tk.Label(add_window, text="Имя:")
    lbl_name.grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(add_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    lbl_surname = tk.Label(add_window, text="Фамилия:")
    lbl_surname.grid(row=1, column=0, padx=10, pady=5)
    entry_surname = tk.Entry(add_window)
    entry_surname.grid(row=1, column=1, padx=10, pady=5)

    lbl_phone = tk.Label(add_window, text="Телефон:")
    lbl_phone.grid(row=2, column=0, padx=10, pady=5)
    entry_phone = tk.Entry(add_window)
    entry_phone.grid(row=2, column=1, padx=10, pady=5)

    lbl_note = tk.Label(add_window, text="Заметка:")
    lbl_note.grid(row=3, column=0, padx=10, pady=5)
    entry_note = tk.Entry(add_window)
    entry_note.grid(row=3, column=1, padx=10, pady=5)

    btn_submit = tk.Button(add_window, text="Добавить",
                                       command=lambda: submit_entry(entry_name.get(),
                                                       entry_surname.get(),
                                                       entry_phone.get(),
                                                       entry_note.get(), add_window))

    btn_submit.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


def submit_entry(name: str, surname: str, phone: str, note: str, window: tk.Toplevel):
    if not name or not surname or not phone or not note:
        tk.messagebox.showerror("Ошибка ввода", "Необходимо заполнить все поля")
        return

    request = f"ADD^{name}^{surname}^{phone}^{note}"

    response = send_request(request)
    tk.messagebox.showinfo("Результат", response)
    window.destroy()


def remove_entry():
    remove_window = tk.Toplevel(root)
    remove_window.title("Удалить запись")

    lbl_id = tk.Label(remove_window, text="ID записи:")
    lbl_id.grid(row=0, column=0, padx=10, pady=5)
    entry_id = tk.Entry(remove_window)
    entry_id.grid(row=0, column=1, padx=10, pady=5)

    btn_submit = tk.Button(remove_window, text="Удалить", command=lambda: submit_remove(entry_id.get(), remove_window))
    btn_submit.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


def submit_remove(entry_id: str, window: tk.Toplevel):
    try:
        entry_id = int(entry_id)
    except ValueError:
        tk.messagebox.showerror("Ошибка", "Введите корректный ID записи")
        return

    request = f"REMOVE^{entry_id}"
    response = send_request(request)
    tk.messagebox.showinfo("Результат", response)
    window.destroy()


def search_entry():
    search_window = tk.Toplevel(root)
    search_window.title("Поиск записи")

    lbl_query = tk.Label(search_window, text="Поиск:")
    lbl_query.grid(row=0, column=0, padx=10, pady=5)
    entry_query = tk.Entry(search_window)
    entry_query.grid(row=0, column=1, padx=10, pady=5)

    btn_submit = tk.Button(search_window, text="Найти", command=lambda: submit_search(entry_query.get(), search_window))
    btn_submit.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


def submit_search(query: str, window: tk.Toplevel):

    request = f"SEARCH^{query}"
    response = send_request(request)
    tk.messagebox.showinfo("Результат поиска", response)

    window.destroy()


def view_entry():
    view_window = tk.Toplevel(root)
    view_window.title("Просмотр записи")

    lbl_id = tk.Label(view_window, text="ID записи:")
    lbl_id.grid(row=0, column=0, padx=10, pady=5)
    entry_id = tk.Entry(view_window)
    entry_id.grid(row=0, column=1, padx=10, pady=5)

    btn_submit = tk.Button(view_window, text="Просмотреть", command=lambda: submit_view(entry_id.get(), view_window))
    btn_submit.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


def submit_view(entry_id: str, window: tk.Toplevel):
    try:
        entry_id = int(entry_id)
    except ValueError:
        tk.messagebox.showerror("Ошибка", "Введите корректный ID записи")
        return

    # Формирование запроса на просмотр записи
    request = f"VIEW^{entry_id}"
    # Отправка запроса на сервер
    response = send_request(request)
    # Отображение информации о записи
    tk.messagebox.showinfo("Просмотр записи", response)
    # Закрытие окна просмотра
    window.destroy()


root = tk.Tk()     #Главное окно
root.title("Телефонная книга")

#Кнопки
btn_add = tk.Button(root, text= "Добавить", command=add_entry, width =30, height=2)
btn_add.pack()

btn_remove = tk.Button(root, text="Удалить", command=remove_entry, width=30, height=2)
btn_remove.pack()

btn_search = tk.Button(root, text="Поиск", command=search_entry, width=30, height=2)
btn_search.pack()

btn_view = tk.Button(root, text="Просмотр", command=view_entry, width=30, height=2)
btn_view.pack()

root.mainloop()  #Запуск главного цикла
