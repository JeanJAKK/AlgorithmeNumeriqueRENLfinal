import sympy as sp

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
# 3. Lecture de la première estimation de la solution
# ----------------------------------------------------------
def initial():
    while True:
        try:
            xa = float(input("Initialisation de x : "))
            return xa
        except ValueError:
            print("Saisie invalide.")

# ----------------------------------------------------------
# 4. Newton-Raphsonn
# ----------------------------------------------------------
def newsonsol():
    f_sympy = fonction()
    f_prime = sp.diff(f_sympy, x)
    f_prime_num = sp.lambdify(x, f_prime)
    f = sp.lambdify(x, f_sympy, "numpy")   # fonction numérique

    def newson(x0, eps):
        x1 = x0 - f(x0) / f_prime_num(x0)
        while abs(x1 - x0) > eps:
            x0 = x1
            x1 = x0 - f(x0) / f_prime_num(x0)
        return x1

    # Récupération des données
    xa = initial()
    eps = precision()
    sol = newson(xa, eps)

    if sol is not None:
        print(f"\n✔ Racine approchée : {sol}")
        print(f"   f({sol}) = {f(sol)}")
    else:
        print("❌ Aucune solution trouvée sur cet intervalle.")