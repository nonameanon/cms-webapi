from user import User
from reporter import Reporter
from cycles import *

'''
    Создаётся объект класса User
'''
u = User()

'''
    Создаётся объект класса Reporter
    В качестве названия файла выбрано test_cycle.html
'''
rep = Reporter(name='test_cycle')

'''
    В качестве заголовка файла выбрано 'Тестовый цикл cms-webapi'
'''
rep.title = 'Тестовый цикл cms-webapi'

'''
    Инициализировано начало записи файла
'''
rep.start()

'''
    Тут можно добавить все необходимые циклы
'''
main_cycle(u, rep)
change_data_cycle(u, rep)
change_carriers_cycle(u, rep)
changed_password = change_password_cycle(u, rep)
u.change_password(changed_password)
live_feed_cycle(u, rep)
maps_cycle(u, rep)

'''
    Reporter заканчивает запись, подводит итог тестовых циклов и сохраняет файл
'''
rep.end()
