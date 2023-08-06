#!/usr/bin/env python3
import os
from platform import system

class DistroRelease(object):
    def __init__(self):
        super().__init__()
        self.KERNEL_TYPE = system()
        if os.path.isfile('/etc/os-release') == True:
            self.release_file = '/etc/os-release'
        elif os.path.isfile('/usr/lib/os-release') == True:
            self.release_file = '/usr/lib/os-release'
        elif os.path.isfile('/usr/local/etc/os-release') == True:
            self.release_file = '/usr/local/etc/os-release'
        else:
            self.release_file = None
        self.__release_info = {}

    def set_distro_info(self):
        info = {}
        if self.KERNEL_TYPE == 'Windows':
            info.update({'BASE_DISTRO': 'windows'})
        elif self.KERNEL_TYPE == 'Linux':
            try:
                with open(self.release_file, 'rt') as f:
                    lines = f.readlines()
            except Exception as err:
                print(__class__.__name__, err)
                return

            for LINE in lines:
                LINE = LINE.replace('\n', '')
                if LINE[0:12] == 'PRETTY_NAME=':
                    LINE = LINE.replace('PRETTY_NAME=', '')
                    info.update({'PRETTY_NAME': LINE})

                elif LINE[0:5] == 'NAME=':
                    LINE = LINE.replace('NAME=', '')
                    info.update({'NAME': LINE})

                elif LINE[0:11] == 'VERSION_ID=':
                    LINE = LINE.replace('VERSION_ID=', '')
                    info.update({'VERSION_ID': LINE})

                elif LINE[0:8] == 'VERSION=':
                    LINE = LINE.replace('VERSION=', '')
                    info.update({'VERSION': LINE})

                elif LINE[0:17] == 'VERSION_CODENAME=':
                    LINE = LINE.replace('VERSION_CODENAME=', '')
                    info.update({'VERSION_CODENAME': LINE})

                elif LINE[0:3] == 'ID=':
                    LINE = LINE.replace('ID=', '')
                    info.update({'ID': LINE})

            if os.path.isfile('/etc/debian_version') == True:
                info.update({'BASE_DISTRO': 'debian'})
            elif os.path.isfile('/etc/fedora-release') == True:
                info.update({'BASE_DISTRO': 'fedora'})
            elif os.path.isfile('/etc/arch-release') == True:
                info.update({'BASE_DISTRO': 'archlinux'})
            else:
                info.update({'BASE_DISTRO': None})

        self.__release_info = info

    def show_info(self):
        '''
        Mostra todas as informações do sitema contidas no arquivo /etc/os-release.
        '''
        self.set_distro_info()
        for key in self.__release_info:
            print(key, '=>', self.__release_info[key])

    def get_distro_info(self) -> dict:
        self.set_distro_info()
        return self.__release_info

    def get_release_info(self, type_info: str) -> str:
        '''
        Recebe uma string com a informação que se deseja obter sobre o sistema, retorna
           a infomação em forma de string.
        EX get_release_info('ID') -> debian, fedora, ubuntu, linuxmint...
           get_release_info('VERSION_CODENAME') -> buster, focal, tricia...
           use o metodo show_all para ver todas as informações disponiveis.
        ou o metódo get_distro info para obter um dicionário com todas as informações
        disponíveis sobre o sistema.
        '''
        self.set_distro_info()
        try:
            return str(self.__release_info[type_info])
        except:
            print(__class__.__name__, '=> A informação solicitada sobre o sistema não existe.')
            return None
