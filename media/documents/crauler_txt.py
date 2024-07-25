import os
import re
import codecs
import multiprocessing
from tqdm import tqdm

def search_file(file_path, search_text):
    try:
        if os.access(file_path, os.R_OK):
            with codecs.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
                if re.search(search_text, file_content, re.IGNORECASE):
                    return file_path
    except (UnicodeDecodeError, IOError):
        pass
    return None

def search_files(directory, search_text):
    found_files = []
    total_files = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.access(file_path, os.R_OK):
                total_files += 1
    with multiprocessing.Pool() as pool, tqdm(total=total_files, unit="files") as progress_bar:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.access(file_path, os.R_OK):
                    result = pool.apply_async(search_file, args=(file_path, search_text), callback=lambda _: progress_bar.update())
                    if result.get():
                        found_files.append(result.get())
    return found_files

# Пример использования
search_text = 'ваш_поисковый_текст'
results = search_files('/', search_text)
for file_path in results:
    print(file_path)
