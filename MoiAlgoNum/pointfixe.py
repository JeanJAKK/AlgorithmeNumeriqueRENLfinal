# ================================
# MODULE : point_fixe_module.py
# ================================

import sympy as sp
import numpy as np
from balayage import balayage  # <<< module externe pour le balayage d'intervalle

x = sp.Symbol('x')

# ----------------------------------------------------------
# 1. Génération automatique de g(x) candidates
# ----------------------------------------------------------
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
def point_fixe(g_expr, x0, eps=1e-5, max_iter=2000):
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
def solve_point_fixe(f_str, inf, supr, h, eps=1e-5, lambda_val=0.1):
    """Résout f(x)=0 par la méthode du point fixe + balayage."""

    try:
        f_expr = sp.sympify(f_str)
    except Exception as e:
        raise ValueError(f"Fonction invalide : {e}")

    f_num = sp.lambdify(x, f_expr, 'numpy')

    # Balayage
    interval = balayage(f_num, inf, supr, h)
    if interval is None:
        return None, "Aucun changement de signe détecté."

    # Génération et filtrage de g(x)
    g_candidates = generate_g_candidates(f_expr, lambda_val)
    safe_g = filter_safe_g(g_candidates, interval)
    if not safe_g:
        return None, "Aucune fonction g(x) valide pour le point fixe."

    # Point initial au milieu de l'intervalle détecté
    x0 = (interval[0] + interval[1]) / 2
    solution = point_fixe(safe_g[0], x0, eps)

    if solution is None:
        return None, "Échec de convergence."
    return solution, f"Intervalle utilisé : {interval}, g(x) choisie : {safe_g[0]}"