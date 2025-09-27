# main.py
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich import box
from rich.table import Table
import time
from encrypt import caesar_encrypt
from decrypt import caesar_decrypt_known
from auto_decrypt import caesar_auto_decrypt

console = Console()

def show_menu():
    title = Text("CAESAR CIPHER TOOL", style="bold cyan", justify="center")
    console.print(Panel(title, style="bold blue", expand=False))

    options = [
        "[1] 🔒 Encrypt text",
        "[2] 🔓 Decrypt with known shift",
        "[3] 🤖 Auto-decrypt (brute-force + dictionary)",
        "[4] ❌ Exit"
    ]
    for opt in options:
        console.print(opt, style="bold white")

def main():
    while True:
        console.clear()
        show_menu()
        choice = Prompt.ask("\n[bold yellow]Select option (1-4)[/bold yellow]", choices=["1", "2", "3", "4"])

        if choice == "1":
            text = Prompt.ask("[bold green]Enter plaintext[/bold green]")
            try:
                shift = IntPrompt.ask("[bold green]Enter shift[/bold green]")
            except Exception:
                console.print("[bold red]Invalid shift![/bold red]")
                time.sleep(1)
                continue
            ciphertext, lang = caesar_encrypt(text, shift)
            result = f"Language: {lang}\nShift: {shift}\nResult: [bold yellow]{ciphertext}[/bold yellow]"
            console.print(Panel(result, title="✅ ENCRYPTED", border_style="green"))

        elif choice == "2":
            text = Prompt.ask("[bold green]Enter ciphertext[/bold green]")
            try:
                shift = IntPrompt.ask("[bold green]Enter shift[/bold green]")
            except Exception:
                console.print("[bold red]Invalid shift![/bold red]")
                time.sleep(1)
                continue
            plaintext = caesar_decrypt_known(text, shift)
            result = f"Shift: {shift}\nResult: [bold yellow]{plaintext}[/bold yellow]"
            console.print(Panel(result, title="✅ DECRYPTED", border_style="green"))

        elif choice == "3":
            text = Prompt.ask("[bold green]Enter ciphertext[/bold green]")
            with console.status("[bold cyan]Brute-forcing all shifts...[/bold cyan]", spinner="dots"):
                time.sleep(0.5)  # имитация работы
                results = caesar_auto_decrypt(text)

            best_score, best_text, best_lang, best_shift = results[0]
            if best_score > 0:
                content = (
                    f"Language: {best_lang}\n"
                    f"Shift: {best_shift}\n"
                    f"Plaintext: [bold yellow]{best_text}[/bold yellow]"
                )
                console.print(Panel(content, title="✅ AUTO-DECRYPT SUCCESS", border_style="green"))
            else:
                table = Table(title="🤔 Top Candidates (no known words)", box=box.SIMPLE)
                table.add_column("Lang", style="cyan")
                table.add_column("Shift", style="magenta")
                table.add_column("Plaintext", style="yellow")
                for score, txt, lang, sh in results:
                    table.add_row(lang, str(sh), txt)
                console.print(table)

        elif choice == "4":
            console.print("[bold blue]Goodbye![/bold blue]")
            break

        console.input("\n[bold dim]Press Enter to continue...[/bold dim]")

if __name__ == "__main__":
    main()