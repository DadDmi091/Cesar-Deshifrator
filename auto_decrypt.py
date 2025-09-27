# auto_decrypt.py
from dictionaries import load_dictionaries

# Загружаем словари один раз
EN_WORDS, RU_WORDS = load_dictionaries()

def clean_word(w):
    return w.strip(".,!?;:\"'()[]{}-—–/\\«»0123456789")

def count_words(text, wordset):
    words = [clean_word(w).lower() for w in text.split() if clean_word(w)]
    return sum(1 for w in words if w in wordset)

def caesar_auto_decrypt(ciphertext):
    RU_WITH_YO = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    RU_NO_YO = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

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
                   