# decrypt.py

def caesar_decrypt_known(ciphertext, shift):
    RU_WITH_YO = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    result = []

    for char in ciphertext:
        if '\u0400' <= char <= '\u04FF':
            alphabet = RU_WITH_YO
            n = len(alphabet)
            lc = char.lower()
            if lc in alphabet:
                idx = alphabet.index(lc)
                new_idx = (idx - shift) % n
                new_char = alphabet[new_idx]
                result.append(new_char.upper() if char.isupper() else new_char)
            else:
                result.append(char)
        elif 'a' <= char.lower() <= 'z':
            base = ord('a') if char.islower() else ord('A')
            new_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(new_char)
        else:
            result.append(char)

    return ''.join(result)