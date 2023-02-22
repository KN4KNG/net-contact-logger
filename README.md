
# Ham Radio Contact Logger

This is a simple Python program that allows users to log their amateur radio contacts. The program uses a graphical user interface (GUI) built with the tkinter library. The log entries are stored in a CSV file, and the program uses the callook.info API to get the name and location of the station being logged.

## Features

The program has the following features:

-   A GUI with separate frames for entering net information and logging contacts.
-   The ability to log contacts with the following information:
    -   Net name
    -   Net frequency
    -   Net mode
    -   Call sign of the station being logged
    -   Name and location of the station being logged (retrieved from the callook.info API)
    -   Comments about the contact
-   The ability to clear the call sign and comments entry fields.
-   The ability to display a list of all logged contacts in a treeview.
-   The ability to refresh the list of logged contacts.

## Requirements

-   Python 3.6 or higher
-   The following Python packages:
    -   tkinter
    -   ttk
    -   requests

## Installation

1.  Clone the repository to your local machine:
    
    bashCopy code
    
    `git clone https://github.com/kn4kng/ham-radio-contact-logger.git` 
    
2.  Install the required Python packages:
    
    Copy code
    
    `pip install tkinter ttk requests` 
    
3.  Run the program:
    
    Copy code
    
    `python ham_radio_contact_logger.py` 
    

## Usage

1.  Enter the net information in the "Net Info" frame.
2.  Enter the call sign and any comments about the contact in the "Log Contact" frame.
3.  Press the "Log Contact" button to add the contact to the log.
4.  Press the "Refresh Log" button to display the updated list of contacts in the treeview.
5.  Press the "Clear Entries" button to clear the call sign and comments entry fields.

## Contributors

Contributions to this project are welcome. If you find a bug or have a feature request, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.
