# ================================
# PROGRAMME PRINCIPAL : point_fixe.py
# ================================
import sympy as sp
from pointfixe import ptfixe
from dichotomie import dichosol

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
        print("4 - Sécante")
        print("5 - Toutes les méthodes")
        print("0. Quitter")

        choix = input("\nChoisir une méthode : ")

        if choix == "1":
             ptfixe()
        elif choix == "2":
            dichosol()
            pass
        elif choix == "3":
            pass
        elif choix == "4":
           pass
        elif choix == "5":
            pass
        else:
            exit()

#================
#  main
#================
menu()
