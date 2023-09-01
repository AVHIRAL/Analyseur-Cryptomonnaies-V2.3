# Analyseur-Cryptomonnaies-V2.3

Analyseur Cryptomonnaies afin de classé par pourcentage la meilleur monnaies à investir.L'Analyseur Cryptomonnaies est une application GUI conçue avec tkinter qui interroge l'API CoinGecko pour obtenir des informations sur les 10 principales cryptomonnaies (par capitalisation boursière). Il classe ces cryptomonnaies en fonction de leur pourcentage de changement de prix absolu au cours des dernières 24 heures et affiche ces données sous forme de graphique à barres horizontales.

Caractéristiques:

    Interrogation de l'API CoinGecko: L'application utilise la bibliothèque requests pour interroger l'API et récupérer les données des cryptomonnaies.

    Affichage graphique: L'application utilise matplotlib pour générer un graphique à barres horizontales des cryptomonnaies, classées en fonction du pourcentage de changement de prix absolu sur 24 heures.

    Interface Utilisateur: La GUI a un bouton "ACTUALISER" qui permet à l'utilisateur de rafraîchir les données et de mettre à jour le graphique.

Comment l'utiliser:

    Lancez le script.
    L'application affichera automatiquement le graphique pour les 10 principales cryptomonnaies.
    Utilisez le bouton "ACTUALISER" pour mettre à jour le graphique avec les données les plus récentes.

Dépendances:

    tkinter
    matplotlib
    requests

Note: Assurez-vous d'avoir accès à l'API CoinGecko et respectez les limites d'utilisation de l'API lors de l'utilisation de cette application.

Ce projet a été inspiré par l'idée de classer les cryptomonnaies en fonction de leur potentiel d'investissement, mais veuillez noter que les résultats ne doivent pas être considérés comme des conseils financiers. Investissez toujours prudemment et faites vos propres recherches.
