import os


# --------------------------------------------------------------------------------------------
def terminal_way(path_to_file):
    return os.popen(f"pdfinfo {path_to_file} | grep 'Pages'").read().split()[1]


# --------------------------------------------------------------------------------------------
def convert_to_unique_version(from_, to):
    cmd = f'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET ' \
          f'-dBATCH -sOutputFile={to} {from_}'
    os.system(cmd)


# --------------------------------------------------------------------------------------------
def python_way(path_to_file):

    str_to_search = '/Count'
    with open(path_to_file, 'rb') as pdf:
        while True:
            line = pdf.readline()
            if str_to_search.encode() in line:
                break
            if line == b'':
                print('Error, nothing was found')
                break

    output = line.decode().strip().split(str_to_search)[1]
    return output


# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    path = 'data/pdf'
    os.mkdir('tmp')
    for p in os.listdir(path):
        print(f'\nFilename: {p}')
        file = os.path.join(path, p)
        convert_to_unique_version(file, f'tmp/{p}')

        new_file = f'tmp/{p}'
        tw = terminal_way(new_file)
        pw = python_way(new_file)
        print(f'Terminal: {tw} Python: {pw}')
    os.system('rm -rf tmp/')
