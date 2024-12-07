import os
import subprocess
import json
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, Menu
import ctypes
import sys

# Hide the console window on Windows
if sys.platform == "win32":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

PROFILES_FILE = "profiles.json"  # The single JSON file to store all profiles

def create_profiles_file_if_not_exists():
    """Create the profiles.json file if it doesn't exist."""
    if not os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "w") as file:
            json.dump({}, file)  # Initialize an empty JSON object

def load_all_profiles():
    """Load all profiles from the JSON file."""
    create_profiles_file_if_not_exists()  # Ensure the file exists before loading
    with open(PROFILES_FILE, "r") as file:
        return json.load(file)

def save_all_profiles(profiles):
    """Save all profiles to the JSON file."""
    with open(PROFILES_FILE, "w") as file:
        json.dump(profiles, file, indent=4)

def save_profile(profile_name, programs):
    """Save a single profile to the JSON file."""
    profiles = load_all_profiles()
    profiles[profile_name] = {"programs": programs}
    save_all_profiles(profiles)
    messagebox.showinfo("Success", f"Profile '{profile_name}' saved successfully.")

def load_profile(profile_name):
    """Load a specific profile from the JSON file."""
    profiles = load_all_profiles()
    profile = profiles.get(profile_name)
    if profile:
        return profile.get("programs", [])
    return None

def launch_profile(programs):
    """Launch all programs in the profile list."""
    for program in programs:
        try:
            subprocess.Popen(program, shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch {program}: {e}")

def add_programs(program_list):
    """Add programs to the profile, asking if the user wants to add more."""
    while True:
        path = filedialog.askopenfilename(title="Select Program to Launch", filetypes=[("Executables", "*.exe"), ("All Files", "*.*")])
        if path and os.path.isfile(path):
            program_list.append(path)
            answer = messagebox.askyesno("Add another?", "Would you like to add another program to the profile?")
            if not answer:
                break
        else:
            break

def create_profile():
    """Create a new profile by selecting programs and saving them."""
    profile_name = profile_name_entry.get().strip()
    if not profile_name:
        messagebox.showerror("Error", "Profile name cannot be empty.")
        return

    profiles = load_all_profiles()
    if profile_name in profiles:
        messagebox.showerror("Error", f"Profile '{profile_name}' already exists.")
        return

    programs = []
    add_programs(programs)
    save_profile(profile_name, programs)

def edit_profile():
    """Edit an existing profile by adding more programs."""
    profile_name = profile_name_entry.get().strip()
    if not profile_name:
        messagebox.showerror("Error", "Please select a profile first.")
        return

    programs = load_profile(profile_name)
    if programs is None:
        messagebox.showerror("Error", f"Profile '{profile_name}' not found.")
        return

    add_programs(programs)
    save_profile(profile_name, programs)

def select_profile():
    """Select an existing profile from file dialog."""
    profiles = load_all_profiles()
    if not profiles:
        messagebox.showerror("Error", "No profiles found.")
        return None

    profile_name = filedialog.askstring("Select Profile", "Enter the name of the profile:")
    if profile_name and profile_name in profiles:
        profile_name_entry.delete(0, 'end')
        profile_name_entry.insert(0, profile_name)
        return profile_name
    else:
        messagebox.showerror("Error", "Profile not found.")
        return None

def launch_selected_profile():
    """Launch the selected profile's programs."""
    profile_name = profile_name_entry.get().strip()
    if not profile_name:
        messagebox.showerror("Error", "No profile selected.")
        return

    programs = load_profile(profile_name)
    if programs is not None:
        launch_profile(programs)

def list_profiles():
    """List all profiles in a message box."""
    profiles = load_all_profiles()
    if profiles:
        profile_names = "\n".join(profiles.keys())  # Create a list of profile names
        messagebox.showinfo("Profiles", f"Available Profiles:\n\n{profile_names}")
    else:
        messagebox.showinfo("Profiles", "No profiles found.")

def list_profile_contents():
    """List the contents of the selected profile."""
    profile_name = profile_name_entry.get().strip()
    if not profile_name:
        messagebox.showerror("Error", "Please select a profile first.")
        return

    programs = load_profile(profile_name)
    if programs is None:
        messagebox.showerror("Error", f"Profile '{profile_name}' not found.")
        return

    # Display program names (without paths) in a message box
    program_names = "\n".join([os.path.basename(program) for program in programs])
    messagebox.showinfo(f"Contents of {profile_name}", f"Programs in {profile_name}:\n\n{program_names}")

def setup_ui():
    """Set up the user interface."""
    global profile_name_entry

    root = Tk()
    root.title("Legion Launcher")

    # Create the menu bar
    menubar = Menu(root)
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="Create Profile", command=create_profile)
    file_menu.add_command(label="Edit Profile", command=edit_profile)
    file_menu.add_command(label="List Profiles", command=list_profiles)
    file_menu.add_command(label="List Profile Contents", command=list_profile_contents)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    Label(root, text="Profile Name:").grid(row=0, column=0, padx=10, pady=10)
    profile_name_entry = Entry(root, width=30)
    profile_name_entry.grid(row=0, column=1, padx=10, pady=10)

    Button(root, text="Launch Profile", command=launch_selected_profile).grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    setup_ui()
