# dictionaries.py
import os

def load_dictionaries():
    """
    Загружает словари из файлов en_words.txt и ru_words.txt.
    Если файлы не найдены — использует мини-словари.
    """
    # Мини-словари на случай, если файлы отсутствуют
    en_words = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'i', 'it', 'you',
        'hello', 'world', 'good', 'day', 'people', 'time', 'see', 'go',
        'make', 'know', 'take', 'think', 'work', 'love', 'life', 'home',
        'friend', 'yes', 'no', 'ok', 'thanks', 'please', 'help', 'now'
    }
    
    ru_words = {
        'и', 'в', 'не', 'на', 'я', 'что', 'он', 'это', 'быть', 'как',
        'а', 'она', 'мы', 'вы', 'они', 'ты', 'привет', 'мир', 'друг',
        'всем', 'пока', 'да', 'нет', 'хорошо', 'спасибо', 'время', 'день',
        'дом', 'работа', 'любовь', 'жизнь', 'человек', 'ребята', 'всё', 'ладно'
    }

    # Попытка загрузить английский словарь
    try:
        if os.path.exists('en_words.txt'):
            with open('en_words.txt', 'r', encoding='utf-8') as f:
                en_words = {line.strip().lower() for line in f if line.strip()}
            print(f"[INFO] Loaded {len(en_words):,} English words")
    except Exception as e:
        print(f"[WARN] Failed to load en_words.txt: {e}")

    # Попытка загрузить русский словарь (с поддержкой кодировок)
    try:
        if os.path.exists('ru_words.txt'):
            loaded = False
            for encoding in ['utf-8', 'cp1251']:
                try:
                    with open('ru_words.txt', 'r', encoding=encoding) as f:
                        ru_words = {line.strip().lower() for line in f if line.strip()}
                    print(f"[INFO] Loaded {len(ru_words):,} Russian words ({encoding})")
                    loaded = True
                    break
                except UnicodeDecodeError:
                    continue
            if not loaded:
                print("[WARN] Could not decode ru_words.txt in utf-8 or cp1251")
    except Exception as e:
        print(f"[WARN] Failed to load ru_words.txt: {e}")

    return frozenset(en_words), frozenset(ru_words)