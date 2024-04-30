# Sonic's Elixir
Sonic's Elixir è un script Python che consente di ottimizzare le prestazioni e la salute di dispositivi Android.

Lo script esegue le seguenti operazioni:

    Controlla la disponibilità di ADB.
    Controlla la presenza di dispositivi collegati.
    Controlla se l'USB debugging è abilitato per ciascun dispositivo.
    Ottiene le informazioni sul dispositivo, come modello, marchio e versione di Android.
    Esegue i seguenti comandi ADB:
    adb shell pm trim-caches: libera la cache di sistema e delle applicazioni.
    adb shell cmd package compile -m speed-profile -f -a: compila le applicazioni in modalità di profilo di velocità.
    adb shell cmd package bg-dexopt-job: esegue l'ottimizzazione di dex in background (riduce abbastanza il battery draining).

Guida all'uso:

Per utilizzare lo script, è necessario installare Python 3 e ADB.

Una volta installati i requisiti, è possibile eseguire lo script come segue:

python sonic-s-elixir.py

Lo script eseguirà tutte le operazioni descritte nella sezione "Descrizione".
