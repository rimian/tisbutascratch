from setuptools import setup, find_packages

setup(
    name='tisbutascratch',
    version='1.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'enum34',
        'typer',
        'GitPython',
        'PyYAML'
    ]
)
