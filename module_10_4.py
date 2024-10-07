from threading import Thread
from random import randint
from time import sleep
from queue import Queue

class Table:
    def __init__(self, number, guest=None):
        self.number = number #номер стола
        self.guest = guest #гость, который сидит за этим столом

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name #имя гостя.
    def run(self):
        sleep(randint(3, 10)) #происходит ожидание случайным образом

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue() #очередь (объект класса Queue)
        self.tables = list(tables) #столы в этом кафе

    def guest_arrival(self, *guests):
        for guest in guests:
            for table in self.tables:
                if table.guest is None: # если есть свободный стол, то садить гостя за стол (назначать столу guest)
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел за стол номер {table.number}')
                    break
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')
    def discuss_guests(self): # обслуживание гостей
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер{table.number} свободен')
                    table.guest = None
                    if not self.queue.empty():
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        next_guest.start()
                        print(f'{next_guest.name} вышел из очереди и сел(-а)  за стол номер {table.number}')



# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()