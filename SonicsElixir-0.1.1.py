import subprocess

def run_command(command):
    """Esegue un comando sul sistema e restituisce il risultato."""
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
        print(output)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Errore: {e.output}")
        return False

def main():
    print("Benvenuto in Sonic's Elixir - Il tuo strumento multipiattaforma per la gestione ADB!")
    print("Verifica della connessione al dispositivo...")
    if not run_command("adb devices"):
        print("Errore: Assicurati che ADB sia installato e aggiunto al PATH di sistema.")
        return

    print("Arresto forzato di tutte le app...")
    packages_output = subprocess.check_output("adb shell pm list packages", shell=True, text=True)
    for line in packages_output.splitlines():
        package_name = line.split(":")[1]
        print(f"Arresto forzato di {package_name}...")
        run_command(f"adb shell am force-stop {package_name}")

    print("Tutte le app sono state fermate con successo.")

    print("Cancellazione della cache delle app...")
    # Esegui il comando di pulizia della cache 30 volte
    for _ in range(30):
        if not run_command("adb shell pm trim-caches 1000G"):
            print("Errore durante la cancellazione della cache delle app.")
            return

    print("Cache delle app cancellata con successo.")

    if run_command("adb shell cmd package compile -m speed -f -a"):
        print("Comando di compilazione eseguito con successo.")
    else:
        print("Errore durante l'esecuzione del comando di compilazione.")
        return

    if run_command('adb shell "cmd package bg-dexopt-job"'):
        print("Ottimizzazione in background completata con successo.")
    else:
        print("Errore durante l'esecuzione dell'ottimizzazione in background.")

    print("Tutti i comandi di Sonic's Elixir sono stati eseguiti con successo.")

if __name__ == "__main__":
    main()
