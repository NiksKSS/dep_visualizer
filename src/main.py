import argparse
import os
import sys
import ast
import subprocess
import tempfile
import shutil

def error(message):
    print(f"\nОшибка: {message}")
    sys.exit(1)

def parse_setup_py(path):
#Извлекаем install_requires из setup.py через ast
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "setup":
            deps = []
            for keyword in node.keywords:
                if keyword.arg == "install_requires":
                    for elt in keyword.value.elts:
                        deps.append(getattr(elt, "value", getattr(elt, "s", None)))
                    return deps
    return []

def get_dependencies(repo_path):
#Получаем прямые зависимости пакета из setup.py
    setup_py = os.path.join(repo_path, "setup.py")
    if not os.path.exists(setup_py):
        error("Не найден setup.py в репозитории.")
    deps = parse_setup_py(setup_py)
    return deps

def clone_repo(url):
#Клонируем git репозиторий во временную папку
    tmp_dir = tempfile.mkdtemp()
    try:
        subprocess.run(["git", "clone", url, tmp_dir], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return tmp_dir
    except subprocess.CalledProcessError:
        error(f"Не удалось клонировать репозиторий {url}")

def main():
    parser = argparse.ArgumentParser()

    # Определяем параметры CLI
    parser.add_argument("--package-name", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--repo", required=True, help="URL или путь к репозиторию")
    parser.add_argument("--repo-mode", choices=["git", "local"], required=True, help="Режим работы: git или local")
    parser.add_argument("--version", required=True, help="Версия пакета")
    parser.add_argument("--ascii-tree", type=str, default="False", help="Вывод в формате ASCII-дерева (True/False)")
    parser.add_argument("--filter", default="", help="Подстрока для фильтрации пакетов")

    args = parser.parse_args()

    # Проверки параметров
    if not args.package_name.strip():
        error("Параметр --package-name не может быть пустым.")
    if not args.repo.strip():
        error("Путь к репозиторию не может быть пустым.")
    if args.repo_mode == "local":
        if not os.path.exists(args.repo):
            error(f"Путь '{args.repo}' не найден.")
        if not os.path.isdir(args.repo):
            error(f"Путь '{args.repo}' не является директорией.")
    else:  # git
        if not (args.repo.startswith("http://") or args.repo.startswith("https://") or args.repo.endswith(".git")):
            error("Для режима git нужен корректный URL (http/https или .git).")

    if not args.version.strip():
        error("Параметр --version не может быть пустым.")
    if not args.version.replace('.', '').isdigit():
        error("Параметр --version должен содержать только цифры и точки (например, 1.0.0).")
    if args.ascii_tree.lower() not in ["true", "false"]:
        error("Параметр --ascii-tree должен быть True/False.")
    args.ascii_tree = args.ascii_tree.lower() == "true"

    # Обработка фильтра
    args.filter = args.filter.strip()
    if not args.filter:
        args.filter = ""

    # Вывод параметров
    print("Настройки приложения:")
    print(f"Имя пакета: {args.package_name}")
    print(f"Репозиторий: {args.repo}")
    print(f"Режим: {args.repo_mode}")
    print(f"Версия: {args.version}")
    print(f"ASCII-дерево: {args.ascii_tree}")
    print(f"Фильтр: {args.filter or '(не задан)'}\n")

    # Получение зависимостей
    tmp_repo = None
    if args.repo_mode == "git":
        tmp_repo = clone_repo(args.repo)
        repo_path = tmp_repo
    else:
        repo_path = args.repo

    print("Прямые зависимости пакета:")
    deps = get_dependencies(repo_path)
    if args.filter:
        deps = [d for d in deps if args.filter in d]

    if not deps:
        print("(зависимости не найдены)")
    else:
        for d in deps:
            print(f"- {d}")

    # Удаляем временный репозиторий после работы
    if tmp_repo:
        shutil.rmtree(tmp_repo)

if __name__ == "__main__":
    main()
