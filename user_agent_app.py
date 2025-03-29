import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk  # Modern themed widgets
from ttkbootstrap.constants import *
import random
import requests

# Predefined lists for demonstration (expand as needed)
DEVICE_TYPES = ['Android', 'Windows', 'Linux', 'macOS', 'iOS']
BROWSERS = {
    'Chrome': ['108.0.5359.145', '109.0.0.0', '110.0.0.0'],
    'Firefox': ['107.0', '108.0', '109.0'],
    'Edge': ['108.0.1462.54', '109.0.1518.70'],
    'Brave': ['1.25.68', '1.26.70'],
    'Safari': ['15.2', '15.3'],
    'Opera': ['93.0.4577.63', '94.0.0.0']
}

def generate_user_agent(device, browser):
    # Simulate realistic version numbers and OS info
    if device == 'Android':
        os_info = f"Android {random.randint(9,12)}.{random.randint(0,5)}"
    elif device == 'iOS':
        os_info = f"iOS {random.randint(14,17)}_{random.randint(0,5)}"
    elif device == 'Windows':
        os_info = f"Windows NT {random.choice(['10.0', '6.1'])}"
    elif device == 'macOS':
        os_info = f"Macintosh; Intel Mac OS X 10_{random.randint(12,15)}_{random.randint(0,9)}"
    elif device == 'Linux':
        os_info = "X11; Linux x86_64"
    else:
        os_info = "UnknownOS"
    version = random.choice(BROWSERS.get(browser, ['0.0']))
    ua = f"Mozilla/5.0 ({os_info}) AppleWebKit/537.36 (KHTML, like Gecko) {browser}/{version} Safari/537.36"
    return ua

def check_license(license_key):
    # Replace the URL with your live license API endpoint
    try:
        response = requests.post("https://yourdomain.com/api/check_license", json={"license_key": license_key})
        data = response.json()
        return data.get("valid", False)
    except Exception as e:
        print("License check error:", e)
        return False

def show_toast(root, message, duration=2000):
    toast = tk.Toplevel(root)
    toast.overrideredirect(True)
    # Position toast at center of the main window
    x = root.winfo_rootx() + root.winfo_width() // 2 - 125
    y = root.winfo_rooty() + root.winfo_height() // 2 - 25
    toast.geometry(f"250x50+{x}+{y}")
    lbl = ttk.Label(toast, text=message, bootstyle="inverse")
    lbl.pack(fill="both", expand=True)
    toast.after(duration, toast.destroy)

class UserAgentApp(ttk.Window):
    def __init__(self, license_key):
        super().__init__(themename="flatly")
        self.title("User Agent Generator")
        self.geometry("600x400")
        # Verify license
        if not check_license(license_key):
            messagebox.showerror("License Error", "Invalid or expired license.")
            self.destroy()
            return
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=20)
        frm.pack(expand=True, fill=BOTH)

        # Dropdowns for device type and browser
        ttk.Label(frm, text="Select Device Type:", font=("Helvetica", 12)).grid(row=0, column=0, pady=10, sticky="w")
        self.device_var = tk.StringVar(value=DEVICE_TYPES[0])
        device_menu = ttk.Combobox(frm, textvariable=self.device_var, values=DEVICE_TYPES, state="readonly")
        device_menu.grid(row=0, column=1, pady=10, sticky="ew")

        ttk.Label(frm, text="Select Browser:", font=("Helvetica", 12)).grid(row=1, column=0, pady=10, sticky="w")
        self.browser_var = tk.StringVar(value=list(BROWSERS.keys())[0])
        browser_menu = ttk.Combobox(frm, textvariable=self.browser_var, values=list(BROWSERS.keys()), state="readonly")
        browser_menu.grid(row=1, column=1, pady=10, sticky="ew")

        # Generate button
        gen_btn = ttk.Button(frm, text="Generate User Agent", command=self.on_generate, bootstyle=SUCCESS)
        gen_btn.grid(row=2, column=0, columnspan=2, pady=20)

        # Entry widget to display user agent
        self.ua_text = ttk.Entry(frm, font=("Courier", 12))
        self.ua_text.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # Copy button
        copy_btn = ttk.Button(frm, text="Copy to Clipboard", command=self.copy_to_clipboard, bootstyle=INFO)
        copy_btn.grid(row=4, column=0, columnspan=2, pady=10)

        frm.columnconfigure(1, weight=1)

    def on_generate(self):
        device = self.device_var.get()
        browser = self.browser_var.get()
        ua = generate_user_agent(device, browser)
        self.ua_text.delete(0, tk.END)
        self.ua_text.insert(0, ua)

    def copy_to_clipboard(self):
        ua = self.ua_text.get().strip()
        if ua:
            self.clipboard_clear()
            self.clipboard_append(ua)
            show_toast(self, "User agent copied!")

if __name__ == "__main__":
    # Replace with the actual license key or read from a config file
    LICENSE_KEY = "YOUR_LICENSE_KEY_HERE"
    app = UserAgentApp(LICENSE_KEY)
    app.mainloop()
