import csv
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests

def get_name_and_location(call_sign):
    url = f"https://callook.info/{call_sign}/json"
    response = requests.get(url)
    data = response.json()
    name = ""
    location = ""
    if data["status"] == "VALID":
        name = data.get("name", "")
        location = f"{data.get('address', {}).get('line1', '')}, {data.get('address', {}).get('line2', '')}"
        return name, location
    else:
        return None

def log_contact(net_name, net_frequency, net_mode, treeview, net_call_sign_entry, net_comments_entry):
    call_sign = net_call_sign_entry.get()
    name_location = get_name_and_location(call_sign)
    if name_location is not None:
        name, location = name_location
    else:
        messagebox.showinfo(title="Invalid Callsign", message="You entered an invalid callsign. Please make sure the callsign is correct.")
        return

    log_contact_to_csv(net_name, net_frequency, net_mode, treeview, net_call_sign_entry, net_comments_entry, name=name, location=location)

def log_contact_to_csv(net_name, net_frequency, net_mode, treeview, call_sign_entry, comments_entry, name=None, location=None):
    call_sign = call_sign_entry.get()

    if not name and not location:
        name, location = get_name_and_location(call_sign)

    date = datetime.datetime.now()
    with open("log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, net_name, net_frequency, net_mode, call_sign, name, location, comments_entry.get()])

    print(f"Wrote log entry: {date} {net_name} {net_frequency} {net_mode} {call_sign} {name} {location} {comments_entry.get()}")

    display_log(treeview)

def clear_entries(entry_call_sign, entry_comments):
    entry_call_sign.delete(0, tk.END)
    entry_comments.delete(0, tk.END)

def display_log(treeview):
    print("Displaying log...")
    treeview.delete(*treeview.get_children())
    with open("log.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "Date" not in row:
                continue
            try:
                date = datetime.datetime.strptime(row["Date"], "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                continue
            if date.date() == datetime.datetime.now().date():
                treeview.insert("", tk.END, values=(date, row["Net Name"], row["Net Frequency"], row["Net Mode"], row["Call Sign"], row["Name"], row["Location"], row["Comments"]))

    # Configure column widths
    treeview.column(0, width=120, anchor="center")
    treeview.column(1, width=120, anchor="center")
    treeview.column(2, width=120, anchor="center")
    treeview.column(3, width=120, anchor="center")
    treeview.column(4, width=120, anchor="center")
    treeview.column(5, width=120, anchor="center")
    treeview.column(6, width=120, anchor="center")
    treeview.column(7, width=120, anchor="center")

    # Set treeview to grow with the window
    treeview.grid(sticky="nsew")

    # Update layout
    treeview.update_idletasks()

def main():
    root = tk.Tk()
    root.title("Log Contacts")
    root.minsize(800, 600) # set minimum size for root window
    root.resizable(True, True) # allow resizing in x and y directions
    # Net info frame
    net_info_frame = ttk.LabelFrame(root, text="Net Info")
    net_info_frame.pack(padx=10, pady=10)

    # Net name
    net_name_label = ttk.Label(net_info_frame, text="Net Name:")
    net_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

    net_name_entry = ttk.Entry(net_info_frame)
    net_name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Net frequency
    net_frequency_label = ttk.Label(net_info_frame, text="Net Frequency:")
    net_frequency_label.grid(row=1, column=0, padx=5, pady=5, sticky="W")

    net_frequency_entry = ttk.Entry(net_info_frame)
    net_frequency_entry.grid(row=1, column=1, padx=5, pady=5)

    # Net mode
    net_mode_label = ttk.Label(net_info_frame, text="Net Mode:")
    net_mode_label.grid(row=2, column=0, padx=5, pady=5, sticky="W")

    net_mode_entry = ttk.Entry(net_info_frame)
    net_mode_entry.grid(row=2, column=1, padx=5, pady=5)

    # Log contact frame
    log_contact_frame = ttk.LabelFrame(root, text="Log Contact")
    log_contact_frame.pack(padx=10, pady=10)

    # Call sign
    call_sign_label = ttk.Label(log_contact_frame, text="Call Sign:")
    call_sign_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

    call_sign_entry = ttk.Entry(log_contact_frame)
    call_sign_entry.grid(row=0, column=1, padx=5, pady=5)
    # Bind the "<Return>" event to the log_contact function for the Call Sign field
    call_sign_entry.bind("<Return>", lambda event: log_contact(net_name_entry.get(), net_frequency_entry.get(), net_mode_entry.get(), treeview, call_sign_entry, comments_entry))

    # Comments
    comments_label = ttk.Label(log_contact_frame, text="Comments:")
    comments_label.grid(row=3, column=0, padx=5, pady=5, sticky="W")

    comments_entry = ttk.Entry(log_contact_frame)
    comments_entry.grid(row=3, column=1, padx=5, pady=5)
    # Bind the "<Return>" event to the log_contact function for the Comments field
    comments_entry.bind("<Return>", lambda event: log_contact(net_name_entry.get(), net_frequency_entry.get(), net_mode_entry.get(), treeview, call_sign_entry, comments_entry))

    button_width = 20

    # Log contact button
    log_contact_button = ttk.Button(log_contact_frame, text="Log Contact", command=lambda: log_contact(net_name_entry.get(), net_frequency_entry.get(), net_mode_entry.get(), treeview, call_sign_entry, comments_entry), width=button_width)
    log_contact_button.grid(row=4, column=1, padx=5, pady=5)

    # Clear entries button
    clear_entries_button = ttk.Button(log_contact_frame, text="Clear Entries", command=lambda: clear_entries(call_sign_entry, comments_entry), width=button_width)
    clear_entries_button.grid(row=5, column=1, padx=5, pady=5)

    # Refresh log button
    refresh_log_button = ttk.Button(log_contact_frame, text="Refresh Log", command=lambda: display_log(treeview), width=button_width)
    refresh_log_button.grid(row=4, column=0, padx=5, pady=5)

    # Quit button
    quit_button = ttk.Button(log_contact_frame, text="Quit", command=root.destroy, width=button_width)
    quit_button.grid(row=5, column=0, padx=5, pady=5)

    # Center the buttons horizontally
    log_contact_frame.grid_columnconfigure(0, weight=1)
    log_contact_frame.grid_columnconfigure(1, weight=1)
    log_contact_frame.grid_columnconfigure(2, weight=1)
    log_contact_frame.grid_columnconfigure(3, weight=1)

    log_contact_frame.grid_rowconfigure(4, weight=1)

    log_contact_button.grid(sticky="ew")
    clear_entries_button.grid(sticky="ew")
    refresh_log_button.grid(sticky="ew")
    quit_button.grid(sticky="ew")

    # Treeview
    treeview_frame = ttk.LabelFrame(root, text="Log")
    treeview_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.BOTTOM, anchor=tk.S)

    treeview = ttk.Treeview(treeview_frame, columns=("Date", "Net Name", "Net Frequency", "Net Mode", "Call Sign", "Name", "Location", "Comments"), show="headings")
    treeview.pack(fill=tk.BOTH, expand=True)

    treeview.column("Date", width=120, anchor="center", stretch=False)
    treeview.heading("Date", text="Date")
    
    treeview.column("Net Name", anchor="center", stretch=True)
    treeview.heading("Net Name", text="Net Name")

    treeview.column("Net Frequency", anchor="center", stretch=True)
    treeview.heading("Net Frequency", text="Net Frequency")

    treeview.column("Net Mode", anchor="center", stretch=True)
    treeview.heading("Net Mode", text="Net Mode")

    treeview.column("Call Sign", width=120, anchor="center", stretch=False)
    treeview.heading("Call Sign", text="Call Sign")

    treeview.column("Name", anchor="center", stretch=True)
    treeview.heading("Name", text="Name")

    treeview.column("Location", anchor="center", stretch=True)
    treeview.heading("Location", text="Location")

    treeview.column("Comments", anchor="center", stretch=True)
    treeview.heading("Comments", text="Comments")

    treeview.grid(row=0, column=0, sticky="nsew")

    treeview_frame.rowconfigure(0, weight=1)
    treeview_frame.columnconfigure(0, weight=1)

    # Display initial log
    display_log(treeview)

    # Start event loop
    root.mainloop()

main ()
