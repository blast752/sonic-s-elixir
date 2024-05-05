import json
import logging
import os
import subprocess
import sys
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

        self.setup_logging()
        self.load_translations()
        self.create_gui()

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
                    "version": "Versione 0.2.1",
                    "description": "Utility per gestire dispositivi Android tramite ADB.",
                    "execute_button": "Esegui Comandi ADB",
                    "language_label": "Seleziona Lingua:",
                    "device_connected": "Dispositivo connesso correttamente.",
                    "device_not_connected": "Nessun dispositivo connesso. Assicurati che il dispositivo sia collegato correttamente e che siano abilitati i permessi ADB.",
                    "error_occurred": "Si è verificato un errore. Riprova più tardi.",
                    "adb_commands_success": "Operazioni ADB completate con successo!",
                    "exit_message": "Grazie per aver utilizzato SonicsElixir. Arrivederci!",
                    "force_stop_apps": "Arresto forzato di tutte le app...",
                    "force_stop_app": "Arresto forzato di {package}...",
                    "force_stop_error": "Errore durante l'arresto forzato di {package}.",
                    "clear_app_cache": "Cancellazione della cache delle app...",
                    "clear_app_cache_iteration": "Iterazione {iteration}/50: Cache delle app in fase di cancellazione...",
                    "clear_app_cache_success": "Cache delle app cancellata con successo.",
                    "clear_app_cache_error": "Errore durante la cancellazione della cache delle app.",
                    "optimize_apps": "Ottimizzazione delle applicazioni in corso...",
                    "optimize_apps_success": "Comando di compilazione eseguito con successo.",
                    "optimize_apps_error": "Errore durante l'esecuzione del comando di compilazione.",
                    "optimize_apps_bg_success": "Ottimizzazione in background completata con successo.",
                    "optimize_apps_bg_error": "Errore durante l'ottimizzazione in background.",
                    "packages_list_error": "Errore durante l'ottenimento dell'elenco dei pacchetti."
                },
                "en": {
                    "title": "SonicsElixir",
                    "version": "Version 0.2.1",
                    "description": "Utility to manage Android devices via ADB.",
                    "execute_button": "Execute ADB Commands",
                    "language_label": "Select Language:",
                    "device_connected": "Device connected successfully.",
                    "device_not_connected": "No device connected. Make sure the device is properly connected and ADB permissions are granted.",
                    "error_occurred": "An error occurred. Please try again later.",
                    "adb_commands_success": "ADB operations completed successfully!",
                    "exit_message": "Thank you for using SonicsElixir. Goodbye!",
                    "force_stop_apps": "Force stopping all apps...",
                    "force_stop_app": "Force stopping {package}...",
                    "force_stop_error": "Error while force stopping {package}.",
                    "clear_app_cache": "Clearing app cache...",
                    "clear_app_cache_iteration": "Iteration {iteration}/50: Clearing app cache...",
                    "clear_app_cache_success": "App cache cleared successfully.",
                    "clear_app_cache_error": "Error while clearing app cache.",
                    "optimize_apps": "Optimizing applications...",
                    "optimize_apps_success": "Compilation command executed successfully.",
                    "optimize_apps_error": "Error while executing the compilation command.",
                    "optimize_apps_bg_success": "Background optimization completed successfully.",
                    "optimize_apps_bg_error": "Error during background optimization.",
                    "packages_list_error": "Error while retrieving the package list."
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
            adb_path = self.get_adb_path()
            command = f'"{adb_path}" {command}'
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

    def get_adb_path(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, "resources", "adb", "windows", "adb.exe")

    def check_device_connection(self):
        try:
            adb_path = self.get_adb_path()
            output = subprocess.check_output(f'"{adb_path}" devices', shell=True, text=True)
            if "device" in output:
                return True
            else:
                return False
        except subprocess.CalledProcessError:
            return False
        
    def execute_adb_commands(self):
        translations = self.translations[self.current_language]

        if not self.check_device_connection():
            messagebox.showerror("Errore", translations["device_not_connected"])
            return

        self.write_output(translations["device_connected"])

        self.write_output(translations["force_stop_apps"])
        try:
            adb_path = self.get_adb_path()
            packages_output = subprocess.check_output(f'"{adb_path}" shell pm list packages', shell=True, text=True)
            packages = [line.split(":")[1] for line in packages_output.splitlines() if line.startswith("package:")]

            for package in packages:
                self.write_output(translations["force_stop_app"].format(package=package))
                if not self.run_command(f'shell am force-stop {package}'):
                    messagebox.showerror("Errore", translations["force_stop_error"].format(package=package))
                    return
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", translations["packages_list_error"])
            return

        self.write_output(translations["clear_app_cache"])
        for i in range(50):
            if not self.run_command("shell pm trim-caches 1000G"):
                messagebox.showerror("Errore", translations["clear_app_cache_error"])
                return
            else:
                self.write_output(translations["clear_app_cache_iteration"].format(iteration=i+1))

        self.write_output(translations["clear_app_cache_success"])

        self.write_output(translations["optimize_apps"])
        if self.run_command("shell cmd package compile -m speed -f -a"):
            self.write_output(translations["optimize_apps_success"])
        else:
            messagebox.showerror("Errore", translations["optimize_apps_error"])
            return

        if self.run_command('shell "cmd package bg-dexopt-job"'):
            self.write_output(translations["optimize_apps_bg_success"])
        else:
            messagebox.showerror("Errore", translations["optimize_apps_bg_error"])
            return

        messagebox.showinfo("Successo", translations["adb_commands_success"])

    def open_url(self, url):
        webbrowser.open_new_tab(url)

    def create_gui(self):
        script_dir = Path(__file__).resolve().parent
        resources_path = script_dir / "resources" / "icons"

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

        self.version_label = ttk.Label(frame, text="Versione 0.2.1", font=("Helvetica", 10), foreground=self.foreground_color)
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

        github_button = ttk.Button(icons_frame, image=github_icon, command=lambda: self.open_url("https://github.com/blast752"))
        github_button.image = github_icon
        github_button.pack(side=tk.LEFT, padx=5)

        telegram_button = ttk.Button(icons_frame, image=telegram_icon, command=lambda: self.open_url("https://t.me/sonicselixir"))
        telegram_button.image = telegram_icon
        telegram_button.pack(side=tk.LEFT, padx=5)

        paypal_button = ttk.Button(icons_frame, image=paypal_icon, command=lambda: self.open_url("https://stillunderprogress.gg"))
        paypal_button.image = paypal_icon
        paypal_button.pack(side=tk.LEFT, padx=5)

        buymeacoffee_button = ttk.Button(icons_frame, image=buy_me_a_coffee_icon, command=lambda: self.open_url("https://buymeacoffee.com/bodmlnnms"))
        buymeacoffee_button.image = buy_me_a_coffee_icon
        buymeacoffee_button.pack(side=tk.LEFT, padx=5)

    def run(self):
        self.root.mainloop()
        messagebox.showinfo("Arrivederci", self.translations[self.current_language]["exit_message"])


def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'installazione delle dipendenze: {e}")
        sys.exit(1)


if __name__ == "__main__":
    install_dependencies()
    app = SonicsElixir()
    app.run()