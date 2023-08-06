#!/usr/bin/env python3
import os.path
import platform
import sys
from setuptools import setup

if float(platform.python_version()[0:3]) < 3.6:
	print('ERRO necessário ter python3.6 ou superior instalado.')
	sys.exit(1)

_script = os.path.relpath(__file__)
dir_of_executable = os.path.dirname(_script)

DESCRIPTION = 'Módulos para obter e gerenciar configurações básicas do usuário nos sistemas Linux e Windows'

setup(
	name='user_utils',
	version='0.1.0',
	description=DESCRIPTION,
	author='Bruno Chaves',
	author_email='brunodasill@gmail.com',
	license='MIT',
	packages=['user_utils'],
	zip_safe=False,
	url='https://github.com/Brunopvh/python-user-utils',
	project_urls = {
		'Código fonte': 'https://github.com/Brunopvh/python-user-utils',
		'Download': 'https://github.com/Brunopvh/python-user-tils/archive/refs/heads/master.zip'
	},
)


