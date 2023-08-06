#!/usr/bin/env python3

import os
import subprocess
import shutil
from user_utils import DistroRelease
from user_utils.colors import *

class UnpackArchive(DistroRelease):
    def __init__(self, output_dir=os.getcwd()):
        super().__init__()
        self.output_dir = output_dir
        self.__work_dir = os.getcwd()

        if os.path.isdir(self.output_dir) == False:
            os.makedirs(self.output_dir)

    def show_info(self, file: str):
        print(f'{CGreen}D{CReset}escompactando {os.path.basename(file)}')

    def unpack_file(self, file: str):
        self.show_info(file)
        os.chdir(self.output_dir)
        try:
            shutil.unpack_archive(file)
        except Exception as err:
            print(__class__.__name__, err)
        else:
            pass
        finally:
            os.chdir(self.__work_dir)

    def unpack_debian(self, deb_file: str) -> int:
        '''Descompactar arquivos Debian(.deb)'''
        if os.path.isfile(deb_file) == False:
            print(f'{CRed}{__class__.__name__}{CReset} O arquivo não existe')
            return False

        if self.get_release_info('BASE_DISTRO') == 'debian':
            commands = ['ar', '-x', deb_file]
        else:
            commands = ['ar', '-x', deb_file, f'--output={self.output_dir}']

        self.show_info(deb_file)
        os.chdir(self.output_dir)
        proc = subprocess.run(commands, capture_output=True, text=True)
        os.chdir(self.__work_dir)
        if proc.returncode == 0:
            return 0
        else:
            print(f'{CRed}ERRO ... {proc.stderr}{CReset}')
            return proc.returncode


class CommandsUtils(object):
    def __init__(self):
        super().__init__()

    def copy(self, src: str, dest: str) -> bool:
        '''
        Copiar arquivos e diretórios.
          Para copiar um diretório, e necessário que o destino "dest" seja um diretório
        que não exista, pois se "dest" existir mesmo sendo vazio a operação irá falhar.

           No caso de arquivos, se o arquivo passado em "dest" já existir, ele será substituído.
        '''
        print('Copiando ... {}'.format(src))
        if os.path.isdir(src) == True:
            try:
                shutil.copytree(src, dest, symlinks=True, ignore=None)
            except Exception as err:
                print(err)
                return False
        elif os.path.isfile(src) == True:
            try:
                shutil.copy(src, dest, follow_symlinks=False)
            except Exception as err:
                print(err)
                return False

        return True

    def mkdir(self, path: str) -> bool:
        try:
            os.makedirs(path)
        except Exception as err:
            if os.path.isdir(path) == False:
                print(__class__.__name__, err)
        finally:
            if os.access(path, os.W_OK) == True:
                return True
            else:
                print(__class__.__name__, 'Você não tem permissão de escrita em ... {}'.format(path))
                return False
    def rmdir(self, path: str) -> bool:
        '''Remove arquivos e diretórios'''
        if os.path.exists(path) == False:
            return True
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except Exception as err:
                print(f'{CRed}{__class__.__name__}{CReset} {err}')
                return False
        elif os.path.islink(path):
            if os.name == 'posix':
                out = subprocess.run(['rm', '-rf', path], capture_output=True, text=True)
            elif os.name == 'nt':
                out = subprocess.run(['rmdir', path], capture_output=True, text=True)
            else:
                os.unlink(path)
        else:
            try:
                os.remove(path)
            except Exception as err:
                print(f'{CRed}{__class__.__name__}{CReset} {err}')
                return False

        return True

    def dir_size(self, dir_path) -> float:
        '''
        https://qastack.com.br/programming/1392413/calculating-a-directorys-size-using-python
        :param dir_path:
        :return:
        '''
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size






