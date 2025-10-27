from setuptools import setup

setup(
    name="testpkg",         # Имя пакета
    version="1.0.0",        # Версия пакета
    install_requires=[       # Прямые зависимости
        "requests",
        "numpy",
        "pandas"
    ]
)
