import sympy as sp
from balayage import balayage


def dicho(expr_str, interval, eps, max_iter=100):

    x = sp.Symbol('x')
    f = sp.lambdify(x, sp.sympify(expr_str), "numpy")

    # Si l’utilisateur n’a pas donné d’intervalle, balayage automatique
    if interval is None:
        intervs = balayage(expr_str)
        if not intervs:
            raise ValueError("Aucun intervalle valable trouvé (pas de changement de signe).")
        print("Intervalles trouvés :", intervs)
        interval = intervs[0]      # on prend le premier intervalle trouvé

    a, b = interval

    if f(a) * f(b) > 0:
        raise ValueError("L’intervalle choisi ne respecte pas f(a)*f(b) < 0.")

    print(f"Intervalle utilisé : [{a}, {b}]")

    # --- Algorithme de dichotomie ---
    for i in range(max_iter):
        m = (a + b) / 2
        fm = f(m)

        if abs(fm) < eps or (b - a)/2 < eps:
            return m

        if f(a) * fm < 0:
            b = m
        else:
            a = m

    return m  # meilleure approximation après max_iter