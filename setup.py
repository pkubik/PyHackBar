from setuptools import setup

setup(name='pyhackbar',
      version='0.1.0',
      description='Qt desktop bar (panel) for BSPWM',
      url='https://github.com/pkubik/PyHackBar',
      author='Pawel Kubik',
      packages=[
          'pyhackbar'
      ],
      install_requires=[
          'PySide2'
      ],
      entry_points={
          'console_scripts': [
              'pyhackbar=pyhackbar.bar:main'
          ],
      }
      )
