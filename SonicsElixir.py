import os
import subprocess
import sys

def install_dependencies():
    try:
        # Ottieni il percorso assoluto dello script Python corrente
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Costruisci il percorso assoluto del file requirements.txt
        requirements_path = os.path.join(script_dir, "requirements.txt")
        
        # Verifica se il file requirements.txt esiste
        if os.path.isfile(requirements_path):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        else:
            print("File requirements.txt non trovato. Assicurati che sia presente nella stessa directory dello script.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'installazione delle dipendenze: {e}")
        sys.exit(1)

install_dependencies()

import json
import logging
import subprocess
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

class SonicsElixir:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SonicsElixir")
        self.root.geometry("800x600")
        self.root.configure(bg="#1C1C1C")

        self.sonic_blue = "#0072F5"
        self.sonic_yellow = "#FFD700"
        self.sonic_red = "#FF4136"
        self.background_color = "#1C1C1C"
        self.foreground_color = "#FFFFFF"
        self.highlight_color = "#2C2C2C"

        self.load_config()
        self.setup_logging()
        self.load_translations()
        self.create_gui()

    def load_config(self):
        try:
            with open("config.json", "r") as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            logging.warning("File di configurazione non trovato. Verranno utilizzate le impostazioni predefinite.")
            self.config = {
                "resources_path": "resources/icons",
                "github_url": "https://github.com/blast752",
                "telegram_url": "https://t.me/sonicselixir",
                "paypal_url": "https://stillunderprogress.gg",
                "buymeacoffee_url": "https://buymeacoffee.com/bodmlnnms"
            }

    def setup_logging(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_translations(self):
        try:
            with open("translations.json", "r") as translations_file:
                self.translations = json.load(translations_file)
        except FileNotFoundError:
            logging.warning("File di traduzioni non trovato. Verranno utilizzate le traduzioni predefinite.")
            self.translations = {
                "it": {
                    "title": "SonicsElixir",
                    "version": "Versione 0.2.0",
                    "description": "Utility per gestire dispositivi Android tramite ADB.",
                    "execute_button": "Esegui Comandi ADB",
                    "language_label": "Seleziona Lingua:",
                    "device_connected": "Dispositivo connesso correttamente.",
                    "device_not_connected": "Nessun dispositivo connesso. Assicurati che il dispositivo sia collegato correttamente e che siano abilitati i permessi ADB.",
                    "error_occurred": "Si è verificato un errore. Riprova più tardi.",
                    "adb_commands_success": "Operazioni ADB completate con successo!",
                    "exit_message": "Grazie per aver utilizzato SonicsElixir. Arrivederci!"
                },
                "en": {
                    "title": "SonicsElixir",
                    "version": "Version 0.2.0",
                    "description": "Utility to manage Android devices via ADB.",
                    "execute_button": "Execute ADB Commands",
                    "language_label": "Select Language:",
                    "device_connected": "Device connected successfully.",
                    "device_not_connected": "No device connected. Make sure the device is properly connected and ADB permissions are granted.",
                    "error_occurred": "An error occurred. Please try again later.",
                    "adb_commands_success": "ADB operations completed successfully!",
                    "exit_message": "Thank you for using SonicsElixir. Goodbye!"
                }
            }

    def change_language(self, language):
        self.current_language = language
        self.update_gui_language()

    def update_gui_language(self):
        translations = self.translations[self.current_language]
        self.title_label.config(text=translations["title"])
        self.version_label.config(text=translations["version"])
        self.description_label.config(text=translations["description"])
        self.execute_button.config(text=translations["execute_button"])
        self.language_label.config(text=translations["language_label"])

    def write_output(self, text):
        self.terminal_output.insert(tk.END, text + "\n")
        self.terminal_output.see(tk.END)

    def run_command(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in process.stdout:
                self.write_output(line.strip())
            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command, output=process.stderr.read())
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Errore durante l'esecuzione del comando: {command}")
            logging.error(e.output)
            self.write_output(f"Errore durante l'esecuzione del comando: {command}\n{e.output}")
            return False

    def check_device_connection(self):
        try:
            output = subprocess.check_output("adb devices", shell=True, text=True)
            if "device" in output:
                return True
            else:
                return False
        except subprocess.CalledProcessError:
            return False

    def execute_adb_commands(self):
        if not self.check_device_connection():
            messagebox.showerror("Errore", self.translations[self.current_language]["device_not_connected"])
            return

        self.write_output(self.translations[self.current_language]["device_connected"])

        self.write_output("Arresto forzato di tutte le app...")
        try:
            packages_output = subprocess.check_output("adb shell pm list packages", shell=True, text=True)
            packages = [line.split(":")[1] for line in packages_output.splitlines() if line.startswith("package:")]
            
            for package in packages:
                self.write_output(f"Arresto forzato di {package}...")
                if not self.run_command(f"adb shell am force-stop {package}"):
                    messagebox.showerror("Errore", f"Errore durante l'arresto forzato di {package}.")
                    return
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", "Errore durante l'ottenimento dell'elenco dei pacchetti.")
            return

        self.write_output("Cancellazione della cache delle app...")
        for i in range(50):
            if not self.run_command("adb shell pm trim-caches 1000G"):
                messagebox.showerror("Errore", "Errore durante la cancellazione della cache delle app.")
                return
            else:
                self.write_output(f"Iterazione {i+1}/50: Cache delle app in fase di cancellazione...")

        self.write_output("Cache delle app cancellata con successo.")

        self.write_output("Ottimizzazione delle applicazioni in corso...")
        if self.run_command("adb shell cmd package compile -m speed -f -a"):
            self.write_output("Comando di compilazione eseguito con successo.")
        else:
            messagebox.showerror("Errore", "Errore durante l'esecuzione del comando di compilazione.")
            return

        if self.run_command('adb shell "cmd package bg-dexopt-job"'):
            self.write_output("Ottimizzazione in background completata con successo.")
        else:
            messagebox.showerror("Errore", "Errore durante l'ottimizzazione in background.")
            return

        messagebox.showinfo("Successo", self.translations[self.current_language]["adb_commands_success"])

    def open_url(self, url):
        webbrowser.open_new_tab(url)

    def create_gui(self):
        script_dir = Path(__file__).resolve().parent
        resources_path = script_dir / self.config["resources_path"]

        github_icon = ImageTk.PhotoImage(Image.open(resources_path / "github-icon.png"))
        telegram_icon = ImageTk.PhotoImage(Image.open(resources_path / "telegram-icon.png"))
        buy_me_a_coffee_icon = ImageTk.PhotoImage(Image.open(resources_path / "buy-me-a-coffee-icon.png"))
        paypal_icon = ImageTk.PhotoImage(Image.open(resources_path / "paypal-icon.png"))

        style = ttk.Style()
        style.configure('TFrame', background=self.background_color)
        style.configure('TLabel', background=self.background_color, foreground=self.foreground_color, font=("Helvetica", 12))
        style.configure('TButton', background=self.sonic_blue, foreground=self.foreground_color, font=("Helvetica", 12, "bold"))
        style.map('TButton', background=[('active', self.sonic_yellow)])

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(frame, text="SonicsElixir", font=("Helvetica", 24, "bold"), foreground=self.sonic_blue)
        self.title_label.pack(pady=(0, 10))

        self.version_label = ttk.Label(frame, text="Versione 0.2.0", font=("Helvetica", 10), foreground=self.foreground_color)
        self.version_label.pack()

        self.description_label = ttk.Label(frame, text="Utility per gestire dispositivi Android tramite ADB.", wraplength=600, justify="center", foreground=self.foreground_color)
        self.description_label.pack(pady=(20, 0))

        language_frame = ttk.Frame(frame)
        language_frame.pack(pady=(10, 0))

        self.language_label = ttk.Label(language_frame, text="Seleziona Lingua:")
        self.language_label.pack(side=tk.LEFT, padx=(0, 10))

        language_var = tk.StringVar(value="it")
        language_dropdown = ttk.Combobox(language_frame, textvariable=language_var, values=["it", "en"], state="readonly")
        language_dropdown.pack(side=tk.LEFT)
        language_dropdown.bind("<<ComboboxSelected>>", lambda event: self.change_language(language_var.get()))

        self.execute_button = ttk.Button(frame, text="Esegui Comandi ADB", command=lambda: threading.Thread(target=self.execute_adb_commands).start())
        self.execute_button.pack(fill=tk.X, pady=(20, 0), ipady=10)

        self.terminal_output = tk.Text(frame, height=10, width=80, bg=self.highlight_color, fg=self.foreground_color, font=("Courier", 10))
        self.terminal_output.pack(pady=(20, 0))

        self.current_language = "it"
        self.update_gui_language()

        icons_frame = ttk.Frame(frame)
        icons_frame.pack(side=tk.BOTTOM, pady=(20, 0))

        github_button = ttk.Button(icons_frame, image=github_icon, command=lambda: self.open_url(self.config["github_url"]))
        github_button.image = github_icon
        github_button.pack(side=tk.LEFT, padx=5)

        telegram_button = ttk.Button(icons_frame, image=telegram_icon, command=lambda: self.open_url(self.config["telegram_url"]))
        telegram_button.image = telegram_icon
        telegram_button.pack(side=tk.LEFT, padx=5)

        paypal_button = ttk.Button(icons_frame, image=paypal_icon, command=lambda: self.open_url(self.config["paypal_url"]))
        paypal_button.image = paypal_icon
        paypal_button.pack(side=tk.LEFT, padx=5)

        buymeacoffee_button = ttk.Button(icons_frame, image=buy_me_a_coffee_icon, command=lambda: self.open_url(self.config["buymeacoffee_url"]))
        buymeacoffee_button.image = buy_me_a_coffee_icon
        buymeacoffee_button.pack(side=tk.LEFT, padx=5)

    def run(self):
        self.root.mainloop()
        messagebox.showinfo("Arrivederci", self.translations[self.current_language]["exit_message"])


if __name__ == "__main__":
    app = SonicsElixir()
    app.run()
