import threading
import time
import random
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        wait_time = random.randint(3, 10)
        time.sleep(wait_time)
        print(f"{self.name} покинул(а) стол")


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            free_table = self.get_free_table()
            if free_table:
                free_table.guest = guest
                guest.start()
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def get_free_table(self):
        for table in self.tables:
            if table.guest is None:
                return table
        return None

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None:
                    if not table.guest.is_alive():
                        print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                        print(f"Стол номер {table.number} свободен")
                        table.guest = None  # Освобождаем стол
                    else:
                        continue


                if not self.queue.empty() and table.guest is None:
                    next_guest = self.queue.get()
                    table.guest = next_guest
                    next_guest.start()
                    print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")



if __name__ == "__main__":

    tables = [Table(number) for number in range(1, 6)]


    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya',
        'Arman', 'Vitoria', 'Nikita', 'Galina', 'Pavel',
        'Ilya', 'Alexandra'
    ]

    guests = [Guest(name) for name in guests_names]


    cafe = Cafe(*tables)


    cafe.guest_arrival(*guests)

    
    cafe.discuss_guests()