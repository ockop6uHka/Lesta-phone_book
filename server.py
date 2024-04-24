import socket
from typing import Tuple
import json
import os
import threading

PHONE_BOOK_FILE = "phone_book.json"


def load_phone_book():
    if os.path.exists(PHONE_BOOK_FILE) and os.path.getsize(PHONE_BOOK_FILE) > 0:
        with open(PHONE_BOOK_FILE, "r") as file:
            return json.load(file)
    else:
        # with open(PHONE_BOOK_FILE, "w") :
        #     pass
        return {}


def save_phone_book(phone_book: dict):
    with open(PHONE_BOOK_FILE, "w") as file:
        json.dump(phone_book, file)


def get_last_id(file_name: str): #Для сохранения логики нумерации записей между перезапусками
    if os.path.exists(PHONE_BOOK_FILE) and os.path.getsize(PHONE_BOOK_FILE) > 0:
        with open(file_name, "r") as file:
            data = json.load(file)

        last_id = max(data.keys(), default=0)

        if last_id is not None:
            last_id = int(last_id)

        return last_id
    else:
        return 0


phone_book = load_phone_book()


def handle_request(request: str):
    global phone_book
    print(request)
    parts = request.split("^")
    print(parts)
    command = parts[0]
    phone_book = load_phone_book()
    if command == "ADD":
        print(parts)
        name, surname, phone, note = parts[1:]

        last_id = get_last_id(PHONE_BOOK_FILE)
        last_id += 1
        entry_id = last_id

        #Получаем и записываем(сохраняем) данные из запроса
        phone_book[entry_id] = {"name": name, "surname": surname, "phone": phone, "note": note}
        save_phone_book(phone_book)
        return f"Запись добавлена с ID: {entry_id}"

    elif command == "REMOVE":
        entry_id = parts[1]
        if entry_id in phone_book:
            del phone_book[entry_id]
            save_phone_book(phone_book)
            return f"Запись с ID {entry_id} удалена "
        else:
            return f"Запись с ID {entry_id} не найдена"

    elif command == "SEARCH":
        query = "^".join(parts[1:])
        print(query)
        results = [] #Проверка на входящую подстроку из запроса и соответствующий вывод данных
        for entry_id, details in phone_book.items():
            if (query.lower() in details['name'].lower() or query.lower() in details['surname'].lower()
            or query.lower() in details['phone'].lower() or query.lower() in details['note'].lower()):
                results.append((entry_id, details))
        if results:
            return "\n".join([f"ID: {entry_id}, Данные: {details}" for entry_id, details in results])
        else:
            return "Ничего не найдено"

    elif command == "VIEW":
        entry_id = parts[1]
        if entry_id in phone_book:
            details = phone_book[entry_id]
            return f"ID {entry_id}, Данные: {details}"
        else:
            return f"Запись с ID {entry_id} не найдена"
    else:
        return "Неверная команда"


def handle_client(conn: socket.socket, addr: Tuple[str, int]):
    print(f"Подклюение клиента {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        request = data.decode('utf-8')
        response = handle_request(request)
        conn.sendall(response.encode())
    conn.close()


def start_server():
    host = '127.0.0.1'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host,port))
        s.listen()

        print(f"Сервер запущен на порту {port}...")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


if __name__ == "__main__":
    start_server()