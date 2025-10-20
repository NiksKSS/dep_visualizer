# Этап 1 — Минимальный CLI-прототип

## Назначение
CLI-приложение принимает параметры командной строки, проверяет их корректность и выводит значения или ошибки.

Проверяются параметры:
- Имя пакета (`--package-name`)
- Репозиторий (`--repo`)
- Режим (`--repo-mode`)
- Версия (`--version`)
- Формат вывода (`--ascii-tree`)
- Фильтр (`--filter`)

---

## Тесты

**Тест 1. Пустое имя пакета**
```bash
python src/main.py --package-name "" --repo ./repo --repo-mode local --version 1.0.0
````

Проверка: вывод ошибки о пустом имени пакета.

---

**Тест 2. Пустой путь к репозиторию**

```bash
python src/main.py --package-name testpkg --repo "" --repo-mode local --version 1.0.0
```

Проверка: вывод ошибки о пустом пути.

---

**Тест 3. Несуществующий путь**

```bash
python src/main.py --package-name testpkg --repo ./no_such_dir --repo-mode local --version 1.0.0
```

Проверка: сообщение о том, что путь не найден.

---

**Тест 4. Путь не является директорией**

```bash
echo "test" > repo_file.txt
python src/main.py --package-name testpkg --repo ./repo_file.txt --repo-mode local --version 1.0.0
del repo_file.txt
```

Проверка: сообщение, что путь не является директорией.

---

**Тест 5. Некорректный git URL**

```bash
python src/main.py --package-name testpkg --repo "invalid_git_url" --repo-mode git --version 1.0.0
```

Проверка: сообщение, что URL должен быть http/https или .git.

---

**Тест 6. Пустая версия**

```bash
python src/main.py --package-name testpkg --repo ./repo --repo-mode local --version ""
```

Проверка: сообщение, что версия не может быть пустой.

---

**Тест 7. Некорректный формат версии**

```bash
python src/main.py --package-name testpkg --repo ./repo --repo-mode local --version "1.a.0"
```

Проверка: сообщение, что версия должна содержать только цифры и точки.

---

**Тест 8. Некорректное значение ascii-tree**

```bash
python src/main.py --package-name testpkg --repo ./repo --repo-mode local --version 1.0.0 --ascii-tree maybe
```

Проверка: сообщение, что значение должно быть True или False.

---

**Тест 9. Пустой фильтр**

```bash
python src/main.py --package-name testpkg --repo ./repo --repo-mode local --version 1.0.0 --ascii-tree True --filter ""
```

Проверка: фильтр пустой, должно вывестись "(не задан)".

---

**Тест 10. Корректные данные**

```bash
python src/main.py --package-name testpkg --repo ./repo --repo-mode local --version 1.0.0 --ascii-tree True --filter core
```

Проверка: успешный запуск и вывод всех параметров без ошибок.


---

# Этап 2 — Сравнение зависимостей

## Назначение

На этом этапе приложение сравнивает зависимости из двух файлов `pyproject.toml`
и выводит различия: какие зависимости были добавлены, удалены или изменены.

Проверяются параметры:

* Имя пакета (`--package-name`)
* Репозиторий (`--repo`)
* Режим (`--repo-mode`)
* Версия (`--version`)
* Формат вывода (`--ascii-tree`)
* Фильтр (`--filter`)
* Первый файл (`--file1`)
* Второй файл (`--file2`)

Перед запуском проверяется наличие всех обязательных параметров и существование указанных путей.

---

## Тесты

**Тест 1. Отсутствует обязательный параметр**

```bash
python src/main.py --repo ./repo --repo-mode local --version 1.0.0 --file1 ./repo/pyproject_1.toml --file2 ./repo/pyproject_2.toml
```

Проверка: сообщение об ошибке, что не указано имя пакета.

---

**Тест 2. Несуществующий путь к файлу**

```bash
python src/main.py --package-name testpkg --repo ./repo --repo-mode local --version 1.0.0 --file1 ./repo/no_file.toml --file2 ./repo/pyproject_2.toml
```

Проверка: сообщение об ошибке, что файл не найден.

---

**Тест 3. Пустой фильтр**

```bash
python src/main.py --package-name testpkg --repo ./repo --repo-mode local --version 1.0.0 --ascii-tree False --filter "" --file1 ./repo/pyproject_1.toml --file2 ./repo/pyproject_2.toml
```

Проверка: фильтр не задан, программа выводит "(не задан)".

---

**Тест 4. Сравнение двух версий с различиями**

```bash
python src/main.py \
  --package-name testpkg \
  --repo ./repo \
  --repo-mode local \
  --version 1.0.0 \
  --ascii-tree False \
  --filter core \
  --file1 ./repo/pyproject_1.toml \
  --file2 ./repo/pyproject_2.toml
```

Проверка: успешный запуск и вывод результатов сравнения зависимостей.

Пример вывода:

```
Настройки приложения:
Имя пакета: testpkg
Репозиторий: /Users/veronikadenisenko/PycharmProjects/dep_visualizer/repo
Режим: local
Версия: 1.0.0
ASCII-дерево: False
Фильтр: core

Результаты сравнения зависимостей:
Добавлены: ['matplotlib']
Удалены: ['numpy']
Изменены: ['requests']
```

---

**Тест 5. Одинаковые файлы**

```bash
python src/main.py \
  --package-name testpkg \
  --repo ./repo \
  --repo-mode local \
  --version 1.0.0 \
  --ascii-tree False \
  --filter core \
  --file1 ./repo/pyproject_1.toml \
  --file2 ./repo/pyproject_1.toml
```

Проверка: вывод, что различий в зависимостях нет.

---
