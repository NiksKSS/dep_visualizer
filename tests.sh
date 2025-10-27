#!/bin/bash

echo " Тест 1: локальный пакет с зависимостями "
python3 src/main.py --package-name testpkg --repo ./repo --repo-mode local --version 1.0.0
echo

echo " Тест 2: локальный пакет без зависимостей "
python3 src/main.py --package-name empty --repo ./repo_empty --repo-mode local --version 1.0.0
echo

echo " Тест 3: пакет с зависимостями через git URL "
python3 src/main.py --package-name testpkg --repo https://github.com/NiksKSS/testpkg_git.git --repo-mode git --version 1.0.0
echo
