from setuptools import setup

setup(
    name='tisbutascatch',
    version='1.0',
    scripts=['main.py'],
    install_requires=[
        'enum34',
        'typer',
        'GitPython'
    ]
)
