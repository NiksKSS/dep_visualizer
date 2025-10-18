#!/bin/bash

echo "Тест 1: Пустое имя пакета"
python3 src/main.py --package-name "" --repo ./repo --repo-mode local --version 1.0.0
echo

echo "Тест 2: Пустой путь к репозиторию"
python3 src/main.py --package-name testpkg --repo "" --repo-mode local --version 1.0.0
echo

echo "Тест 3: Несуществующий путь"
python3 src/main.py --package-name testpkg --repo ./no_such_dir --repo-mode local --version 1.0.0
echo

echo "Тест 4: Путь не является директорией"
echo "test" > repo_file
python3 src/main.py --package-name testpkg --repo ./repo_file --repo-mode local --version 1.0.0
rm repo_file
echo

echo "Тест 5: Некорректный git URL"
python3 src/main.py --package-name testpkg --repo myrepo --repo-mode git --version 1.0.0
echo

echo "Тест 6: Пустая версия"
python3 src/main.py --package-name testpkg --repo ./repo --repo-mode local --version ""
echo

echo "Тест 7: Некорректный формат версии"
python3 src/main.py --package-name testpkg --repo ./repo --repo-mode local --version "v1.x"
echo

echo "Тест 8: Некорректное значение ascii-tree"
python3 src/main.py --package-name testpkg --repo ./repo --repo-mode local --version 1.0.0 --ascii-tree maybe
echo

echo "Тест 9: Пустой фильтр"
python3 src/main.py --package-name testpkg --repo ./repo --repo-mode local --version 1.0.0 --ascii-tree True --filter " "
echo

echo "Тест 10: Корректные данные"
python3 src/main.py --package-name testpkg --repo ./repo --repo-mode local --version 1.0.0 --ascii-tree True --filter core
echo
