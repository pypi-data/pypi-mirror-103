from setuptools import setup

with open('Readme.md') as file:
    longDescription = file.read()

setup(name='Undo_Redo',
      version='1.1',
      description='Implementation of Undo, Redo',
      long_description=longDescription,
      url='https://github.com/abhi1p/UndoRedo',
      author='Abhishek Anand',
      author_email="abhishekanand2a@gmail.com",
      license='MIT',
      packages=['Undo_Redo'],
      install_requires=[],
      long_description_content_type='text/markdown'
      )