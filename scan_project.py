#!/usr/bin/env python3
"""
Скрипт для сканирования проекта и сохранения структуры с кодом в Markdown формате
"""

import os
import sys
from pathlib import Path
from typing import List, Set, Optional
from datetime import datetime


# Расширения файлов кода, которые нужно сканировать
CODE_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h',
    '.hpp', '.cs', '.rb', '.php', '.go', '.rs', '.kt', '.swift', '.html',
    '.css', '.scss', '.sass', '.less', '.sql', '.sh', '.bash', '.md',
    '.env', '.yaml', '.yml', '.json', '.toml', '.ini', '.cfg', '.conf'
}

# Файлы и папки, которые нужно игнорировать
IGNORE_PATTERNS = {
    '__pycache__', '.git', '.idea', '.vscode', 'venv', 'env', 
    'node_modules', '.DS_Store', '.pytest_cache', '.mypy_cache',
    'dist', 'build', 'target', '.egg-info', '.tox'
}

# Маппинг расширений для подсветки синтаксиса в Markdown
LANGUAGE_MAPPING = {
    '.py': 'python',
    '.js': 'javascript',
    '.jsx': 'jsx',
    '.ts': 'typescript',
    '.tsx': 'tsx',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.h': 'c',
    '.hpp': 'cpp',
    '.cs': 'csharp',
    '.rb': 'ruby',
    '.php': 'php',
    '.go': 'go',
    '.rs': 'rust',
    '.kt': 'kotlin',
    '.swift': 'swift',
    '.html': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.sass': 'sass',
    '.less': 'less',
    '.sql': 'sql',
    '.sh': 'bash',
    '.bash': 'bash',
    '.md': 'markdown',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.json': 'json',
    '.toml': 'toml',
    '.ini': 'ini',
    '.cfg': 'ini',
    '.conf': 'ini',
    '.txt': 'text',
    '.env': 'env',
    '.dockerfile': 'dockerfile'
}


class MarkdownBuilder:
    """Класс для построения Markdown документа"""
    
    def __init__(self):
        self.lines: List[str] = []
    
    def add_header(self, text: str, level: int = 1) -> None:
        """Добавить заголовок"""
        self.lines.append(f"{'#' * level} {text}\n")
    
    def add_paragraph(self, text: str) -> None:
        """Добавить параграф"""
        self.lines.append(f"{text}\n")
    
    def add_horizontal_rule(self) -> None:
        """Добавить горизонтальную линию"""
        self.lines.append("---\n")
    
    def add_code_block(self, code: str, language: str = "") -> None:
        """Добавить блок кода"""
        self.lines.append(f"```{language}")
        self.lines.append(code)
        self.lines.append("```\n")
    
    def add_unordered_list_item(self, text: str, indent: int = 0) -> None:
        """Добавить элемент списка"""
        prefix = "  " * indent + "- "
        self.lines.append(f"{prefix}{text}")
    
    def add_bold(self, text: str) -> str:
        """Добавить жирный текст"""
        return f"**{text}**"
    
    def add_italic(self, text: str) -> str:
        """Добавить курсив"""
        return f"*{text}*"
    
    def add_link(self, text: str, url: str) -> str:
        """Добавить ссылку"""
        return f"[{text}]({url})"
    
    def get_content(self) -> str:
        """Получить итоговый контент"""
        return "\n".join(self.lines)


def should_ignore(path: Path, base_path: Path) -> bool:
    """Проверяет, нужно ли игнорировать путь"""
    # Проверяем по имени
    if path.name in IGNORE_PATTERNS:
        return True
    
    # Особая обработка для .env:
    # - файл .env НЕ игнорируем (для анализа структуры)
    # - директорию .env игнорируем
    if path.name == '.env':
        if path.is_dir():
            return True  # Игнорируем директорию .env
        else:
            return False  # НЕ игнорируем файл .env
    
    # Проверяем скрытые файлы и папки (кроме некоторых)
    if path.name.startswith('.') and path.name not in ['.gitignore', '.env', '.env.example']:
        return True
    
    # Проверяем относительный путь
    try:
        rel_path = path.relative_to(base_path)
        parts = rel_path.parts
        if any(part in IGNORE_PATTERNS for part in parts):
            return True
    except ValueError:
        return True
    
    return False


def get_file_size_kb(file_path: Path) -> float:
    """Возвращает размер файла в килобайтах"""
    try:
        return file_path.stat().st_size / 1024
    except Exception:
        return 0


def get_language_for_file(file_path: Path) -> str:
    """Определяет язык для подсветки синтаксиса по расширению файла"""
    # Специальная обработка для файла .env (без расширения)
    if file_path.name == '.env' and not file_path.suffix:
        return 'env'
    
    ext = file_path.suffix.lower()
    return LANGUAGE_MAPPING.get(ext, "")


def build_tree_structure(path: Path, base_path: Path, indent: int = 0) -> List[str]:
    """
    Рекурсивно строит структуру директории для Markdown
    
    Возвращает список строк для добавления в список
    """
    result = []
    
    # Определяем префикс для текущего уровня
    prefix = "  " * indent
    
    if path.is_file():
        size_kb = get_file_size_kb(path)
        file_name = path.name
        
        # Особая обработка для .env файла - скрываем чувствительные данные
        if file_name == '.env':
            result.append(f"{prefix}- `{file_name}` ({size_kb:.1f} KB) 📝")
        else:
            result.append(f"{prefix}- `{file_name}` ({size_kb:.1f} KB)")
    else:
        dir_name = path.name if path != base_path else path.name + "/"
        result.append(f"{prefix}- **{dir_name}/**")
    
    # Если это директория, обрабатываем её содержимое
    if path.is_dir():
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            items = [item for item in items if not should_ignore(item, base_path)]
            
            for item in items:
                result.extend(build_tree_structure(item, base_path, indent + 1))
        except PermissionError:
            result.append(f"{prefix}  - [Permission Denied]")
    
    return result


