# ================================
# PROGRAMME PRINCIPAL : point_fixe.py
# ================================
import sympy as sp
from dichotomie import dicho
from pointfixe import solve_point_fixe
from balayage import balayage

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

        choix = input("Choisir une méthode : ")
        donnee()

        if choix == "1":
            solve_point_fixe(expr_str, inf, supr, h, eps, lambda_val=0.1)
        elif choix == "2":
            dicho(expr_str, interval, eps , max_iter=100)
        elif choix == "3":
            pass
        elif choix == "4":
           pass
        elif choix == "5":
            pass
        else:
            exit()
def donnee():
    # ----------------------------------------------------------
    # 1. Lecture et préparation de f(x)
    # ----------------------------------------------------------

    expr_str = input("Entrez la fonction f(x) : ")
    # Précision
    def precision():
        while True:
            try:
               eps = input("précision (exemple: 1e-7 ou 0.000001): ")
               return float(eps)
            except ValueError:
               print("La valeur n'est pas valide")

    eps = precision()
    try:
        f_expr = sp.sympify(expr_str)
    except Exception as e:
        print("❌ Erreur : fonction invalide.")
        print(e)
        exit()

    f_num = sp.lambdify(x, f_expr, 'numpy')

    # ----------------------------------------------------------
    # 2. Récupération des bornes et du pas
    # ----------------------------------------------------------
    while True:
        try:
            inf = float(input("Borne inférieure : "))
            supr = float(input("Borne supérieure : "))
            if supr <= inf:
                print("⚠ La borne supérieure doit être > à la borne inférieure.")
                continue

            h = float(input("Pas de balayage h : "))
            if h <= 0:
                print("⚠ Le pas doit être > 0.")
                continue
            break
        except ValueError:
            print("❌ Saisie invalide.")

    # Appel du module balayage
    interval = balayage(f_num, inf, supr, h)

    if interval is None:
        print("❌ Aucun changement de signe détecté.")
        exit()
    else:
        print(f"✔ Intervalle détecté : {interval}")
    return expr_str, inf, supr, h, eps,interval

#================
#  main
#================
menu()