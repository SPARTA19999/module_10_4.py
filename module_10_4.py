import threading
import time
import random
from queue import Queue


# Класс Table представляет стол в кафе
class Table:
    def __init__(self, number):
        """
        Инициализация стола.

        :param number: Номер стола (int)
        """
        self.number = number  # Номер стола
        self.guest = None  # Гость за столом (изначально None)


# Класс Guest представляет гостя, который является потоком
class Guest(threading.Thread):
    def __init__(self, name):
        """
        Инициализация гостя.

        :param name: Имя гостя (str)
        """
        super().__init__()
        self.name = name  # Имя гостя

    def run(self):
        """
        Метод, который выполняется при запуске потока.
        Имитирует время приема пищи гостя (от 3 до 10 секунд).
        """
        # Случайное время приема пищи от 3 до 10 секунд
        dining_time = random.randint(3, 10)
        time.sleep(dining_time)


# Класс Cafe управляет столами и очередью гостей
class Cafe:
    def __init__(self, *tables):
        """
        Инициализация кафе.

        :param tables: Объекты класса Table
        """
        self.tables = tables  # Список столов в кафе
        self.queue = Queue()  # Очередь гостей

    def guest_arrival(self, *guests):
        """
        Метод для приема гостей в кафе.
        Размещает гостей за столами или добавляет в очередь, если свободных столов нет.

        :param guests: Неограниченное количество объектов класса Guest
        """
        for guest in guests:
            placed = False
            # Поиск свободного стола
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    guest.start()
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    placed = True
                    break
            # Если свободных столов нет, добавляем гостя в очередь
            if not placed:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        """
        Метод для обслуживания гостей.
        Проверяет столы на завершение приема пищи гостями и размещает новых гостей из очереди.
        Работает до тех пор, пока очередь не пуста или хотя бы один стол занят.
        """
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None:
                    # Проверяем, завершил ли гость прием пищи
                    if not table.guest.is_alive():
                        print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                        print(f"Стол номер {table.number} свободен")
                        table.guest = None
                        # Если в очереди есть гости, садим следующего за свободный стол
                        if not self.queue.empty():
                            next_guest = self.queue.get()
                            table.guest = next_guest
                            next_guest.start()
                            print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
            # Небольшая задержка перед следующей проверкой
            time.sleep(1)


def main():
    # Создание столов (например, 5 столов)
    tables = [Table(number) for number in range(1, 6)]

    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]

    # Создание гостей
    guests = [Guest(name) for name in guests_names]

    # Создание кафе с заданными столами
    cafe = Cafe(*tables)

    # Приём гостей
    cafe.guest_arrival(*guests)

    # Обслуживание гостей
    cafe.discuss_guests()

    print("Все гости обслужены!")


if __name__ == "__main__":
    main()
