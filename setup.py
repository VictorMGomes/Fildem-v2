import setuptools
import os
import sys
import shutil
from pathlib import Path

import fildem

with open('README.md', 'r') as fh:
    long_description = fh.read()


def fildemStartup():
    return input("Would you like to run fildem on startup? [Y/N]: ")

def __Main__():
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        # Skip startup prompt if running as root
        if os.geteuid() == 0:
            print("Running as root — skipping startup configuration.")
            return

        response = fildemStartup().lower()
        if response in ["y", "yes"]:
            user_home = str(Path.home())
            autostart_dir = os.path.join(user_home, ".config", "autostart")
            os.makedirs(autostart_dir, exist_ok=True)

            startup_src = "./fildemstartup"
            if os.path.isdir(startup_src):
                for file in os.listdir(startup_src):
                    full_src = os.path.join(startup_src, file)
                    full_dst = os.path.join(autostart_dir, file)
                    shutil.copy(full_src, full_dst)
                print(f"Autostart files copied to: {autostart_dir}")
            else:
                print(f"Warning: Directory '{startup_src}' does not exist.")
        elif response in ["n", "no"]:
            print("Skipping autostart configuration.")
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
            __Main__()

__Main__()

setuptools.setup(
    name='fildem',
    version=fildem.__version__,
    author='Gonzalo',
    author_email='gonzaarcr@gmail.com',
    description='Fildem Global Menu for Gnome Desktop',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gonzaarcr/Fildem',
    packages=setuptools.find_packages(),
    data_files=[
        ('share/applications', ['fildem-hud.desktop'])
    ],
    install_requires=[
        'PyGObject>=3.30.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/gonzaarcr/Fildem/issues',
        'Source': 'https://github.com/gonzaarcr/Fildem',
    },
    entry_points={
        'console_scripts': [
            'fildem = fildem.run:main',
            'fildem-hud = fildem.inithud:main'
        ]
    }
)
