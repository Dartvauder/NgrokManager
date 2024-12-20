import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
from TechnicalFiles.ngrok_manager import NgrokManager
import json
import webbrowser
from configparser import ConfigParser
import subprocess

with open("TechnicalFiles/translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

manager = None


class NgrokApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NgrokManager")

        self.config = ConfigParser()
        self.config.read('TechnicalFiles/config.ini')

        self.language = self.config.get('general', 'language', fallback='en')
        self.theme = self.config.get('general', 'theme', fallback='dark')
        self.t = translations.get(self.language, translations["en"])

        self.root.configure(bg="#2e2e2e" if self.theme == "dark" else "#ffffff")

        self.token_label = tk.Label(root, text=self.t["ngrok_token"], bg=self.root["bg"],
                                    fg="#ffffff" if self.theme == "dark" else "#000000")
        self.token_label.grid(row=0, column=0, padx=5, pady=5)

        self.token_entry = tk.Entry(root, width=30)
        self.token_entry.grid(row=0, column=1, padx=5, pady=5)
        self.token_entry.insert(0, self.config.get('general', 'ngrok_token', fallback=''))

        self.port_label = tk.Label(root, text=self.t["port"], bg=self.root["bg"],
                                   fg="#ffffff" if self.theme == "dark" else "#000000")
        self.port_label.grid(row=1, column=0, padx=5, pady=5)

        self.port_entry = tk.Entry(root)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)

        self.protocol_label = tk.Label(root, text=self.t["protocol"], bg=self.root["bg"],
                                       fg="#ffffff" if self.theme == "dark" else "#000000")
        self.protocol_label.grid(row=2, column=0, padx=5, pady=5)

        self.protocol_var = tk.StringVar(value="http")
        self.protocol_menu = tk.OptionMenu(root, self.protocol_var, "http", "tcp", "tls")
        self.protocol_menu.config(bg=self.root["bg"], fg="#ffffff" if self.theme == "dark" else "#000000")
        self.protocol_menu.grid(row=2, column=1, padx=5, pady=5)

        self.domain_label = tk.Label(root, text=self.t["domain_optional"], bg=self.root["bg"],
                                     fg="#ffffff" if self.theme == "dark" else "#000000")
        self.domain_label.grid(row=3, column=0, padx=5, pady=5)

        self.domain_entry = tk.Entry(root, width=30)
        self.domain_entry.grid(row=3, column=1, padx=5, pady=5)

        self.login_label = tk.Label(root, text=self.t["login_optional"], bg=self.root["bg"],
                                    fg="#ffffff" if self.theme == "dark" else "#000000")
        self.login_label.grid(row=4, column=0, padx=5, pady=5)

        self.login_entry = tk.Entry(root, width=30)
        self.login_entry.grid(row=4, column=1, padx=5, pady=5)

        self.password_label = tk.Label(root, text=self.t["password_optional"], bg=self.root["bg"],
                                       fg="#ffffff" if self.theme == "dark" else "#000000")
        self.password_label.grid(row=5, column=0, padx=5, pady=5)

        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.grid(row=5, column=1, padx=5, pady=5)

        self.region = self.config.get('general', 'region', fallback='us')
        self.region_label = tk.Label(root, text=self.t["region"], bg=self.root["bg"],
                                     fg="#ffffff" if self.theme == "dark" else "#000000")
        self.region_label.grid(row=6, column=0, padx=5, pady=5)

        self.region_var = tk.StringVar(value=self.region)
        self.region_menu = ttk.Combobox(root, textvariable=self.region_var,
                                        values=["us", "eu", "ap", "au", "sa", "jp", "in"])
        self.region_menu.grid(row=6, column=1, padx=5, pady=5)
        self.region_menu.bind("<<ComboboxSelected>>", self.change_region)

        self.create_button = tk.Button(root, text=self.t["create_tunnel"], command=self.create_tunnel,
                                       bg="#444444" if self.theme == "dark" else "#e0e0e0",
                                       fg="#ffffff" if self.theme == "dark" else "#000000")
        self.create_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        self.ssh_button = tk.Button(root, text=self.t["create_ssh_tunnel"], command=self.create_ssh_tunnel,
                                    bg="#444444" if self.theme == "dark" else "#e0e0e0",
                                    fg="#ffffff" if self.theme == "dark" else "#000000")
        self.ssh_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        self.web_inspect_button = tk.Button(root, text="Web Inspection Interface", command=self.open_web_inspection,
                                            bg="#444444" if self.theme == "dark" else "#e0e0e0",
                                            fg="#ffffff" if self.theme == "dark" else "#000000")
        self.web_inspect_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        self.save_button = tk.Button(root, text=self.t["save_config"], command=self.save_config,
                                     bg="#444444" if self.theme == "dark" else "#e0e0e0",
                                     fg="#ffffff" if self.theme == "dark" else "#000000")
        self.save_button.grid(row=10, column=0, padx=5, pady=5)

        self.load_button = tk.Button(root, text=self.t["load_config"], command=self.load_config,
                                     bg="#444444" if self.theme == "dark" else "#e0e0e0",
                                     fg="#ffffff" if self.theme == "dark" else "#000000")
        self.load_button.grid(row=10, column=1, padx=5, pady=5)

        self.language_label = tk.Label(root, text=self.t["language"], bg=self.root["bg"],
                                       fg="#ffffff" if self.theme == "dark" else "#000000")
        self.language_label.grid(row=11, column=0, padx=5, pady=5)

        self.language_var = tk.StringVar(value=self.language)
        self.language_menu = ttk.Combobox(root, textvariable=self.language_var, values=["en", "ru", "zh"])
        self.language_menu.grid(row=11, column=1, padx=5, pady=5)
        self.language_menu.bind("<<ComboboxSelected>>", self.change_language)

        self.theme_label = tk.Label(root, text=self.t["theme"], bg=self.root["bg"],
                                    fg="#ffffff" if self.theme == "dark" else "#000000")
        self.theme_label.grid(row=12, column=0, padx=5, pady=5)

        self.theme_var = tk.StringVar(value=self.theme)
        self.theme_menu = ttk.Combobox(root, textvariable=self.theme_var, values=["dark", "light"])
        self.theme_menu.grid(row=12, column=1, padx=5, pady=5)
        self.theme_menu.bind("<<ComboboxSelected>>", self.change_theme)

        self.tunnel_list = tk.Listbox(root, width=50, height=10, bg="#333333" if self.theme == "dark" else "#ffffff",
                                      fg="#ffffff" if self.theme == "dark" else "#000000")
        self.tunnel_list.grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.tunnel_list.bind("<Double-Button-1>", self.open_tunnel_url)

        self.delete_button = tk.Button(root, text=self.t["delete_selected_tunnel"], command=self.delete_tunnel,
                                       bg="#444444" if self.theme == "dark" else "#e0e0e0",
                                       fg="#ffffff" if self.theme == "dark" else "#000000")
        self.delete_button.grid(row=14, column=0, columnspan=2, padx=5, pady=5)

    def open_web_inspection(self):
        webbrowser.open("http://localhost:4040")

    def change_region(self, event=None):
        self.region = self.region_var.get()
        self.config.set('general', 'region', self.region)
        with open('TechnicalFiles/config.ini', 'w') as configfile:
            self.config.write(configfile)

    def create_tunnel(self):
        token = self.token_entry.get()
        region = self.region_var.get()

        self.config.set('general', 'ngrok_token', token)
        with open('TechnicalFiles/config.ini', 'w') as configfile:
            self.config.write(configfile)

        self.config.set('general', 'region', region)
        with open('TechnicalFiles/config.ini', 'w') as configfile:
            self.config.write(configfile)

        global manager
        manager = NgrokManager(token, region)

        port = self.port_entry.get()
        proto = self.protocol_var.get()
        domain = self.domain_entry.get().strip()
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        if port.isdigit():
            try:
                url = manager.start_tunnel(port, proto=proto, domain=domain,
                                           auth=f"{login}:{password}" if login and password else None)
                self.tunnel_list.insert(tk.END, f"{port} - {url}")
                messagebox.showinfo(self.t["success"], self.t["tunnel_created"] + url)
            except Exception as e:
                messagebox.showerror(self.t["error"], str(e))
        else:
            messagebox.showerror(self.t["error"], self.t["invalid_port"])

    def create_ssh_tunnel(self):
        remote_port = simpledialog.askstring(self.t["remote_port"], self.t["enter_remote_port"])
        local_port = simpledialog.askstring(self.t["local_port"], self.t["enter_local_port"])

        if remote_port.isdigit() and local_port.isdigit():
            command = f"ssh -R {remote_port}:localhost:{local_port} v2@connect.ngrok-agent.com http"
            try:
                subprocess.Popen(command, shell=True)
                messagebox.showinfo(self.t["success"], self.t["ssh_tunnel_started"])
            except Exception as e:
                messagebox.showerror(self.t["error"], str(e))
        else:
            messagebox.showerror(self.t["error"], self.t["invalid_port"])

    def delete_tunnel(self):
        selected = self.tunnel_list.curselection()
        if selected:
            tunnel_info = self.tunnel_list.get(selected)
            port = tunnel_info.split(" - ")[0]
            try:
                manager.stop_tunnel(port)
                self.tunnel_list.delete(selected)
                messagebox.showinfo(self.t["success"], self.t["tunnel_closed"])
            except Exception as e:
                messagebox.showerror(self.t["error"], str(e))
        else:
            messagebox.showerror(self.t["error"], self.t["tunnel_not_found"])

    def open_tunnel_url(self, event):
        selected = self.tunnel_list.curselection()
        if selected:
            tunnel_info = self.tunnel_list.get(selected)
            url = tunnel_info.split(" - ")[1]
            webbrowser.open(url)

    def change_language(self, event=None):
        self.language = self.language_var.get()
        self.config.set('general', 'language', self.language)
        with open('TechnicalFiles/config.ini', 'w') as configfile:
            self.config.write(configfile)

        self.t = translations.get(self.language, translations["en"])
        self.update_labels()

    def change_theme(self, event=None):
        self.theme = self.theme_var.get()
        self.config.set('general', 'theme', self.theme)
        with open('TechnicalFiles/config.ini', 'w') as configfile:
            self.config.write(configfile)

        bg_color = "#2e2e2e" if self.theme == "dark" else "#ffffff"
        fg_color = "#ffffff" if self.theme == "dark" else "#000000"

        self.root.configure(bg=bg_color)
        self.token_label.config(bg=bg_color, fg=fg_color)
        self.port_label.config(bg=bg_color, fg=fg_color)
        self.protocol_label.config(bg=bg_color, fg=fg_color)
        self.domain_label.config(bg=bg_color, fg=fg_color)
        self.login_label.config(bg=bg_color, fg=fg_color)
        self.password_label.config(bg=bg_color, fg=fg_color)
        self.language_label.config(bg=bg_color, fg=fg_color)
        self.theme_label.config(bg=bg_color, fg=fg_color)
        self.create_button.config(bg="#444444" if self.theme == "dark" else "#e0e0e0", fg=fg_color)
        self.delete_button.config(bg="#444444" if self.theme == "dark" else "#e0e0e0", fg=fg_color)
        self.tunnel_list.config(bg="#333333" if self.theme == "dark" else "#ffffff", fg=fg_color)

    def update_labels(self):
        self.token_label.config(text=self.t["ngrok_token"])
        self.port_label.config(text=self.t["port"])
        self.protocol_label.config(text=self.t["protocol"])
        self.domain_label.config(text=self.t["domain_optional"])
        self.login_label.config(text=self.t["login_optional"])
        self.password_label.config(text=self.t["password_optional"])
        self.language_label.config(text=self.t["language"])
        self.theme_label.config(text=self.t["theme"])
        self.create_button.config(text=self.t["create_tunnel"])
        self.delete_button.config(text=self.t["delete_selected_tunnel"])

    def save_config(self):
        tunnel_data = {
            "token": self.token_entry.get(),
            "port": self.port_entry.get(),
            "protocol": self.protocol_var.get(),
            "domain": self.domain_entry.get(),
            "login": self.login_entry.get(),
            "password": self.password_entry.get(),
            "region": self.region_var.get()
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(tunnel_data, file)
            messagebox.showinfo(self.t["success"], self.t["config_saved"])

    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                tunnel_data = json.load(file)
                self.token_entry.delete(0, tk.END)
                self.token_entry.insert(0, tunnel_data["token"])
                self.port_entry.delete(0, tk.END)
                self.port_entry.insert(0, tunnel_data["port"])
                self.protocol_var.set(tunnel_data["protocol"])
                self.domain_entry.delete(0, tk.END)
                self.domain_entry.insert(0, tunnel_data["domain"])
                self.login_entry.delete(0, tk.END)
                self.login_entry.insert(0, tunnel_data["login"])
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, tunnel_data["password"])
                self.region_var.set(tunnel_data["region"])
            messagebox.showinfo(self.t["success"], self.t["config_loaded"])
