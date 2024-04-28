import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import threading
import webbrowser
from PIL import Image, ImageTk  # Aggiungi questa importazione per supportare PNG
from pathlib import Path  # Importa Path da pathlib

# Funzione per eseguire comandi shell
def run_command(command):
    try:
        subprocess.check_output(command, shell=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(e.output)
        return False

# Funzione principale per eseguire i comandi ADB
def execute_adb_commands():
    print("Arresto forzato di tutte le app...")
    try:
        packages_output = subprocess.check_output("adb shell pm list packages", shell=True, text=True)
        for line in packages_output.splitlines():
            package_name = line.split(":")[1]
            print(f"Arresto forzato di {package_name}...")
            run_command(f"adb shell am force-stop {package_name}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Errore", "Impossibile ottenere l'elenco dei pacchetti.")
        return

    print("Cancellazione della cache delle app...")
    for i in range(30):
        if not run_command("adb shell pm trim-caches 1000G"):
            messagebox.showerror("Errore", "Errore durante la cancellazione della cache delle app.")
            return
        else:
            print(f"Iterazione {i+1}/30: Cache delle app in fase di cancellazione...")

    print("Cache delle app cancellata con successo.")

    if run_command("adb shell cmd package compile -m speed -f -a"):
        print("Comando di compilazione eseguito con successo.")
    else:
        messagebox.showerror("Errore", "Errore durante l'esecuzione del comando di compilazione.")
        return

    if run_command('adb shell "cmd package bg-dexopt-job"'):
        print("Ottimizzazione in background completata con successo.")
    else:
        messagebox.showerror("Errore", "Errore durante l'ottimizzazione in background.")

    messagebox.showinfo("Successo", "Operazioni ADB completate con successo!")

# Funzione per gestire l'evento click sul pulsante di esecuzione
def on_execute_button_click():
    threading.Thread(target=execute_adb_commands).start()

# Funzione per aprire URL
def open_url(url):
    webbrowser.open_new_tab(url)

# Creazione dell'interfaccia grafica aggiornata
def create_gui():
    root = tk.Tk()
    root.title("SonicsElixir")
    root.geometry("800x800")  # Dimensioni aggiornate per ospitare i nuovi elementi

    # Ottieni il percorso della directory in cui si trova lo script
    script_path = Path(__file__).parent

    # Definisci il percorso della cartella delle risorse in modo dinamico
    resources_path = script_path / "resources/icons"

    # Carica le icone usando PIL per supportare PNG e Path per il percorso
    github_icon = ImageTk.PhotoImage(Image.open(resources_path / "github-icon.png"))
    telegram_icon = ImageTk.PhotoImage(Image.open(resources_path / "telegram-icon.png"))
    buy_me_a_coffee_icon = ImageTk.PhotoImage(Image.open(resources_path / "buy-me-a-coffee-icon.png"))
    paypal_icon = ImageTk.PhotoImage(Image.open(resources_path / "paypal-icon.png"))

    style = ttk.Style()
    style.configure('TFrame', background='#3F88C5')

    frame = ttk.Frame(root, padding="10 10 10 10")
    frame.pack(fill=tk.BOTH, expand=True)

    title = ttk.Label(frame, text="SonicsElixir", font=("Roboto", 30, "bold"), background='#032B43')
    title.pack()

    version = ttk.Label(frame, text="Versione 0.2.0", font=("Roboto", 10), background='#032B43')
    version.pack()

    description = ttk.Label(frame, text="Utility per gestire dispositivi Android tramite ADB.", font=("Roboto", 15), wraplength=600, background='#FFBA08', foreground='#032B43')
    description.pack(pady=10)

    # Imposta uno stile personalizzato per il bottone
    style = ttk.Style(root)
    style.configure('W.TButton', font=('Roboto', 12), background='#032B43', foreground='#FFFFFF', borderwidth=0)
    
    execute_button = ttk.Button(frame, text="Esegui Comandi ADB", style='W.TButton', command=lambda: threading.Thread(target=execute_adb_commands).start())
    execute_button.pack(fill=tk.BOTH, expand=True, pady=10)

    # Frame per le icone
    icons_frame = tk.Frame(root)
    icons_frame.pack(fill=tk.X, side=tk.TOP, anchor='ne')

    # Pulsanti per i link con icone, posizionati nel frame delle icone
    github_button = ttk.Button(icons_frame, image=github_icon, command=lambda: open_url("https://github.com/myUsername"))
    github_button.image = github_icon
    github_button.pack(side=tk.LEFT, padx=5)

    telegram_button = ttk.Button(icons_frame, image=telegram_icon, command=lambda: open_url("https://t.me/myTelegramChannel"))
    telegram_button.image = telegram_icon
    telegram_button.pack(side=tk.LEFT, padx=5)

    paypal_button = ttk.Button(icons_frame, image=paypal_icon, command=lambda: open_url("https://myDonationLink"))
    paypal_button.image = paypal_icon
    paypal_button.pack(side=tk.LEFT, padx=5)

    buymeacoffee_button = ttk.Button(icons_frame, image=buy_me_a_coffee_icon, command=lambda: open_url("https://myDonationLink2"))
    buymeacoffee_button.image = buy_me_a_coffee_icon
    buymeacoffee_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()