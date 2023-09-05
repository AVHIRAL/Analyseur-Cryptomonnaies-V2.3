import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import numpy as np
from sklearn.linear_model import LinearRegression

# Simulons des données : 7 jours de pourcentage de changement et le 8ème jour comme cible
# Dans la pratique, vous devriez obtenir ces données de votre API ou d'une autre source.
data = [
    [1, 2, -1, 2, 3, -2, 1, 2.5],
    [2, -1, 2, 3, -2, 1, 2.5, 3],
    [-1, 2, 3, -2, 1, 2.5, 3, 2.8],
    # Ajoutez d'autres données ici
]

data = np.array(data)
X = data[:, :-1]  # Toutes les colonnes sauf la dernière
y = data[:, -1]  # Dernière colonne

# Entraîner un modèle de régression linéaire
model = LinearRegression().fit(X, y)

# Prévoir le pourcentage de changement pour demain
# Supposons que ces pourcentages viennent des 7 derniers jours
latest_data = np.array([2, 3, -2, 1, 2.5, 3, 2.8]).reshape(1, -1)
prediction = model.predict(latest_data)

print(f"Prédiction pour demain : {prediction[0]:.2f}%")

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

        names.insert(0, "PREDICTION")
        percentages.insert(0, prediction[0])
        
        fig, ax = plt.subplots(figsize=(10, 6))

        colors = ['red' if p < 0 else 'skyblue' for p in percentages]
        bars = ax.barh(names, percentages, color=colors)

        ax.set_xlabel('Pourcentage de Changement en 24 heures')
        ax.set_ylabel('Cryptomonnaies')
        ax.set_title('Meilleures Cryptomonnaies à Acheter en Pourcentage\nActualisation toutes les 5 minutes')

        ax.invert_yaxis()

        for bar, percentage in zip(bars, percentages):
            color = 'black'
            if percentage < 0:
                note = "↘"
                offset = 0
                ha = 'right'
            else:
                note = "↗"
                offset = 0
                ha = 'left'
            ax.text(percentage + offset, bar.get_y() + bar.get_height() / 2, f"{percentage:.2f}% ({note})", color=color, va='center', ha=ha, fontsize=8)

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        plt.tight_layout()
        plt.close(fig)

    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
    
    # Ajout de l'actualisation automatique toutes les 5 minutes (300 000 millisecondes)
    root.after(300000, show_graph)

root = tk.Tk()
root.title("ANALYSEUR CRYPTOMONNAIES AVHIRAL V3.0")

root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

btn_refresh = ttk.Button(root, text="ACTUALISER", command=show_graph)
btn_refresh.pack(pady=20)

show_graph()

root.mainloop()
