# ui.py
import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_box(x, y, width, height, title=""):
    """Рисует рамку в консоли (просто для демонстрации — без curses)"""
    # В чистом Python без curses нельзя рисовать по координатам,
    # поэтому сделаем псевдо-TUI через print
    pass  # не используется в простом режиме

def input_box(prompt, y=None):
    return input(prompt)

def show_menu():
    clear_screen()
    print("┌──────────────────────────────────────┐")
    print("│        CAESAR CIPHER TOOL            │")
    print("├──────────────────────────────────────┤")
    print("│  [1] Encrypt text                    │")
    print("│  [2] Decrypt with known shift        │")
    print("│  [3] Auto-decrypt (brute-force)      │")
    print("│  [4] Exit                            │")
    print("└──────────────────────────────────────┘")

def show_result(title, data):
    clear_screen()
    print("┌──────────────────────────────────────┐")
    print(f"│ {title:^36} │")
    print("├──────────────────────────────────────┤")
    for line in data:
        print(f"│ {line:<36} │")
    print("└──────────────────────────────────────┘")
    input("\nPress Enter to continue...")