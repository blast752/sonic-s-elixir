# SonicsElixir

SonicsElixir is a utility program for managing Android devices via ADB (Android Debug Bridge). It provides a user-friendly graphical interface to execute various ADB commands and optimize the performance of connected Android devices. NB that this program is still a beta pre-release and needs lot of testing
Table of Contents

    Features
    Prerequisites
    Installation
    Usage
    Configuration
    Translations
    Contributing
    License

Features

    Execute ADB commands to manage connected Android devices
    Force stop all running applications
    Clear application cache
    Optimize application performance through compilation and background optimization
    Support for multiple languages (English and Italian)
    Logging and error handling
    User-friendly graphical interface with icons and themed elements

Prerequisites

Before using SonicsElixir, ensure that you have the following prerequisites installed on your Windows system:

    Python 3.x
    ADB (Android Debug Bridge) command-line tool

Installation

    Download the latest available version of Sonic's Elixir from my GitHub page
    Extract in a directory named Sonic-s Elixir the downloaded files
    Open command prompt (cmd) or PowerShell and navigate to the project directory.
    Install the required dependencies by running the following command:
    basic
    
    pip install -r requirements.txt

Usage

    Connect your Android device to your computer via USB.
    Enable USB debugging on your Android device in the Developer options.
    Run the SonicsElixir program by executing the following command:

    python sonics_elixir.py

    The SonicsElixir graphical interface will open.
    Select the desired language from the language dropdown menu.
    Click the "Execute ADB Commands" button to start the optimization process.
    The program will execute various ADB commands, including force stopping applications, clearing cache, and optimizing application performance.
    The progress and output of the commands will be displayed in the terminal output area.
    If any errors occur during the process, an error message will be displayed, and the program will terminate gracefully.
    Once the optimization process is complete, a success message will be shown.

Configuration

SonicsElixir uses a configuration file (config.json) to store various settings and URLs. This will be used for futures updates and purposes
IN PROGRESS...

Translations

SonicsElixir supports multiple languages through a translations file (translations.json). The default translations are provided for English and Italian. You can add or modify translations by editing the translations.json file.

Contributing

Contributions to SonicsElixir are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.
License

This project is licensed under the MIT License.

Note: Do not use SonicsElixir on devices without proper authorization. Always ensure that you have the necessary permissions and comply with the terms and conditions of the device manufacturer and any applicable laws and regulations.

Disclaimer: The developers of SonicsElixir are not responsible for any damage or loss caused by the use of this program. Use it at your own risk.
