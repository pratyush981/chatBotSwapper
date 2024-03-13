import tkinter as tk
from tkinter import ttk
import requests

class CryptoSwapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Swapper")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#263D42")
        self.style.configure("TLabel", background="#263D42", foreground="white", font=("Helvetica", 14))
        self.style.configure("TButton", background="#FF5733", foreground="white", font=("Helvetica", 12, "bold"))
        self.style.map("TButton", background=[("active", "#EA7A61")])

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0)

        ttk.Label(main_frame, text="Swap From:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.crypto_from_var = tk.StringVar()
        self.crypto_from_var.set("BTC")
        crypto_from_menu = ttk.Combobox(main_frame, textvariable=self.crypto_from_var, values=self.get_crypto_list(), state="readonly")
        crypto_from_menu.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(main_frame, text="Swap To:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.crypto_to_var = tk.StringVar()
        self.crypto_to_var.set("ETH")
        crypto_to_menu = ttk.Combobox(main_frame, textvariable=self.crypto_to_var, values=self.get_crypto_list(), state="readonly")
        crypto_to_menu.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(main_frame, text="Enter Amount to Swap:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(main_frame, width=15, font=("Helvetica", 12))
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(main_frame, text="Swap", command=self.swap_crypto).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.result_label = ttk.Label(main_frame, text="", font=("Helvetica", 14))
        self.result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def get_crypto_list(self):
        # Fetching the list of supported cryptocurrencies from a different API
        response = requests.get("https://api.coinlore.net/api/tickers/")
        data = response.json()
        crypto_list = [crypto['symbol'].upper() for crypto in data['data']]
        return crypto_list

    def get_current_price(self, crypto_symbol):
        # Fetching the current price of a cryptocurrency from a different API
        response = requests.get(f"https://api.coinlore.net/api/ticker/?id={crypto_symbol}")
        data = response.json()
        if data['info']['coins_num'] > 0:
            return float(data['data'][0]['price_usd'])
        else:
            return None

    def swap_crypto(self):
        crypto_from = self.crypto_from_var.get()
        crypto_to = self.crypto_to_var.get()
        amount = self.amount_entry.get()

        if not amount:
            self.result_label.config(text="Please enter the amount to swap.", foreground="red")
            return

        try:
            amount = float(amount)
        except ValueError:
            self.result_label.config(text="Please enter a valid amount.", foreground="red")
            return

        price_from = self.get_current_price(crypto_from)
        price_to = self.get_current_price(crypto_to)

        if price_from is not None and price_to is not None:
            amount_to_receive = (amount * price_from) / price_to
            self.result_label.config(text=f"Swapped {amount:.2f} {crypto_from} to {amount_to_receive:.2f} {crypto_to}", foreground="green")
        else:
            self.result_label.config(text="Failed to fetch current prices. Please try again later.", foreground="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoSwapApp(root)
    root.mainloop()
