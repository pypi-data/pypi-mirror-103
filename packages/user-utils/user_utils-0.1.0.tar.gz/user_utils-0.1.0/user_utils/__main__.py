#!/usr/bin/env python3

import os
import sys
import argparse

'''
_script = os.path.realpath(__file__)
dir_of_executable = os.path.dirname(_script)
sys.path.insert(0, dir_of_executable)
'''

from user_utils import CommandsUtils, UnpackArchive

__version__ = '0.1.0'
__author__ =  'Bruno Chaves'

def main():
    commands = CommandsUtils()
    parser = argparse.ArgumentParser()
    parser.add_argument('--copy',
                        nargs=2,
                        action='store',
                        dest='copy_files',
                        help='Copia arquivos ou diretórios. Use src dest como argumentos')
    parser.add_argument('--mkdir',
                        nargs='*',
                        action='store',
                        dest='mkdir',
                        help='Cria um ou mais diretórios'
                        )
    parser.add_argument('--rmdir',
                        nargs=1,
                        action='store',
                        dest='rmdir',
                        help='Apaga arquivos e diretórios')
    parser.add_argument('--unpack',
                        nargs=1,
                        action='store',
                        dest='file_for_extract',
                        help='Descompacta arquivos. Use --unpack <file> --dir <output_dir>')
    parser.add_argument('--dir',
                        nargs=1,
                        action='store',
                        dest='output_dir',
                        help='Destino para descompressão de um arquivo.')

    args = parser.parse_args()
    if args.copy_files:
        try:
            commands.copy(args.copy_files[0], args.copy_files[1])
        except:
            sys.exit(1)
        else:
            sys.exit(0)
    elif args.rmdir:
        try:
            commands.rmdir(args.rmdir[0])
        except:
            sys.exit(1)
        else:
            sys.exit(0)
    elif args.mkdir:
        try:
            for _dir in args.mkdir:
                commands.mkdir(_dir)
        except:
            sys.exit(1)
        else:
            sys.exit(0)
    elif args.file_for_extract:
        if args.output_dir:
            unpack = UnpackArchive(args.output_dir[0])
        else:
            unpack = UnpackArchive()

        if args.file_for_extract[0][-4:] == '.deb': # Descompactar .deb
            unpack.unpack_debian(args.file_for_extract[0])
        else:
            unpack.unpack_file(args.file_for_extract[0]) # Descompactar outras extensões de arquivos

if __name__ == '__main__':
    main()