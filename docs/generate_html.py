import os
from pathlib import Path
from datetime import datetime


def generate_html(root_dir: str, output_file: "index.html", title: str = "Архив файлов (PDF/PNG)"):
    """
    Рекурсивно обходит root_dir, находит все PDF и PNG и создаёт HTML-навигацию.
    """
    root = Path(root_dir).resolve()
    if not root.exists():
        print(f"Ошибка: папка {root} не существует")
        return

    # Расширения для поиска
    extensions = ('.pdf', '.png')

    # Собираем все файлы с нужными расширениями (регистр не важен)
    all_files = []
    for ext in extensions:
        all_files.extend(root.rglob(f"*{ext}"))
        all_files.extend(root.rglob(f"*{ext.upper()}"))
        all_files.extend(root.rglob(f"*{ext.capitalize()}"))

    all_files = list(set(all_files))  # убираем дубликаты

    if not all_files:
        print("Не найдено ни одного PDF или PNG файла")
        return

    # Группируем файлы по папкам относительно root
    files_by_folder = {}
    for file_path in all_files:
        rel_path = file_path.relative_to(root)
        folder = rel_path.parent
        if folder not in files_by_folder:
            files_by_folder[folder] = []
        files_by_folder[folder].append(file_path.name)

    for folder in files_by_folder:
        files_by_folder[folder].sort()

    # Генерация HTML
    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .folder {{
            background: white;
            margin: 20px 0;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .folder h2 {{
            color: #2980b9;
            margin-top: 0;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .folder h2:hover {{
            color: #1abc9c;
        }}
        .file-list {{
            margin-left: 25px;
            display: block;
        }}
        .file-list a {{
            display: inline-block;
            margin: 5px 15px 5px 0;
            padding: 5px 10px;
            background: #ecf0f1;
            border-radius: 4px;
            text-decoration: none;
            color: #2c3e50;
            font-size: 14px;
            transition: 0.2s;
        }}
        .file-list a:hover {{
            background: #3498db;
            color: white;
        }}
        .toggle-icon {{
            font-size: 18px;
            font-weight: bold;
        }}
        footer {{
            margin-top: 40px;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }}
    </style>
    <script>
        function toggleFolder(id) {{
            var list = document.getElementById('list-' + id);
            var icon = document.getElementById('icon-' + id);
            if (list.style.display === 'none') {{
                list.style.display = 'block';
                icon.textContent = '▼';
            }} else {{
                list.style.display = 'none';
                icon.textContent = '▶';
            }}
        }}
    </script>
</head>
<body>
<div class="container">
    <h1>📄 {title}</h1>
    <p>Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Найдено файлов: {len(all_files)} (PDF/PNG)</p>
"""

    # Добавляем блоки для каждой папки
    for idx, (folder, files) in enumerate(sorted(files_by_folder.items())):
        folder_name = str(folder) if str(folder) != '.' else 'Корневая папка'
        display_name = folder_name.replace('\\', ' / ')
        pdf_count = sum(1 for f in files if f.lower().endswith('.pdf'))
        png_count = sum(1 for f in files if f.lower().endswith('.png'))
        count_str = f" (PDF: {pdf_count}, PNG: {png_count})"

        html_content += f"""
    <div class="folder">
        <h2 onclick="toggleFolder({idx})">
            <span class="toggle-icon" id="icon-{idx}">▼</span>
            📁 {display_name}{count_str}
        </h2>
        <div class="file-list" id="list-{idx}">
"""
        for fname in files:
            icon = "📄" if fname.lower().endswith('.pdf') else "🖼️"
            file_path = f"{folder}/{fname}" if str(folder) != '.' else fname
            file_path = file_path.replace('\\', '/')
            html_content += f'            <a href="{file_path}" target="_blank">{icon} {fname}</a>\n'
        html_content += """        </div>
    </div>
"""

    html_content += """
    <footer>
        Сгенерировано автоматически. Для обновления списка запустите скрипт заново.
    </footer>
</div>
</body>
</html>
"""

    output_path = root / output_file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML-страница создана: {output_path}")
    print(
        f"   Найдено файлов: {len(all_files)} (PDF: {sum(1 for p in all_files if p.suffix.lower() == '.pdf')}, PNG: {sum(1 for p in all_files if p.suffix.lower() == '.png')})")
    print(f"   Откройте {output_path} в браузере")


if __name__ == "__main__":
    # Укажите путь к корневой папке
    ROOT_DIR = r"C:\Users\Elizaveta\YandexDisk\profiles_database"

    generate_html(ROOT_DIR, output_file="index.html", title="Архив профилей (PDF/PNG)")