import sys
import os
import subprocess
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QWidget, QTextEdit, QMessageBox, QLabel, QStyleFactory, QProgressBar)
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QColor, QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QEvent

# Colori ispirati a Sonic
SONIC_BLUE = "#0066CC"
SONIC_YELLOW = "#FFD700"
SONIC_WHITE = "#FFFFFF"
SONIC_DARK_GRAY = "#333333"

def get_app_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

class ADBThread(QThread):
    output_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)
    finished_signal = pyqtSignal()

    def __init__(self, commands, adb_path):
        super().__init__()
        self.commands = commands
        self.adb_path = adb_path

    def run(self):
        total_steps = len(self.commands)
        for i, command in enumerate(self.commands, 1):
            self.output_signal.emit(f"Esecuzione del comando {i}/{total_steps}: {command}")
            self.progress_signal.emit(i, total_steps)
            try:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.output_signal.emit(output.strip())
                rc = process.poll()
                if rc != 0:
                    error = process.stderr.read()
                    self.output_signal.emit(f"Errore nell'esecuzione del comando: {error}")
            except Exception as e:
                self.output_signal.emit(f"Errore nell'esecuzione del comando: {str(e)}")
        self.finished_signal.emit()

class SonicButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {SONIC_BLUE};
                color: {SONIC_WHITE};
                border-radius: 15px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {SONIC_YELLOW};
                color: {SONIC_DARK_GRAY};
            }}
        """)

class SonicsElixir(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_path = get_app_path()
        self.adb_path = os.path.join(self.app_path, 'adb', 'adb.exe')
        self.setupEasterEgg()
        self.initUI()

    def setupEasterEgg(self):
        self.secret_sequence = []
        self.secret_code = [Qt.Key.Key_B, Qt.Key.Key_A]
        self.sequence_timer = QTimer(self)
        self.sequence_timer.setSingleShot(True)
        self.sequence_timer.timeout.connect(self.resetSequence)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            self.handleKeyPress(key)
        return super().eventFilter(obj, event)

    def handleKeyPress(self, key):
        self.secret_sequence.append(key)
        if len(self.secret_sequence) > len(self.secret_code):
            self.secret_sequence.pop(0)
        if self.secret_sequence == self.secret_code:
            QMessageBox.information(self, "Super Sonic Mode", "Hai sbloccato la modalità Super Sonic! Ora sei incredibilmente veloce!")
            self.resetSequence()
        else:
            self.sequence_timer.start(2000)

    def resetSequence(self):
        self.secret_sequence.clear()

    def initUI(self):
        self.setWindowTitle("Sonic's Elixir")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(os.path.join(self.app_path, 'icons', 'sonic_icon.png')))

        self.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(SONIC_DARK_GRAY))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(SONIC_WHITE))
        palette.setColor(QPalette.ColorRole.Base, QColor(SONIC_DARK_GRAY))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(SONIC_BLUE))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(SONIC_WHITE))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(SONIC_DARK_GRAY))
        palette.setColor(QPalette.ColorRole.Text, QColor(SONIC_WHITE))
        palette.setColor(QPalette.ColorRole.Button, QColor(SONIC_BLUE))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(SONIC_WHITE))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(SONIC_YELLOW))
        self.setPalette(palette)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Pulsanti principali
        button_layout = QHBoxLayout()
        self.optimize_button = SonicButton("Esegui ottimizzazione", self)
        self.optimize_button.clicked.connect(self.run_optimization)
        self.device_info_button = SonicButton("Informazioni dispositivo", self)
        self.device_info_button.clicked.connect(self.show_device_info)
        self.stop_button = SonicButton("Interrompi esecuzione", self)
        self.stop_button.clicked.connect(self.stop_optimization)
        self.stop_button.hide()  # Nascondi il pulsante inizialmente
        button_layout.addWidget(self.optimize_button)
        button_layout.addWidget(self.device_info_button)
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)

        # Barra di progresso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {SONIC_BLUE};
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {SONIC_YELLOW};
            }}
        """)
        main_layout.addWidget(self.progress_bar)

        # Area di output
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet(f"background-color: {SONIC_DARK_GRAY}; color: {SONIC_WHITE}; border: 1px solid {SONIC_BLUE};")
        main_layout.addWidget(self.output_area)

        # Pulsanti aggiuntivi
        additional_buttons_layout = QHBoxLayout()
        self.exit_button = SonicButton("Esci", self)
        self.exit_button.clicked.connect(self.close)
        self.info_button = SonicButton("Info", self)
        self.info_button.clicked.connect(self.show_info)
        self.version_button = SonicButton("Versione", self)
        self.version_button.clicked.connect(self.show_version)
        self.update_button = SonicButton("Aggiornamento", self)
        self.update_button.clicked.connect(self.check_update)
        additional_buttons_layout.addWidget(self.exit_button)
        additional_buttons_layout.addWidget(self.info_button)
        additional_buttons_layout.addWidget(self.version_button)
        additional_buttons_layout.addWidget(self.update_button)

        main_layout.addLayout(additional_buttons_layout)

        # Collegamenti esterni
        external_links_layout = QHBoxLayout()
        self.telegram_button = QPushButton(QIcon(os.path.join(self.app_path, 'icons', 'telegram.png')), "", self)
        self.telegram_button.clicked.connect(lambda: self.open_link("https://t.me/sonicselixir"))
        self.github_button = QPushButton(QIcon(os.path.join(self.app_path, 'icons', 'github.png')), "", self)
        self.github_button.clicked.connect(lambda: self.open_link("https://github.com/blast752/sonic-s-elixir"))
        self.paypal_button = QPushButton(QIcon(os.path.join(self.app_path, 'icons', 'paypal.png')), "", self)
        self.paypal_button.clicked.connect(lambda: self.open_link("https://www.paypal.me/blast752"))
        self.coffee_button = QPushButton(QIcon(os.path.join(self.app_path, 'icons', 'coffee.png')), "", self)
        self.coffee_button.clicked.connect(lambda: self.open_link("https://www.buymeacoffee.com/BodmLNnMs"))
        
        for button in [self.telegram_button, self.github_button, self.paypal_button, self.coffee_button]:
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {SONIC_BLUE};
                    border-radius: 20px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: {SONIC_YELLOW};
                }}
            """)
            button.setFixedSize(40, 40)
            external_links_layout.addWidget(button)

        main_layout.addLayout(external_links_layout)

        self.adb_thread = None

    def run_optimization(self):
        if not self.check_device_connection():
            return

        self.clear_output()
        self.update_output("Inizio dell'ottimizzazione...")

        commands = [f'"{self.adb_path}" shell pm trim-caches 1000G' for _ in range(100)]
        commands.extend([
            f'"{self.adb_path}" shell cmd package compile -m speed -f -a',
            f'"{self.adb_path}" shell "cmd package bg-dexopt-job"'
        ])

        self.adb_thread = ADBThread(commands, self.adb_path)
        self.adb_thread.output_signal.connect(self.update_output)
        self.adb_thread.progress_signal.connect(self.update_progress)
        self.adb_thread.finished_signal.connect(self.optimization_finished)
        self.adb_thread.start()

        self.optimize_button.setEnabled(False)
        self.show_stop_button()

    def update_progress(self, current, total):
        progress = int((current / total) * 100)
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(f"{progress}% - {current}/{total}")
        self.update_output(f"Progresso: {current}/{total} comandi completati")

    def optimization_finished(self):
        self.optimize_button.setEnabled(True)
        self.stop_button.hide()
        self.update_output("Ottimizzazione completata! Il tuo dispositivo ora è veloce come Sonic!")
        self.progress_bar.setValue(100)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {SONIC_BLUE};
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {SONIC_YELLOW};
            }}
        """)
        self.progress_bar.setFormat("%p%")
        QMessageBox.information(self, "Ottimizzazione Completata", 
                                "L'ottimizzazione è stata completata con successo! Il tuo dispositivo ora è veloce come Sonic!")
    
    def optimization_interrupted(self):
        self.optimize_button.setEnabled(True)
        self.stop_button.hide()
        self.progress_bar.setValue(0)
        QMessageBox.information(self, "Ottimizzazione Interrotta", 
                                "L'ottimizzazione è stata interrotta. Il dispositivo potrebbe essere in uno stato parzialmente ottimizzato.")

    def show_stop_button(self):
        self.stop_button.show()

    def stop_optimization(self):
        if self.adb_thread and self.adb_thread.isRunning():
            reply = QMessageBox.question(self, 'Conferma Interruzione', 
                                        "Sei sicuro di voler interrompere l'ottimizzazione? Il dispositivo potrebbe rimanere in uno stato parzialmente ottimizzato.",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.adb_thread.terminate()
                self.adb_thread.wait()
                self.update_output("Ottimizzazione interrotta! Sonic ha frenato la sua corsa.")
                self.progress_bar.setStyleSheet(f"""
                    QProgressBar {{
                        border: 2px solid {SONIC_BLUE};
                        border-radius: 5px;
                        text-align: center;
                    }}
                    QProgressBar::chunk {{
                        background-color: {SONIC_YELLOW};
                        width: 20px;
                    }}
                """)
                self.progress_bar.setFormat("Interrotto")
                self.optimization_interrupted()

    def show_device_info(self):
        if not self.check_device_connection():
            return

        self.clear_output()
        self.update_output("Recupero delle informazioni sul dispositivo...")
        try:
            result = subprocess.run(f'"{self.adb_path}" devices -l', shell=True, check=True, capture_output=True, text=True)
            self.update_output("Informazioni dispositivo:")
            for line in result.stdout.splitlines():
                self.update_output(line)
        except subprocess.CalledProcessError as e:
            self.update_output(f"Errore nel recupero delle informazioni del dispositivo: {e.stderr}")

    def check_device_connection(self):
        self.clear_output()
        self.update_output("Verifica della connessione del dispositivo...")
        try:
            result = subprocess.run(f'"{self.adb_path}" devices', shell=True, check=True, capture_output=True, text=True)
            if "device" not in result.stdout:
                self.update_output("Nessun dispositivo connesso. Connetti un dispositivo e riprova, veloce come Sonic!")
                return False
            self.update_output("Dispositivo connesso correttamente!")
            return True
        except subprocess.CalledProcessError as e:
            self.update_output(f"Errore nella verifica della connessione del dispositivo: {e.stderr}")
            return False

    def clear_output(self):
        self.output_area.clear()
        self.progress_bar.setValue(0)

    def update_output(self, text):
        self.output_area.append(text)
        self.output_area.verticalScrollBar().setValue(self.output_area.verticalScrollBar().maximum())

    def show_info(self):
        info_text = ("Sonic's Elixir\n"
                     "Sviluppato con la velocità di Sonic per ottimizzare i tuoi dispositivi Android!\n"
                     "Easter Egg: Prova la sequenza segreta di Sonic per sbloccare una sorpresa!")
        QMessageBox.information(self, "Informazioni", info_text)

    def show_version(self):
        version = "0.5.0"  # Aggiornata la versione
        QMessageBox.information(self, "Versione", f"Sonic's Elixir versione {version} - Veloce come il vento!")

    def check_update(self):
        current_version = "0.5.0"  # Assicurati che corrisponda alla versione attuale
        github_repo = "blast752/sonic-s-elixir"
        
        try:
            response = requests.get(f"https://api.github.com/repos/{github_repo}/releases/latest")
            response.raise_for_status()  # Solleva un'eccezione per errori HTTP
            latest_release = response.json()
            
            if "tag_name" not in latest_release:
                raise ValueError("Tag name not found in the GitHub release")
            
            latest_version = latest_release["tag_name"].lstrip('v')
            
            if latest_version > current_version:
                update_msg = f"È disponibile una nuova versione: {latest_version}. Vuoi correre ad aggiornarla?"
                reply = QMessageBox.question(self, 'Aggiornamento disponibile', update_msg, 
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    self.update_output("Avvio dell'aggiornamento... Preparati per una corsa supersonica!")
                    self.download_and_install_update(latest_release)
            else:
                QMessageBox.information(self, "Aggiornamento", "Sei già alla velocità massima! Nessun aggiornamento disponibile.")
        except requests.RequestException as e:
            QMessageBox.warning(self, "Errore di rete", f"Impossibile controllare gli aggiornamenti: {str(e)}")
        except ValueError as e:
            QMessageBox.warning(self, "Errore", f"Errore nel formato della risposta GitHub: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Oops! Un ostacolo nell'aggiornamento: {str(e)}")

    def download_and_install_update(self, release):
        try:
            # Trova l'asset .exe nella release
            exe_asset = next((asset for asset in release["assets"] if asset["name"].endswith(".exe")), None)
            if not exe_asset:
                raise ValueError("Nessun file .exe trovato nella release")

            # Scarica il nuovo eseguibile
            download_url = exe_asset["browser_download_url"]
            new_exe_path = os.path.join(os.path.dirname(sys.executable), "SonicsElixir_new.exe")
            
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            with open(new_exe_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Crea uno script batch per sostituire l'eseguibile e riavviare l'applicazione
            current_exe = sys.executable
            batch_path = os.path.join(os.path.dirname(sys.executable), "update.bat")
            with open(batch_path, 'w') as batch:
                batch.write(f'''
    @echo off
    timeout /t 2 /nobreak >nul
    del "{current_exe}"
    move "{new_exe_path}" "{current_exe}"
    start "" "{current_exe}"
    del "%~f0"
    ''')

            # Esegui lo script batch e chiudi l'applicazione corrente
            subprocess.Popen(batch_path, shell=True)
            self.close()
            sys.exit(0)

        except Exception as e:
            QMessageBox.warning(self, "Errore di aggiornamento", f"Impossibile completare l'aggiornamento: {str(e)}")

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SonicsElixir()
    ex.show()
    sys.exit(app.exec())