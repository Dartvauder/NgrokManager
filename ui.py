import tkinter as tk
from tkinter import messagebox, ttk
from ngrok_manager import NgrokManager
import json
import webbrowser
from configparser import ConfigParser

with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

manager = None


class NgrokApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NgrokManager")

        self.config = ConfigParser()
        self.config.read('config.ini')

        self.language = self.config.get('general', 'language', fallback='en')
        self.t = translations.get(self.language, translations["en"])

        self.token_label = tk.Label(root, text="ngrok Token:")
        self.token_label.grid(row=0, column=0, padx=5, pady=5)

        self.token_entry = tk.Entry(root, width=30)
        self.token_entry.grid(row=0, column=1, padx=5, pady=5)
        self.token_entry.insert(0, self.config.get('general', 'ngrok_token', fallback=''))

        self.port_label = tk.Label(root, text=self.t["port"])
        self.port_label.grid(row=1, column=0, padx=5, pady=5)

        self.port_entry = tk.Entry(root)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)

        self.protocol_label = tk.Label(root, text="Protocol")
        self.protocol_label.grid(row=2, column=0, padx=5, pady=5)

        self.protocol_var = tk.StringVar(value="http")
        self.protocol_menu = tk.OptionMenu(root, self.protocol_var, "http", "tcp", "tls")
        self.protocol_menu.grid(row=2, column=1, padx=5, pady=5)

        self.domain_label = tk.Label(root, text="Domain (Optional):")
        self.domain_label.grid(row=3, column=0, padx=5, pady=5)

        self.domain_entry = tk.Entry(root, width=30)
        self.domain_entry.grid(row=3, column=1, padx=5, pady=5)

        self.language_label = tk.Label(root, text="Language")
        self.language_label.grid(row=4, column=0, padx=5, pady=5)

        self.language_var = tk.StringVar(value=self.language)
        self.language_menu = ttk.Combobox(root, textvariable=self.language_var, values=["en", "ru", "zh"])
        self.language_menu.grid(row=4, column=1, padx=5, pady=5)
        self.language_menu.bind("<<ComboboxSelected>>", self.change_language)

        self.create_button = tk.Button(root, text=self.t["create_tunnel"], command=self.create_tunnel)
        self.create_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.tunnel_list = tk.Listbox(root, width=50, height=10)
        self.tunnel_list.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.tunnel_list.bind("<Double-Button-1>", self.open_tunnel_url)

        self.delete_button = tk.Button(root, text=self.t["delete_selected_tunnel"], command=self.delete_tunnel)
        self.delete_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def change_language(self, event):
        self.language = self.language_var.get()
        self.t = translations.get(self.language, translations["en"])

        self.port_label.config(text=self.t["port"])
        self.create_button.config(text=self.t["create_tunnel"])
        self.delete_button.config(text=self.t["delete_selected_tunnel"])

        self.config.set('general', 'language', self.language)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def create_tunnel(self):
        token = self.token_entry.get()
        self.config.set('general', 'ngrok_token', token)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        global manager
        manager = NgrokManager(token)

        port = self.port_entry.get()
        proto = self.protocol_var.get()
        domain = self.domain_entry.get().strip()

        if port.isdigit():
            try:
                url = manager.start_tunnel(port, proto=proto, domain=domain)
                self.tunnel_list.insert(tk.END, f"{port} - {url}")
                messagebox.showinfo(self.t["success"], self.t["tunnel_created"] + url)
            except Exception as e:
                messagebox.showerror(self.t["error"], str(e))
        else:
            messagebox.showerror(self.t["error"], self.t["invalid_port"])

    def open_tunnel_url(self, event):
        selected = self.tunnel_list.curselection()
        if selected:
            url = self.tunnel_list.get(selected[0]).split(" - ")[1]
            webbrowser.open(url)

    def delete_tunnel(self):
        selected = self.tunnel_list.curselection()
        if selected:
            tunnel_info = self.tunnel_list.get(selected[0])
            tunnel_name = tunnel_info.split(" - ")[0]
            if manager.stop_tunnel(tunnel_name):
                self.tunnel_list.delete(selected[0])
                messagebox.showinfo(self.t["success"], self.t["tunnel_closed"])
            else:
                messagebox.showerror(self.t["error"], self.t["tunnel_not_found"])


root = tk.Tk()
app = NgrokApp(root)
root.mainloop()
