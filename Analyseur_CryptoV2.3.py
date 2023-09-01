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
        "per_page": 10,
        "page": 1,
        "ids": "bitcoin,ethereum,binancecoin,cardano,xrp,dogecoin,polkadot,uniswap,litecoin,chainlink"
    }
    response = session.get(url, params=params)
    data = response.json()

    if isinstance(data, dict) and "error_message" in data:
        raise ValueError(data["error_message"])

    if not isinstance(data, list):  
        # Afficher le contenu de la réponse pour un diagnostic plus détaillé
        raise ValueError(f"Réponse inattendue de l'API: {data}")

    return data

    if isinstance(data, dict) and "error_message" in data:
        raise ValueError(data["error_message"])
    
    if not isinstance(data, list):  
        raise ValueError("Réponse inattendue de l'API")

    return data

canvas_widget = None

def show_graph():
    global canvas_widget
    
    if canvas_widget:
        canvas_widget.destroy()

    try:
        data = fetch_data()
        names = [entry['symbol'].upper() for entry in data]
        percentages = [abs(entry['price_change_percentage_24h']) for entry in data]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(names, percentages, color='skyblue')

        ax.set_xlabel('Absolue Pourcentage de Changement en 24 heures')
        ax.set_ylabel('Cryptomonnaies')
        ax.set_title('Meilleures Cryptomonnaies à Acheter en Pourcentage')

        ax.invert_yaxis()

        for bar, percentage in zip(bars, percentages):
            ax.text(percentage, bar.get_y() + bar.get_height()/2, f"{percentage:.2f}%", color='blue', va='center')

        # Intégrer le graphique à l'interface tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        plt.tight_layout()
        plt.close(fig)  

    except ValueError as e:
        messagebox.showerror("Erreur", str(e))

root = tk.Tk()
root.title("ANALYSEUR CRYPTOMONNAIES AVHIRAL V2.3")

root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

btn_refresh = ttk.Button(root, text="ACTUALISER", command=show_graph)
btn_refresh.pack(pady=20)

show_graph()  

root.mainloop()
