import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import threading
import time

class CryptocurrencyConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cryptocurrency Converter")
        self.geometry("600x400")
        self.configure(bg="#f0f0f0")

        self.create_widgets()

        # Start the thread to fetch live cryptocurrency prices
        self.live_update_thread = threading.Thread(target=self.live_update_prices)
        self.live_update_thread.daemon = True
        self.live_update_thread.start()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Cryptocurrency Converter", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333333")
        self.title_label.pack(pady=10)

        input_frame = tk.Frame(self, bg="#f0f0f0")
        input_frame.pack(pady=10)

        self.amount_label = tk.Label(input_frame, text="Amount:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
        self.amount_label.grid(row=0, column=0, padx=(10,5))
        self.amount_entry = tk.Entry(input_frame, font=("Arial", 12), bg="white", fg="#333333", relief=tk.FLAT, borderwidth=2)
        self.amount_entry.grid(row=0, column=1, padx=(0,10))
        self.amount_entry.insert(0, "Enter amount")
        self.amount_entry.bind("<FocusIn>", lambda event: self.amount_entry.delete(0, tk.END))
        self.amount_entry.bind("<FocusOut>", lambda event: self.amount_entry.insert(0, "Enter amount"))

        self.from_coin_label = tk.Label(input_frame, text="From Currency:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
        self.from_coin_label.grid(row=1, column=0, padx=(10,5), pady=(10,5))
        self.from_coin_var = tk.StringVar(self)
        self.from_coin_dropdown = ttk.Combobox(input_frame, textvariable=self.from_coin_var, font=("Arial", 12), state="readonly", width=20)
        self.from_coin_dropdown["values"] = ["BTC - Bitcoin", "ETH - Ethereum", "LTC - Litecoin", "XRP - Ripple", "DOGE - Dogecoin", "ADA - Cardano", "DOT - Polkadot", "LINK - Chainlink", "XLM - Stellar", "USDC - USD Coin"]
        self.from_coin_dropdown.grid(row=1, column=1, padx=(0,10), pady=(10,5))

        self.to_coin_label = tk.Label(input_frame, text="To Currency:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
        self.to_coin_label.grid(row=2, column=0, padx=(10,5), pady=(5,10))
        self.to_coin_var = tk.StringVar(self)
        self.to_coin_dropdown = ttk.Combobox(input_frame, textvariable=self.to_coin_var, font=("Arial", 12), state="readonly", width=20)
        self.to_coin_dropdown["values"] = ["BTC - Bitcoin", "ETH - Ethereum", "LTC - Litecoin", "XRP - Ripple", "DOGE - Dogecoin", "ADA - Cardano", "DOT - Polkadot", "LINK - Chainlink", "XLM - Stellar", "USDC - USD Coin"]
        self.to_coin_dropdown.grid(row=2, column=1, padx=(0,10), pady=(5,10))

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=10)

        self.convert_button = tk.Button(button_frame, text="Convert", command=self.convert, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, relief=tk.FLAT)
        self.convert_button.pack(side=tk.LEFT, padx=(10,5))

        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_entries, font=("Arial", 12), bg="#f44336", fg="white", padx=10, relief=tk.FLAT)
        self.clear_button.pack(side=tk.LEFT, padx=(5,10))

        self.result_label = tk.Label(self, text="", font=("Arial", 14, "bold"), fg="#4CAF50", bg="#f0f0f0")
        self.result_label.pack(pady=10)

        history_label = tk.Label(self, text="Conversion History", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333333")
        history_label.pack(pady=10)

        self.history_text = scrolledtext.ScrolledText(self, width=40, height=10, font=("Arial", 12))
        self.history_text.pack(padx=10, pady=5)

        self.status_bar = tk.Label(self, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#f0f0f0", fg="#333333")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def live_update_prices(self):
        while True:
            try:
                bitcoin_price = self.get_price("bitcoin")
                ethereum_price = self.get_price("ethereum")
                usd_coin_price = self.get_price("usd-coin")
                time.sleep(60)  # Update prices every minute
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update prices: {e}")

    def get_price(self, coin):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if coin not in data:
                messagebox.showerror("Error", f"Invalid cryptocurrency: {coin}")
                return None

            if "usd" not in data[coin]:
                messagebox.showerror("Error", f"Price data not available for {coin} against USD")
                return None

            return data[coin]["usd"]
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Network error: {e}")
            return None
        except ValueError:
            messagebox.showerror("Error", "Invalid response from the server")
            return None

    def calculate_conversion(self, amount, from_coin, to_coin):
        from_price = self.get_price(from_coin)
        to_price = self.get_price(to_coin)

        if from_price is None or to_price is None:
            return None

        converted_amount = (amount / from_price) * to_price
        return converted_amount

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            from_coin = self.from_coin_var.get().split(" - ")[1].lower()
            to_coin = self.to_coin_var.get().split(" - ")[1].lower()

            converted_amount = self.calculate_conversion(amount, from_coin, to_coin)
            if converted_amount is None:
                return

            fee = converted_amount * 0.05  # 5% fee
            converted_amount -= fee  # Deduct fee from the converted amount
            self.result_label.config(text=f"{amount} {from_coin.upper()} is equivalent to {converted_amount:.2f} {to_coin.upper()} (after 5% fee)", fg="#4CAF50")
            self.add_to_history(f"{amount} {from_coin.upper()} -> {converted_amount:.2f} {to_coin.upper()} (after 5% fee)")
            self.status_bar.config(text="Conversion successful", fg="#4CAF50")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            self.status_bar.config(text="Please enter a valid amount", fg="#f44336")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {e}")
            self.status_bar.config(text="Conversion failed", fg="#f44336")

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.from_coin_var.set("")
        self.to_coin_var.set("")
        self.result_label.config(text="")
        self.status_bar.config(text="Entries cleared", fg="#333333")

    def add_to_history(self, entry):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = CryptocurrencyConverter()
    app.mainloop()
