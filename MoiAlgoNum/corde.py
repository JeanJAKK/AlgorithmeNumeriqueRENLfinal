import sympy as sp
from _balayage import balayage


x = sp.Symbol('x')

# ----------------------------------------------------------
# 1. Lecture et préparation de f(x)
# ----------------------------------------------------------
def fonction():
    f_str = input("Expression de la fonction f(x) = ")
    try:
        f_sympy = sp.sympify(f_str)
    except Exception as e:
        print("❌ Fonction invalide :", e)
        exit()
    return f_sympy


# ----------------------------------------------------------
# 2. Lecture de la précision
# ----------------------------------------------------------
def precision():
    while True:
        try:
            eps = float(input("Précision (ex: 1e-6) : "))
            return abs(eps)
        except ValueError:
            print("❌ Valeur invalide.")


# ----------------------------------------------------------
# 3. Lecture des bornes
# ----------------------------------------------------------
def donnee():
    while True:
        try:
            a = float(input("Borne inférieure : "))
            b = float(input("Borne supérieure : "))

            if b <= a:
                print("⚠ La borne supérieure doit être > à la borne inférieure.")
                continue

            return a, b

        except ValueError:
            print("❌ Saisie invalide.")


# ----------------------------------------------------------
# 4. Dichotomie
# ----------------------------------------------------------
def cordesol():
    f_sympy = fonction()
    f = sp.lambdify(x, f_sympy, "numpy")   # fonction numérique

    def corde(x0, x1, eps):
        # Vérification du changement de signe
        if f(x0) * f(x1) > 0:
            print(f"⚠ Pas de changement de signe sur [{x0}, {x1}].")
            return None

        while abs(x1 - x0) > eps:
            x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
            x0, x1 = x1, x2
        return x1

    # Récupération des données
    a, b = donnee()
    eps = precision()
    a, b = balayage(f, a, b, h=0.1)
    sol = corde(a, b, eps)

    if sol is not None:
        print(f"\n✔ Racine approchée : {sol}")
        print(f"   f({sol}) = {f(sol)}")
    else:
        print("❌ Aucune solution trouvée sur cet intervalle.")