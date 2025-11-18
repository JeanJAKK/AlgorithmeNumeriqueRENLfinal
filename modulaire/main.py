# ================================
# PROGRAMME PRINCIPAL
# ================================
import sympy as sp

from modulaire.newton_raphson import newsonsol
from pointfixe import ptfixe
from dichotomie import dichosol
from corde import cordesol

x = sp.Symbol('x')
global expr_str, inf, supr, h, eps,interval
#=========================
# Affichage menu
#=========================
def menu():
    while True:
        print("\n=== Résolution d'équation non linéaire ===\n")

        print("\nMéthodes disponibles :")
        print("1 - Point Fixe")
        print("2 - Dichotomie")
        print("3 - Newton-Raphson")
        print("4 - Corde")
        print("5 - Toutes les méthodes")
        print("0. Quitter")

        choix = input("\nChoisir une méthode : ")

        if choix == "1":
            ptfixe()
        elif choix == "2":
            dichosol()
        elif choix == "3":
            newsonsol()
        elif choix == "4":
            cordesol()
        elif choix == "5":
            ptfixe()
            dichosol()
            newsonsol()
            cordesol()
        else:
            exit()

#================
#  main
#================
menu()