def read_file_content(file_path: Path) -> Optional[str]:
    """Читает содержимое файла с обработкой ошибок"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Если это .env файл, заменяем значения на [REDACTED] для безопасности
            if file_path.name == '.env':
                lines = content.split('\n')
                processed_lines = []
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        processed_lines.append(line)
                    elif '=' in line:
                        key, _ = line.split('=', 1)
                        processed_lines.append(f"{key}=[REDACTED]")
                    else:
                        processed_lines.append(line)
                content = '\n'.join(processed_lines)
            
            return content
    except UnicodeDecodeError:
        return f"[Бинарный файл или ошибка кодировки: {file_path.name}]"
    except Exception as e:
        return f"[Ошибка чтения файла: {e}]"


def scan_project_to_markdown(project_path: str = ".", output_file: Optional[str] = None) -> str:
    """
    Сканирует проект и возвращает содержимое в формате Markdown
    
    Args:
        project_path: Путь к проекту
        output_file: Путь к выходному файлу (если None, возвращает строку)
    
    Returns:
        Содержимое в формате Markdown
    """
    base_path = Path(project_path).resolve()
    
    if not base_path.exists():
        raise FileNotFoundError(f"Директория не существует: {base_path}")
    
    if not base_path.is_dir():
        raise NotADirectoryError(f"Указанный путь не является директорией: {base_path}")
    
    # Создаем строитель Markdown
    md = MarkdownBuilder()
    
    # Заголовок документа
    project_name = base_path.name
    md.add_header(f"Структура проекта: {project_name}", level=1)
    md.add_paragraph(f"*Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    md.add_paragraph(f"*Путь: `{base_path}`*")
    md.add_horizontal_rule()
    
    # Раздел: Структура проекта
    md.add_header("Структура проекта", level=2)
    md.add_paragraph("Дерево файлов и директорий проекта:")
    md.add_paragraph("")
    
    # Строим структуру дерева
    tree_lines = build_tree_structure(base_path, base_path)
    for line in tree_lines:
        md.lines.append(line)
    
    md.add_paragraph("")
    md.add_horizontal_rule()
    
    # Собираем все файлы кода
    code_files: List[Path] = []
    
    for root, dirs, files in os.walk(base_path):
        # Фильтруем директории для игнорирования
        dirs[:] = [d for d in dirs if not should_ignore(Path(root) / d, base_path)]
        
        for file in files:
            file_path = Path(root) / file
            # Проверяем по расширению ИЛИ по имени файла (.env без расширения)
            if (file_path.suffix in CODE_EXTENSIONS or file_path.name in ['.env', '.env.example']) \
               and not should_ignore(file_path, base_path):
                code_files.append(file_path)
    
    # Раздел: Файлы кода
    md.add_header("Файлы кода", level=2)
    md.add_paragraph(f"Найдено файлов кода: **{len(code_files)}**")
    md.add_paragraph("")
    
    if not code_files:
        md.add_paragraph("*Файлы кода не найдены.*")
    else:
        # Выводим содержимое каждого файла кода
        for i, file_path in enumerate(sorted(code_files, key=lambda x: str(x.relative_to(base_path))), 1):
            rel_path = file_path.relative_to(base_path)
            file_name = file_path.name
            size_kb = get_file_size_kb(file_path)
            language = get_language_for_file(file_path)
            
            md.add_header(f"{i}. `{rel_path}`", level=3)
            md.add_paragraph(f"**Размер:** {size_kb:.1f} KB")
            if language:
                md.add_paragraph(f"**Язык:** `{language}`")
            
            # Предупреждение для .env файлов
            if file_name == '.env':
                md.add_paragraph("⚠️ **Внимание:** Значения переменных окружения скрыты для безопасности.")
            
            md.add_paragraph("")
            
            # Читаем и добавляем код
            content = read_file_content(file_path)
            md.add_code_block(content, language)
            md.add_paragraph("")
    
    md.add_horizontal_rule()
    md.add_paragraph(f"*Всего файлов кода: {len(code_files)}*")
    
    # Получаем итоговый контент
    content = md.get_content()
    
    # Сохраняем в файл, если указан путь
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Отчет сохранен в: {output_path.absolute()}")
        print(f"📊 Найдено файлов кода: {len(code_files)}")
    
    return content


def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Сканирование проекта и сохранение структуры с кодом в Markdown формате"
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Путь к проекту (по умолчанию: текущая директория)"
    )
    parser.add_argument(
        "-o", "--output",
        default="project_structure.md",
        help="Путь к выходному файлу (по умолчанию: project_structure.md)"
    )
    parser.add_argument(
        "-p", "--print",
        action="store_true",
        help="Также вывести результат в консоль"
    )
    parser.add_argument(
        "--no-redact",
        action="store_true",
        help="Не скрывать значения в .env файлах (ОСТОРОЖНО!)"
    )
    
    args = parser.parse_args()
    
    try:
        content = scan_project_to_markdown(args.project_path, args.output)
        
        if args.print:
            print("\n" + "="*80)
            print(content)
            print("="*80)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()