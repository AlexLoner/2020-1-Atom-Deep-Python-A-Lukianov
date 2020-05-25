import os
import xlwt
import datetime


# --------------------------------------------------------------------------------------------
def collect_row(line):
    lst = line.split('/')
    name = lst[-1]
    if os.path.isfile(line):
        fod = 'file'
        size = round(os.stat(line).st_size / 1024, 2)
    else:
        fod = 'dir'
        cmd = f"ls -al {line} --b=K | grep 'total'"
        size = float(os.popen(cmd).read().split()[1][:-1])
    dtime = datetime.datetime.fromtimestamp(os.stat(line).st_ctime).__str__()
    depths_level = len(lst) - 1
    abs_path = line #os.path.abspath(os.path.dirname(__file__))
    return (name, fod, size, dtime, depths_level, abs_path)


# --------------------------------------------------------------------------------------------
def generate_book(data, filename=''):
    book = xlwt.Workbook(encoding='utf-8')
    cols_names = ['Название', 'Директория или файл', 'Размер [kb]', 'Дата изменения',
                  'Уровень вложенности','Полный абсолютный путь']
    sht = book.add_sheet(sheetname='table')

    for num, col in enumerate(cols_names):
        sht.write(0, num, col)
    for row, line in enumerate(data, 1):
        res = collect_row(line)
        for col, item in enumerate(res):
            sht.write(row, col, item)

    if filename:
        book.save(f'{filename}.xlsx')


# --------------------------------------------------------------------------------------------
def inner(p, lst):
    for name in os.listdir(p):
        path = os.path.join(p, name)
        if os.path.isdir(path):
            lst.append(path)
            inner(path, lst)
        elif os.path.isfile(path):
            lst.append(path)
    return lst


# --------------------------------------------------------------------------------------------
def walk(p):
    all_files = []
    inner(p, all_files)
    return all_files


# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    w = os.getcwd()
    data = walk(w)

    generate_book(data, 'test_tab')
