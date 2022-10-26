import sys  # системная библиотека
import requests  # для работы с HTTP запросами (получаем информацию о пакете с сайта pypi.org)
import graphviz as gv  # для работы с графами (создание графа из полученной JSON строки)


# read arguments given to program
def read_args_of_program():  # функция для чтения аргумента программы
    args = []  # создаём массив для аргументов

    for arg in sys.argv[1:]:   # читаем аргумент при вызове программы
        args.append(arg)  # добавляем его в массив
    return args  # вызвращаем массив


def get_dependencies_of_package(name_of_package) -> list:  # функция для получения списка зависимостей пакета
    url = 'https://pypi.org/pypi/{}/json'  # путь, по которому осуществляется запрос данных
    json = requests.get(url.format(name_of_package)).json()  # формируем json строку

    # осуществляем проверку на успешность получения данных в json
    try:
        requirements = json['info']['requires_dist']
    except:
        return []

    data = []  # создаём массив данных

    if requirements is not None:  # если данные есть
        for req in requirements:
            data.append(req.split(' ')[0])  # добавляем их в массив данных
    return data  # возвращаем массив данных


def recursiveNodes(graph, name, depth=0):  # рекурсивная функция для составления графа
    dependencies = get_dependencies_of_package(name)  # получаем зависимости пакета

    if (dependencies.__len__() == 0 or depth > 1):  # если зависимостей нет
        return

    for dep in dependencies:  # добавляем зависимости в граф
        graph.node(dep, dep)
        graph.edge(name, dep)
        recursiveNodes(graph, dep, depth + 1)  # повторно вызываем функцию для составления след. ряда графа


def main(args):  # основная функция
    if len(args) == 0:  # если никаких аргументов не передано в программу
        print("U need to run program with name of package!")  # выводим об этом сообщение
        return

    dot = gv.Digraph(comment='Dependencies of {}'.format(args[0]))  # запись комментария с названием пакета
    dot.node(args[0], args[0])  # создание элемента графа зависимостей пакета

    recursiveNodes(dot, args[0])  # вызов рекурсивной функции для составления графа зависимостей

    # создание файла с зависимостями пакета на языке Graphviz
    dot.render('dependencies/graphviz-file.gv', view=True)  # doctest: +SKIP


if __name__ == "__main__":
    main(read_args_of_program())