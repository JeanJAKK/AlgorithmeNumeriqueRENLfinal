# ================================
# MODULE : point_fixe_module.py
# ================================

import sympy as sp
import numpy as np
from _balayage import balayage

# ----------------------------------------------------------
# 1. Lecture et préparation de f(x)
# ----------------------------------------------------------
x = sp.Symbol('x')

def fonction():
    global expr_str, f_sym
    expr_str = input("Expression de la fonction (ex: x**2 - 1): ")
    try:
        f_sym = sp.sympify(expr_str)
    except Exception as e:
        print("❌ Erreur : fonction invalide.")
        print(e)
        exit()

    f_num = sp.lambdify(x, f_sym, 'numpy')
    return f_num

 # Précision
def precision():
    while True:
        try:
           eps = input("précision (exemple: 1e-7 ou 0.000001): ")
           return float(eps)
        except ValueError:
           print("La valeur n'est pas valide")

# ----------------------------------------------------------
# 2. Récupération des bornes et du pas
# ----------------------------------------------------------
def donnee():
    while True:
        try:
            inf = float(input("Borne inférieure : "))
            supr = float(input("Borne supérieure : "))

            if supr <= inf:
                print("⚠ La borne supérieure doit être > à la borne inférieure.")
                continue

            return inf, supr  # ← retourne directement les valeurs

        except ValueError:
            print("❌ Saisie invalide.")

#------------------------------
# pas
#------------------------------
def pas():
    while True:
        try:
            h = float(input("Pas de balayage h : "))
            if h <= 0:
                print("⚠ Le pas doit être > 0.")
                continue
            return h
        except ValueError:
            print("Saisie invalide.")

def ptfixe():
    # ← on récupère les valeurs ici
    f_num = fonction()
    inf, supr = donnee()
    h = pas()
    eps = precision()

    # ============================================================
    # 1. Génération automatique de g(x) candidates
    # ============================================================
    def generate_g_candidates(expr_str, lambda_val=0.1):
        g_candidates_expr = []

        # A) g(x) = x - λ f(x)
        g_candidates_expr.append(x - lambda_val * expr_str)

        # B) Essayer d’isoler x dans f(x)=0
        try:
            sols = sp.solve(expr_str, x)
            for s in sols:
                g_candidates_expr.append(sp.simplify(s))
        except Exception:
            pass

        # Nettoyage
        g_candidates_expr = [sp.simplify(g) for g in g_candidates_expr]
        return g_candidates_expr

    # ----------------------------------------------------------
    # 2. Filtrage des g(x) via g'(x)
    # ----------------------------------------------------------
    def is_safe_g(g_expr, interval, num_points=200):
        try:
            g_num = sp.lambdify(x, g_expr, 'numpy')
            g_prime_expr = sp.diff(g_expr, x)
            g_prime_num = sp.lambdify(x, g_prime_expr, 'numpy')
            xs = np.linspace(interval[0], interval[1], num_points)
            for xi in xs:
                gi = g_num(xi)
                dpi = g_prime_num(xi)
                if np.isnan(gi) or np.isnan(dpi) or np.isinf(gi) or np.isinf(dpi):
                    return False
                if abs(dpi) >= 1:  # condition de convergence
                    return False
            return True
        except Exception:
            return False

    def filter_safe_g(g_candidates_expr, interval):
        return [g for g in g_candidates_expr if is_safe_g(g, interval)]

    # ----------------------------------------------------------
    # 3. Méthode du point fixe
    # ----------------------------------------------------------
    def point_fixe(g_expr, x0, eps , max_iter=2000):
        g_num = sp.lambdify(x, g_expr, 'numpy')
        for _ in range(max_iter):
            try:
                x1 = g_num(x0)
                if np.isnan(x1) or np.isinf(x1):
                    return None
                if abs(x1 - x0) < eps:
                    return x1
                x0 = x1
            except Exception:
                return None
        return None

    # ----------------------------------------------------------
    # 4. Fonction principale du module
    # ----------------------------------------------------------
    def solve_point_fixe(f_num, inf, supr, h, eps ):

        # Appel du module balayage
        interval = balayage(f_num, inf, supr, h)
        if interval is None:
            print("\n❌ Aucun changement de signe détecté.")
            exit()
        else:
            print(f"\n✔ Intervalle détecté : [{interval[0]}, {interval[1]}]")

        # Génération et filtrage de g(x)
        g_candidates = generate_g_candidates(f_sym, lambda_val=0.1)
        safe_g = filter_safe_g(g_candidates, interval)
        if not safe_g:
            return None, "\nAucune fonction g(x) valide pour le point fixe."


        # Point initial au milieu de l'intervalle détecté
        x0 = (interval[0] + interval[1]) / 2
        solution = point_fixe(safe_g[0], x0, eps)

        if solution is None:
            return None, "Échec de convergence."
        a = f"\nLa fonction g(x) choisie : {safe_g[0]}"
        b = f"🎯 Solution approchée : x ≈ {solution}"
        print(a)
        print(b)
        return None

    solve_point_fixe(f_num, inf, supr, h, eps)