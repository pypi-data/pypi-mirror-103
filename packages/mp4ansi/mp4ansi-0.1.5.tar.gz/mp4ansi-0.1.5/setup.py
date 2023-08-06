#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'mp4ansi',
        version = '0.1.5',
        description = 'A simple ANSI-based terminal emulator that provides multi-processing capabilities.',
        long_description = 'A simple ANSI-based terminal emulator that provides multi-processing capabilities.',
        author = 'Emilio Reyes',
        author_email = 'soda480@gmail.com',
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/soda480/mp4ansi',
        scripts = [],
        packages = ['mp4ansi'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'mpmq',
            'colorama'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
