import os
import sys
import time
import threading
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

# =============== ЗАГРУЗКА СЛОВАРЕЙ ===============
def load_dictionaries():
    en_path = 'en_words.txt'
    ru_path = 'ru_words.txt'

    en_words = set()
    ru_words = set()

    if os.path.exists(en_path):
        try:
            with open(en_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        en_words.add(word)
        except Exception:
            pass

    if os.path.exists(ru_path):
        for enc in ['utf-8', 'cp1251']:
            try:
                with open(ru_path, 'r', encoding=enc) as f:
                    for line in f:
                        word = line.strip().lower()
                        if word:
                            ru_words.add(word)
                break
            except Exception:
                continue

    return frozenset(en_words or {'hello', 'world'}), frozenset(ru_words or {'привет', 'мир'})

EN_WORDS, RU_WORDS = load_dictionaries()

# =============== АНИМАЦИЯ ЗАГРУЗКИ (Linux-стиль) ===============
class LinuxSpinner:
    def __init__(self):
        self.running = False
        self.thread = None

    def animate(self):
        phases = ['-', '\\', '|', '/']
        i = 0
        while self.running:
            sys.stdout.write(f"\r{Fore.CYAN}analyzing shifts... {phases[i % 4]}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.animate, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

# =============== ОСНОВНАЯ ЛОГИКА ===============
def caesar_decrypt(ciphertext):
    RU_WITH_YO = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    RU_NO_YO = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

    def clean_word(w):
        return w.strip(".,!?;:\"'()[]{}-—–/\\«»0123456789")

    def count_words(text, wordset):
        words = [clean_word(w).lower() for w in text.split() if clean_word(w)]
        return sum(1 for w in words if w in wordset)

    has_cyr = any('\u0400' <= c <= '\u04FF' for c in ciphertext)
    has_lat = any('a' <= c.lower() <= 'z' for c in ciphertext)

    candidates = []

    if has_cyr:
        for alph, name in [(RU_WITH_YO, "Russian (with yo)"), (RU_NO_YO, "Russian (no yo)")]:
            n = len(alph)
            for shift in range(n):
                dec = []
                for ch in ciphertext:
                    lc = ch.lower()
                    if lc in alph:
                        idx = alph.index(lc)
                        new_idx = (idx - shift) % n
                        new_ch = alph[new_idx]
                        dec.append(new_ch.upper() if ch.isupper() else new_ch)
                    else:
                        dec.append(ch)
                text = ''.join(dec)
                score = count_words(text, RU_WORDS)
                candidates.append((score, text, name, shift))

    if has_lat:
        for shift in range(26):
            dec = []
            for ch in ciphertext:
                if ch.isalpha() and 'a' <= ch.lower() <= 'z':
                    base = ord('a') if ch.islower() else ord('A')
                    new_ch = chr((ord(ch) - base - shift) % 26 + base)
                    dec.append(new_ch)
                else:
                    dec.append(ch)
            text = ''.join(dec)
            score = count_words(text, EN_WORDS)
            candidates.append((score, text, "English", shift))

    if not candidates:
        return [(0, ciphertext, "Unknown", 0)]
    
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[:3]

# =============== MAIN ===============
def main():
    print(f"{Fore.GREEN}caesar-decryptor v2.1{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'-' * 50}{Style.RESET_ALL}")
    print("Supports English and Russian (with/without 'yo')")
    print()

    try:
        ciphertext = input("Enter ciphertext: ").strip()
    except KeyboardInterrupt:
        print("\nAborted.")
        return

    if not ciphertext:
        print(f"{Fore.RED}Error: empty input{Style.RESET_ALL}")
        input("Press Enter to exit...")
        return

    # Анимация в стиле Linux
    spinner = LinuxSpinner()
    spinner.start()
    time.sleep(1)  # имитация задержки
    results = caesar_decrypt(ciphertext)
    spinner.stop()

    # Вывод результата
    print()
    print(f"{Fore.GREEN}RESULT{Style.RESET_ALL}")
    print("-" * 50)
    best_score, best_text, best_lang, best_shift = results[0]

    if best_score > 0:
        print(f"Language: {best_lang}")
        print(f"Shift:    {best_shift}")
        print(f"Plaintext: {Fore.YELLOW}{best_text}{Style.RESET_ALL}")
    else:
        print("No known words found. Top candidates:")
        for i, (score, text, lang, shift) in enumerate(results, 1):
            print(f"{i}. [{lang}, shift={shift}] -> {text}")

    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
