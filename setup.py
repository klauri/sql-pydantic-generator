from setuptools import setup

setup(
    name='table-cli',
    version='0.1.0',
    py_modules=['table-cli'],
    install_requires=[
        'Click'
    ],
    entry_points={
        'console_scripts': [
            'table-cli = table-cli:generate'
        ]
    }
)