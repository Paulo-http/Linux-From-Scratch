#!/usr/bin/env python

def get_packages(filename):    
    packages = []
    with open(filename) as file:
        for line in file:
            packages.append(line[34:-1])
    return packages

def write_script(package, template):
    try:
        directory, compression = package.split('.tar.')
    except ValueError:
        tar = False
    else:
        tar = True

    if not tar:
        return

    content = ""

    with open(template) as file1:
        content = file1.read()

    opt = get_tar_type(compression)
    formatted = content.format(opt, package, directory)
    script = get_script(directory)

    if script is not "SKIP":
        with open(script, 'a') as file2:
            file2.write(formatted)

def get_tar_type(comp):
    return {
        'gz': 'z',
        'bz2': 'j',
        'xz': 'J',
        }.get(comp, 'z')

def get_script(directory):
    chapters = {
        'binutils-2.23.1' : '04',
        'gcc-4.7.2' : '05',
        'linux-3.8.1' : '06',
        'glibc-2.17' : '07',
        'tcl-8.6.0' : '10',
        'expect5.45' : '11',
        'dejagnu-1.5' : '12',
        'check-0.9.9' : '13',
        'ncurses-5.9' : '14',
        'bash-4.2' : '15',
        'bzip2-1.0.6' : '16',
        'coreutils-8.21' : '17',
        'diffutils-3.2' : '18',
        'file-5.13' : '19',
        'findutils-4.4.2' : '20',
        'gawk-4.0.2' : '21',
        'gettext-0.18.2' : '22',
        'grep-2.14' : '23',
        'gzip-1.5' : '24',
        'm4-1.4.16' : '25',
        'make-3.82' : '26',
        'patch-2.7.1' : '27',
        'perl-5.16.2' : '28',
        'sed-4.2.2' : '29',
        'tar-1.26' : '30',
        'texinfo-5.0' : '31',
        'xz-5.0.4' : '32',
    }

    chap = chapters.get(directory, None)

    if chap is not None:
        name = chap + '-' + directory + '.sh'
    else:
        name = 'SKIP'

    return name

def main():
    packages = get_packages("md5sums")

    for package in packages:
        write_script(package, "cap5.tmp")

if __name__ == "__main__":
    main()
