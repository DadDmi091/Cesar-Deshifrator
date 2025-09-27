# encrypt.py

def caesar_encrypt(plaintext, shift):
    RU_WITH_YO = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    result = []
    lang = "Mixed"

    for char in plaintext:
        if '\u0400' <= char <= '\u04FF':
            alphabet = RU_WITH_YO
            n = len(alphabet)
            lc = char.lower()
            if lc in alphabet:
                idx = alphabet.index(lc)
                new_idx = (idx + shift) % n
                new_char = alphabet[new_idx]
                result.append(new_char.upper() if char.isupper() else new_char)
            else:
                result.append(char)
            lang = "Russian" if lang == "Mixed" else lang
        elif 'a' <= char.lower() <= 'z':
            base = ord('a') if char.islower() else ord('A')
            new_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(new_char)
            lang = "English" if lang == "Mixed" else lang
        else:
            result.append(char)

    return ''.join(result), lang