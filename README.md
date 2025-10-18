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


