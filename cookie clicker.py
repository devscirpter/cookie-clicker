
import tkinter as tk
from tkinter import ttk
import json
import os

class CookieClicker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cookie Clicker")
        self.window.geometry("400x500")
        
        self.cookies = 0
        self.multiplier = 1
        self.auto_clickers = 0
        
        # Load saved data if exists
        self.load_game()
        
        # Cookie counter
        self.counter_label = ttk.Label(self.window, text=f"Cookies: {self.cookies}", font=("Arial", 20))
        self.counter_label.pack(pady=20)
        
        # Cookie button
        self.cookie_image = tk.PhotoImage(file="cookie.png") if os.path.exists("cookie.png") else None
        self.cookie_button = ttk.Button(
            self.window,
            text="Click Me!" if self.cookie_image is None else "",
            image=self.cookie_image,
            compound="center",
            command=self.click_cookie
        )
        self.cookie_button.pack(pady=20)
        
        # Upgrade buttons
        self.multiplier_button = ttk.Button(
            self.window,
            text=f"Buy Multiplier (Cost: {self.get_multiplier_cost()} cookies)",
            command=self.buy_multiplier
        )
        self.multiplier_button.pack(pady=10)
        
        self.auto_clicker_button = ttk.Button(
            self.window,
            text=f"Buy Auto-Clicker (Cost: {self.get_auto_clicker_cost()} cookies)",
            command=self.buy_auto_clicker
        )
        self.auto_clicker_button.pack(pady=10)
        
        # Stats
        self.stats_label = ttk.Label(
            self.window,
            text=f"Multiplier: x{self.multiplier}\nAuto-Clickers: {self.auto_clickers}"
        )
        self.stats_label.pack(pady=20)
        
        # Save button
        self.save_button = ttk.Button(self.window, text="Save Game", command=self.save_game)
        self.save_button.pack(pady=10)
        
        # Start auto-clicker timer
        self.auto_click()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def click_cookie(self):
        self.cookies += 1 * self.multiplier
        self.update_labels()
    
    def get_multiplier_cost(self):
        return 10 * (self.multiplier + 1)
    
    def get_auto_clicker_cost(self):
        return 50 * (self.auto_clickers + 1)
    
    def buy_multiplier(self):
        cost = self.get_multiplier_cost()
        if self.cookies >= cost:
            self.cookies -= cost
            self.multiplier += 1
            self.update_labels()
    
    def buy_auto_clicker(self):
        cost = self.get_auto_clicker_cost()
        if self.cookies >= cost:
            self.cookies -= cost
            self.auto_clickers += 1
            self.update_labels()
    
    def auto_click(self):
        if self.auto_clickers > 0:
            self.cookies += self.auto_clickers * self.multiplier
            self.update_labels()
        self.window.after(1000, self.auto_click)
    
    def update_labels(self):
        self.counter_label.config(text=f"Cookies: {self.cookies}")
        self.multiplier_button.config(text=f"Buy Multiplier (Cost: {self.get_multiplier_cost()} cookies)")
        self.auto_clicker_button.config(text=f"Buy Auto-Clicker (Cost: {self.get_auto_clicker_cost()} cookies)")
        self.stats_label.config(text=f"Multiplier: x{self.multiplier}\nAuto-Clickers: {self.auto_clickers}")
    
    def save_game(self):
        game_data = {
            "cookies": self.cookies,
            "multiplier": self.multiplier,
            "auto_clickers": self.auto_clickers
        }
        with open("cookie_save.json", "w") as f:
            json.dump(game_data, f)
    
    def load_game(self):
        try:
            with open("cookie_save.json", "r") as f:
                game_data = json.load(f)
                self.cookies = game_data["cookies"]
                self.multiplier = game_data["multiplier"]
                self.auto_clickers = game_data["auto_clickers"]
        except FileNotFoundError:
            pass
    
    def on_closing(self):
        self.save_game()
        self.window.destroy()

if __name__ == "__main__":
    game = CookieClicker()

