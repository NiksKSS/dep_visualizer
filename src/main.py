import argparse
import os
import sys
import tomllib

def error(message):
    print(f"\nОшибка: {message}")
    sys.exit(1)

def read_pyproject(path):  # чтение toml
    if not os.path.exists(path):
        error(f"Файл {path} не найден.")
    with open(path, "rb") as f:
        return tomllib.load(f)

def parse_dependencies(project_data):  # достаем зависимости
    deps = {}
    try:
        for dep in project_data["project"]["dependencies"]:
            name, version = dep.split(">=")
            deps[name.strip()] = version.strip()
    except KeyError:
        deps = {}
    return deps

def compare_dependencies(dep1, dep2):  # сравнение
    added = [pkg for pkg in dep2 if pkg not in dep1]
    removed = [pkg for pkg in dep1 if pkg not in dep2]
    changed = [pkg for pkg in dep1 if pkg in dep2 and dep1[pkg] != dep2[pkg]]
    return added, removed, changed

def main():
    parser = argparse.ArgumentParser()

    # Определяем параметры
    parser.add_argument("--package-name", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--repo", required=True, help="URL или путь к репозиторию")
    parser.add_argument("--repo-mode", choices=["git", "local"], required=True, help="Режим работы: git или local")
    parser.add_argument("--version", required=True, help="Версия пакета")
    parser.add_argument("--ascii-tree", type=str, required=False, default="False", help="Вывод в формате ASCII-дерева (True/False)")
    parser.add_argument("--filter", default="", help="Подстрока для фильтрации пакетов")
    parser.add_argument("--file1", required=True, help="Путь к первому pyproject.toml")
    parser.add_argument("--file2", required=True, help="Путь ко второму pyproject.toml")
    args = parser.parse_args()

    # Делаем пути абсолютными, чтобы не было ошибок поиска
    args.repo = os.path.abspath(args.repo)
    args.file1 = os.path.abspath(args.file1)
    args.file2 = os.path.abspath(args.file2)

    # Проверка параметра --package-name
    if not args.package_name.strip():
        error("Параметр --package-name не может быть пустым.")

    # Проверка параметра --repo
    if not args.repo.strip():
        error("Параметр --repo не может быть пустым.")
    if args.repo_mode == "local":
        if not os.path.exists(args.repo):
            error(f"Путь '{args.repo}' не найден.")
        if not os.path.isdir(args.repo):
            error(f"Путь '{args.repo}' не является директорией.")
    elif args.repo_mode == "git":
        if not (args.repo.startswith("http://") or args.repo.startswith("https://") or args.repo.endswith(".git")):
            error("Для режима git нужен корректный URL (http/https или .git).")

    # Проверка параметра --version
    if not args.version.strip():
        error("Параметр --version не может быть пустым.")
    if not args.version.replace('.', '').isdigit():
        error("Параметр --version должен содержать только цифры и точки (например, 1.0.0).")

    # Проверка параметра --ascii-tree
    if args.ascii_tree.lower() not in ["true", "false"]:
        error("Параметр --ascii-tree должен быть логическим (True/False).")
    args.ascii_tree = args.ascii_tree.lower() == "true"

    # Проверка параметра --filter
    if args.filter is not None and args.filter.strip() == "":
        error("Параметр --filter не может быть пустым при указании.")

    # Вывод параметров
    print("Настройки приложения:")
    print(f"Имя пакета: {args.package_name}")
    print(f"Репозиторий: {args.repo}")
    print(f"Режим: {args.repo_mode}")
    print(f"Версия: {args.version}")
    print(f"ASCII-дерево: {args.ascii_tree}")
    print(f"Фильтр: {args.filter or '(не задан)'}")

    # Чтение и сравнение зависимостей
    project1 = read_pyproject(args.file1)
    project2 = read_pyproject(args.file2)
    deps1 = parse_dependencies(project1)
    deps2 = parse_dependencies(project2)
    added, removed, changed = compare_dependencies(deps1, deps2)

    print("\nРезультаты сравнения зависимостей:")
    print(f"Добавлены: {added or '—'}")
    print(f"Удалены: {removed or '—'}")
    print(f"Изменены: {changed or '—'}")

if __name__ == "__main__":
    main()
