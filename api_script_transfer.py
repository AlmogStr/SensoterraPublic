import requests
import json
import pandas as pd
import tkinter as tk
from tkinter import ttk


auth_user = input("enter username: ")
auth_pwd = input("enter password: ")

base_url = "https://monitor.sensoterra.com/api/v3"

auth_url = f"{base_url}/customer/auth"

auth_body = {
    "email": auth_user,
    "password": auth_pwd
}

# Authenticate and get the API key
auth_res = requests.post(auth_url, json=auth_body)
auth_res.raise_for_status()
auth_data = auth_res.json()

# Get the list of customers of a Reseller
get_customer_url = f"{base_url}/customer"

get_customer_res = requests.get(get_customer_url, headers={"api_key": auth_data["api_key"]})
get_customer_res.raise_for_status()
customer_list = get_customer_res.json()
print("customer list: ")
print(*customer_list, sep="\n")

# Choose customers
customer_from = int(input("Enter customer id to transfer from: "))
customer_to = int(input("Enter customer id to transfer to: "))

# Get the list of all probes
get_probes_url = f"{base_url}/probe"

# Choose the parameters for getting the probes
get_probe_query = {
    "limit": 110,
    "skip": 0,
    "customer": customer_from,
    "include_shared_data": "NO"
}

# Retrieve probes data
get_probes_res = requests.get(get_probes_url, params=get_probe_query, headers={"api_key": auth_data["api_key"]})
get_probes_res.raise_for_status()
probe_list = get_probes_res.json()

# Convert the probe list to a DataFrame
probes_df = pd.DataFrame(probe_list)

# Function to create a new DataFrame with only selected probes
def get_selected_probes():
    global new_probes_df
    selected_probes = [probe for i, probe in enumerate(probe_list) if var_list[i].get()]
    new_probes_df = pd.DataFrame(selected_probes)
    root.destroy()  # Close the window

# Function to select all probes7
def select_all():
    for var in var_list:
        var.set(True)

# Function to deselect all probes
def deselect_all():
    for var in var_list:
        var.set(False)

# Initialize main window
root = tk.Tk()
root.title("Select Probes")

# Create a canvas and a vertical scrollbar for scrolling
canvas = tk.Canvas(root)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

# Create a frame inside the canvas
frame = ttk.Frame(canvas)

# Link the scrollbar and the canvas
frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

# Pack the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# Variable list for checkboxes
var_list = []

# Create checkboxes for each probe
for probe in probe_list:
    var = tk.BooleanVar(value=True)
    chk = ttk.Checkbutton(frame, text=probe['serial'], variable=var)
    chk.pack(anchor='w')
    var_list.append(var)

# Select All and Deselect All buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

select_all_btn = ttk.Button(button_frame, text="Select All", command=select_all)
select_all_btn.pack(side=tk.LEFT, padx=5)

deselect_all_btn = ttk.Button(button_frame, text="Deselect All", command=deselect_all)
deselect_all_btn.pack(side=tk.LEFT, padx=5)

# OK button
ok_btn = ttk.Button(button_frame, text="OK", command=get_selected_probes)
ok_btn.pack(side=tk.RIGHT, padx=5)

# Run the main event loop
root.mainloop()


# Prepare the data for the transfer request
transfer_data = {
    "to_customer_id": customer_to,
    "keep_sensordata": True
}

# Iterate through all the probes and transfer each one
for idx, row in new_probes_df.iterrows():
    probe_id = row["id"]
    probe_sn = row["serial"]
    put_transfer_url = f"{base_url}/probe/{probe_id}/transfer"

    # Make the PUT request with headers and JSON data
    put_transfer_res = requests.put(
        put_transfer_url,
        headers={
            "accept": "application/json",
            "language": "en",
            "api_key": auth_data["api_key"],
            "Content-Type": "application/json"
        },
        json=transfer_data
    )

    # Check the response
    print("Probe ID:", probe_id)
    print("Probe Serial:", probe_sn)
    print("Response Status Code:", put_transfer_res.status_code)
    print("Response Text:", put_transfer_res.text)

    # Raise an exception if there was an error
    put_transfer_res.raise_for_status()
    print(f"moved {idx+1} probes")