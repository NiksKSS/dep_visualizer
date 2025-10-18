import argparse
import os
import sys

def error(message):
    print(f"\nОшибка: {message}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()

    # Определяем параметры
    parser.add_argument("--package-name", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--repo", required=True, help="URL или путь к репозиторию")
    parser.add_argument("--repo-mode", choices=["git", "local"], required=True, help="Режим работы: git или local")
    parser.add_argument("--version", required=True, help="Версия пакета")
    parser.add_argument("--ascii-tree", type=str, required=False, default="False", help="Вывод в формате ASCII-дерева (True/False)")
    parser.add_argument("--filter", default="", help="Подстрока для фильтрации пакетов")

    args = parser.parse_args()

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

if __name__ == "__main__":
    main()
