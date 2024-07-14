import os
import threading
import configparser
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from service.repository import clone_or_pull
from utils.data import *

selected_folder = None

config = configparser.ConfigParser()

def load_config():
    global selected_folder

    if os.path.exists(CONFIG_FILE):
        print("Config file exists, loading...")
        config.read(CONFIG_FILE)
        if config.has_section(CONFIG_SECTION) and config.has_option(CONFIG_SECTION, CONFIG_KEY_FOLDER):
            selected_folder = config.get(CONFIG_SECTION, CONFIG_KEY_FOLDER)
            if os.path.exists(selected_folder): on_folder_selected()
            else: selected_folder = None

def save_config():
    if not config.has_section(CONFIG_SECTION): config.add_section(CONFIG_SECTION)
    config.set(CONFIG_SECTION, CONFIG_KEY_FOLDER, selected_folder)
    with open(CONFIG_FILE, 'w') as config_file: config.write(config_file)


def get_mods_folder():
    return os.path.join(selected_folder, 'mods')

def update_mods(mods_folder):
    try:
        clone_or_pull(REPO_URL, mods_folder)
        list_mods(mods_folder)
        messagebox.showinfo("Finalizado", "Los mods se han actualizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error al actualizar los mods: {e}")

def update_mods_with_spinner(mods_folder):
    start_spinner()
    threading.Thread(target=run_update_mods, args=(mods_folder,)).start()

def run_update_mods(mods_folder):
    try: update_mods(mods_folder)
    finally: stop_spinner()

def select_folder():
    global selected_folder
    folder_selected = filedialog.askdirectory()

    if folder_selected:
        selected_folder = folder_selected
        save_config()
        on_folder_selected()

def on_folder_selected():
    folder_label.config(text=f"Carpeta: {selected_folder}")
    list_mods(get_mods_folder())
    mods_listbox.grid(row=2, column=0, pady=10)
    update_button.grid(row=3, column=0, pady=5)

def list_mods(mods_folder):
    mods_listbox.delete(0, tk.END)

    if os.path.exists(mods_folder) and os.path.isdir(mods_folder):
        mods = [f for f in os.listdir(mods_folder) if f.endswith('.jar')]
        for mod in mods: mods_listbox.insert(tk.END, mod)
    else:
        print("No mods folder, creating it...")
        os.makedirs(mods_folder)
        list_mods(mods_folder)

def start_spinner():
    spinner.grid(row=4, column=0, pady=5)
    spinner.start()

def stop_spinner():
    spinner.stop()
    spinner.grid_remove()

# --------------------------------------------------------------------------------

# Window
root = tk.Tk()
root.title("Instalador YeeLand")

# Selected folder label
folder_label = tk.Label(root, text="Carpeta no seleccionada")
folder_label.grid(row=0, column=0, pady=5)

# Select folder button
select_button = tk.Button(root, text="Seleccionar Carpeta de Minecraft", command=select_folder)
select_button.grid(row=1, column=0, pady=5)

# Spinner (Initially hidden)
spinner = ttk.Progressbar(root, mode='indeterminate')
spinner.grid_remove()

# Update mods button (Initially hidden)
update_button = tk.Button(root, text="Actualizar Mods", command=lambda: update_mods_with_spinner(get_mods_folder()))
update_button.grid_remove()

# Mods listbox (Initially hidden)
mods_listbox = tk.Listbox(root, width=50, height=10)
mods_listbox.grid_remove()

# Start app
load_config()
root.mainloop()