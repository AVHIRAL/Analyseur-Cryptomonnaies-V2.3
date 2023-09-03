import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

session = requests.Session()
session.headers.update({
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
})

# Obtenir les données de CoinGecko
def fetch_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h",
        "market_category": "all",
        "localization": "false",
        "lang": "en"
    }

    response = session.get(url, params=params)
    data = response.json()

    if isinstance(data, dict) and "error_message" in data:
        raise ValueError(data["error_message"])

    if not isinstance(data, list):
        raise ValueError(f"Réponse inattendue de l'API: {data}")

    return data

canvas_widget = None


def show_graph():
    global canvas_widget

    if canvas_widget:
        canvas_widget.destroy()

    try:
        data = fetch_data()
        names = [entry['symbol'].upper() for entry in data]
        percentages = [entry['price_change_percentage_24h'] for entry in data]

        fig, ax = plt.subplots(figsize=(10, 6))

        colors = ['red' if p < 0 else 'skyblue' for p in percentages]
        bars = ax.barh(names, percentages, color=colors)

        ax.set_xlabel('Pourcentage de Changement en 24 heures')
        ax.set_ylabel('Cryptomonnaies')
        ax.set_title('Meilleures Cryptomonnaies à Acheter en Pourcentage')

        ax.invert_yaxis()

        for bar, percentage in zip(bars, percentages):
            color = 'black'
            if percentage < 0:
                offset = 0  # ajustez cette valeur selon vos besoins
                ha = 'right'
            else:
                offset = 0  # ajustez cette valeur selon vos besoins
                ha = 'left'
            ax.text(percentage + offset, bar.get_y() + bar.get_height() / 2, f"{percentage:.2f}%", color=color, va='center', ha=ha)

        # Intégrer le graphique à l'interface tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        plt.tight_layout()
        plt.close(fig)

    except ValueError as e:
        messagebox.showerror("Erreur", str(e))

root = tk.Tk()
root.title("ANALYSEUR CRYPTOMONNAIES AVHIRAL V2.7")

root.lift()
root.attributes('-topmost' , True)
root.after_idle(root.attributes , '-topmost' , False)

btn_refresh = ttk.Button(root , text="ACTUALISER" , command=show_graph)
btn_refresh.pack(pady=20)

show_graph()

root.mainloop()