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
def dichosol():
    f_sympy = fonction()
    f = sp.lambdify(x, f_sympy, "numpy")   # fonction numérique

    def dicho(a, b, eps):
        # Vérification du changement de signe
        if f(a) * f(b) > 0:
            print(f"⚠ Pas de changement de signe sur [{a}, {b}].")
            return None

        while abs(b - a) > eps:
            m = (a + b) / 2

            if f(m) == 0:     # racine exacte
                return m

            if f(a) * f(m) < 0:
                b = m
            else:
                a = m

        return (a + b) / 2

    # Récupération des données
    a, b = donnee()
    eps = precision()
    a, b = balayage(f, a, b, h=0.1)
    sol = dicho(a, b, eps)

    if sol is not None:
        print(f"\n✔ Racine approchée : {sol}")
        print(f"   f({sol}) = {f(sol)}")
    else:
        print("❌ Aucune solution trouvée sur cet intervalle.")