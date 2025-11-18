# ================================
# PROGRAMME PRINCIPAL
# ================================
import sympy as sp
import numpy as np

# Déclaration explicite des variables globales pour qu'elles soient accessibles et modifiables
global f_sympy, a, b, eps, h, x0_newton # J'ajoute 'h' et 'x0_newton' pour la clarté

# Initialisation (bien que l'affectation soit faite dans menu(), c'est une bonne pratique)
f_sympy = None
a = None
b = None
eps = None
h = None
x0_newton = None
x = sp.Symbol('x') # La variable symbolique doit être globale/accessible


#====================================================================
# Affichage menu et appel des fonctions de récupération des données
#====================================================================
def menu():
    global f_sympy, a, b, eps, h, x0_newton

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

        if choix == "0":
             exit()

        # 1. Récupération des données POUR TOUTES LES MÉTHODES
        f_sympy = fonction()
        inf, supr = donnee()
        h = pas()

        # 2. Balayage : recherche d'un intervalle de changement de signe [a, b]
        f_num_balayage = sp.lambdify(x, f_sympy, 'numpy')
        resultat_balayage = balayage(f_num_balayage, inf, supr, h)

        if resultat_balayage is None:
            print("\n❌ Aucun intervalle de changement de signe détecté. Veuillez modifier les bornes ou le pas.")
            # On recommence la boucle pour un nouveau choix/saisie
            continue
        else:
            a, b = resultat_balayage
            print(f"\n✔ Intervalle détecté pour la racine : [{a}, {b}]")

        # 3. Récupération de la précision
        eps = precision()

        # 4. Pour Newton-Raphson, on demande un point initial, souvent dans [a, b]
        if choix == "3" or choix == "5":
            print(f"\n--- Initialisation de Newton (idéalement dans [{a}, {b}]) ---")
            x0_newton = initial()


        # 5. Appel des solveurs avec les variables globales
        if choix == "1":
            ptfixe()
        elif choix == "2":
            dichosol()
        elif choix == "3":
            newsonsol(x0_newton) # Passer l'initialisation à Newton
        elif choix == "4":
            cordesol()
        elif choix == "5":
            ptfixe()
            dichosol()
            newsonsol(x0_newton) # Passer l'initialisation à Newton
            cordesol()
        else:
            # Cette branche ne devrait pas être atteinte si choix="0" est géré au début
            exit()


#================
#  main
#================
# Lancement du programme
# La fonction menu() gère maintenant la boucle et la récupération des données.
# menu() # Décommenter pour exécuter le programme


# ================================
# MODULE : _balayage.py
# ================================

def balayage(f, inf, supr, h):

    x0 = inf

    # Assurez-vous que les bornes ne sont pas identiques
    if inf == supr:
        return None

    # Ajustement pour s'assurer que l'on vérifie tous les intervalles jusqu'à supr
    while x0 < supr:
        # Assurer que le dernier point ne dépasse pas supr
        x_next = min(x0 + h, supr)

        try:
            y1 = f(x0)
            y2 = f(x_next)

            # Ignore NaN, infinies
            if np.isnan(y1) or np.isnan(y2) or np.isinf(y1) or np.isinf(y2):
                x0 += h
                continue

            if y1 * y2 < 0:   # changement de signe
                return x0, x_next

        except Exception:
            # En cas d’erreur f(x) → passer au point suivant
            pass

        x0 += h

        # S'assurer qu'on sort bien de la boucle si x0 a dépassé supr
        if x0 >= supr:
            break

    return None

# ----------------------------------------------------------
# 1. Lecture et préparation de f(x)
# ----------------------------------------------------------
# x est déjà défini comme global
# x = sp.Symbol('x')

def fonction():
    f_str = input("Expression de la fonction (ex: x**2 - 1): ")
    try:
        # S'assurer que 'x' est accessible pour sympify
        global x
        f_sympy = sp.sympify(f_str)
    except Exception as e:
        print("❌ Erreur : fonction invalide.")
        print(e)
        # On ne quitte pas, on laisse l'utilisateur réessayer via la boucle du menu
        raise # Renvoyer l'erreur pour que menu() la gère

    return f_sympy

 # Précision
def precision():
    while True:
        try:
           # Remplacer 'input' qui peut être interprété comme une fonction Python intégrée si elle est masquée
           eps_str = input("précision (exemple: 1e-7 ou 0.000001): ")
           return float(eps_str)
        except ValueError:
           print("La valeur n'est pas valide")

# ----------------------------------------------------------
# 2. Récupération des bornes et du pas
# ----------------------------------------------------------
def donnee():
    while True:
        try:
            inf_str = input("Borne inférieure : ")
            supr_str = input("Borne supérieure : ")
            inf = float(inf_str)
            supr = float(supr_str)


            if supr <= inf:
                print("⚠ La borne supérieure doit être > à la borne inférieure.")
                continue

            return inf, supr  # ← retourne directement les valeurs

        except ValueError:
            print("❌ Saisie invalide (valeur non numérique).")

#------------------------------
# pas
#------------------------------
def pas():
    while True:
        try:
            h_str = input("Pas de balayage h : ")
            h = float(h_str)
            if h <= 0:
                print("⚠ Le pas doit être > 0.")
                continue
            return h
        except ValueError:
            print("Saisie invalide.")

#-------------------------------------
# valeur initiale pour Newton-Raphson
#-------------------------------------
def initial():
    while True:
        try:
            xa_str = input("Initialisation de x pour Newton (x0) : ")
            xa = float(xa_str)
            return xa
        except ValueError:
            print("Saisie invalide.")



#==================================================================
# FONCTIONS DE TRAITEMENT
#==================================================================
# point fixe
def ptfixe():
    global f_sympy, a, b, eps, x # Utilisation des globales

    # La fonction numérique pour le balayage est déjà prête
    f_num = sp.lambdify(x, f_sympy, 'numpy')

    # ============================================================
    # 1. Génération automatique de g(x) candidates
    # ============================================================
    def generate_g_candidates(expr_str, lambda_val=0.1):
        g_candidates_expr = []

        # A) g(x) = x - λ f(x)
        g_candidates_expr.append(x - lambda_val * expr_str)

        # B) Essayer d’isoler x dans f(x)=0 (si possible)
        try:
            # Nous utilisons f_sympy qui est global
            sols = sp.solve(expr_str, x)
            for s in sols:
                # Assurez-vous que 's' est une expression et non une simple valeur si f(x) n'était pas un polynôme simple
                if s.has(x):
                     g_candidates_expr.append(sp.simplify(s))
        except Exception:
            pass

        # C) Ajouter g(x) = x + f(x) * c, où c est une constante pour les cas simples (non implémenté ici)

        # Nettoyage
        # Filtrer les expressions qui ne sont pas des expressions symboliques valides si sp.solve a retourné des constantes
        g_candidates_expr = [sp.simplify(g) for g in g_candidates_expr if isinstance(g, (sp.Expr, sp.Basic))]

        # Ajout d'une autre forme classique si le degré est simple (ex: x=g(x))
        if f_sympy.has(x**2) and not f_sympy.has(x**3): # Exemple simple pour x^2-C
             try:
                 g_candidates_expr.extend([sp.sqrt(f_sympy + x**2 - x), -sp.sqrt(f_sympy + x**2 - x)])
             except:
                 pass

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
                # Vérification de l'existence de g(x) et g'(x)
                gi = g_num(xi)
                dpi = g_prime_num(xi)
                if np.isnan(gi) or np.isnan(dpi) or np.isinf(gi) or np.isinf(dpi):
                    return False
                # Condition de convergence |g'(x)| < 1
                if abs(dpi) >= 1:
                    return False
            # Une vérification supplémentaire pour s'assurer que g(x) reste dans l'intervalle si possible
            # g_min = min(g_num(xs))
            # g_max = max(g_num(xs))
            # if not (g_min >= interval[0] and g_max <= interval[1]):
            #     return False

            return True
        except Exception:
            return False

    def filter_safe_g(g_candidates_expr, interval):
        return [g for g in g_candidates_expr if is_safe_g(g, interval)]

    # ----------------------------------------------------------
    # 3. Méthode du point fixe
    # ----------------------------------------------------------
    def point_fixe(g_expr, x0, eps, max_iter=2000):
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
        return None # Échec si max_iter atteint

    # ----------------------------------------------------------
    # 4. Fonction principale du module
    # ----------------------------------------------------------
    def solve_point_fixe(f_num, inf, supr, eps):

        interval = (inf, supr) # Intervalle [a, b] déjà trouvé par le balayage dans menu()

        # Génération et filtrage de g(x)
        g_candidates = generate_g_candidates(f_sympy, lambda_val=0.1)
        safe_g = filter_safe_g(g_candidates, interval)

        print("\n--- Point Fixe ---")
        if not safe_g:
            print("\n❌ Aucune fonction g(x) valide (|g'(x)| < 1) trouvée pour le point fixe sur l'intervalle.")
            return

        # Point initial au milieu de l'intervalle détecté
        x0 = (interval[0] + interval[1]) / 2
        solution = point_fixe(safe_g[0], x0, eps)

        if solution is None:
            print("❌ Échec de convergence de la méthode du point fixe.")
            return

        print(f"\nLa fonction g(x) choisie : {safe_g[0]}")
        print(f"🎯 Solution approchée : x ≈ {solution}")
        print(f"   f({solution}) = {f_num(solution)}") # Vérification de f(sol)

    # La fonction menu() s'assure que a, b, eps sont définis
    solve_point_fixe(f_num, a, b, eps)

# Dichotomie
def dichosol():
    global f_sympy, a, b, eps, x # Utilisation des globales

    f = sp.lambdify(x, f_sympy, "numpy")  # fonction numérique

    def dicho(a, b, eps):
        # Vérification du changement de signe (déjà fait par balayage, mais bonne sécurité)
        if f(a) * f(b) > 0:
            return None

        for _ in range(2000): # Limite d'itérations pour éviter les boucles infinies
             if abs(b - a) <= eps:
                break

             m = (a + b) / 2

             # Pour gérer les erreurs de calcul ou les valeurs non numériques
             try:
                 fm = f(m)
             except Exception:
                 # Si f(m) n'est pas calculable (ex: domaine de définition), on sort
                 return None

             if np.isnan(fm) or np.isinf(fm):
                 return None

             if fm == 0:  # racine exacte
                 return m

             if f(a) * fm < 0:
                 b = m
             else:
                 a = m

        return (a + b) / 2

    print("\n--- Dichotomie ---")
    # Utilisation des globales a, b, eps
    sol = dicho(a, b, eps)

    if sol is not None:
        print(f"✔ Racine approchée : x ≈ {sol}")
        print(f"   f({sol}) = {f(sol)}")
    else:
        print("❌ Aucune solution trouvée sur cet intervalle par dichotomie (problème de signe ou de domaine).")

# Newton-Raphson
def newsonsol(x0_init):
    global f_sympy, a, b, eps, x # Utilisation des globales

    f_prime = sp.diff(f_sympy, x)
    f_prime_num = sp.lambdify(x, f_prime, 'numpy')
    f = sp.lambdify(x, f_sympy, "numpy")  # fonction numérique

    def newson(x0, eps, max_iter=1000):
        for _ in range(max_iter):
            try:
                fx0 = f(x0)
                fpx0 = f_prime_num(x0)

                # Éviter la division par zéro
                if fpx0 == 0:
                    return None
                # Éviter NaN/Inf
                if np.isnan(fx0) or np.isinf(fx0) or np.isnan(fpx0) or np.isinf(fpx0):
                    return None

                x1 = x0 - fx0 / fpx0

                if abs(x1 - x0) < eps:
                    return x1
                x0 = x1
            except Exception:
                return None
        return None # Échec si max_iter atteint

    print("\n--- Newton-Raphson ---")
    # Utilisation de x0_init (qui est x0_newton) et eps
    sol = newson(x0_init, eps)

    if sol is not None:
        print(f"✔ Racine approchée : x ≈ {sol}")
        print(f"   f({sol}) = {f(sol)}")
    else:
        print("❌ Échec de convergence (dérivée nulle, NaN, ou max_iter atteint).")

# Corde
def cordesol():
    global f_sympy, a, b, eps, x # Utilisation des globales

    f = sp.lambdify(x, f_sympy, "numpy")  # fonction numérique

    def corde(x0, x1, eps, max_iter=1000):
        # Vérification du changement de signe (déjà fait par balayage, mais bonne sécurité)
        if f(x0) * f(x1) > 0:
            return None

        for _ in range(max_iter):
            try:
                fx0 = f(x0)
                fx1 = f(x1)

                denominateur = fx1 - fx0
                if denominateur == 0:
                    # Si f(x1) = f(x0), on sort
                    return None

                x2 = x1 - fx1 * (x1 - x0) / denominateur

                if abs(x2 - x1) < eps:
                    return x2

                x0, x1 = x1, x2 # Mise à jour de l'intervalle/points
            except Exception:
                return None # Erreur de calcul

        return None # Échec si max_iter atteint

    print("\n--- Méthode de la Corde (Sécan-Fausse Position) ---")
    # Utilisation des globales a, b, eps
    sol = corde(a, b, eps)

    if sol is not None:
        print(f"✔ Racine approchée : x ≈ {sol}")
        print(f"   f({sol}) = {f(sol)}")
    else:
        print("❌ Échec de convergence ou pas de changement de signe sur l'intervalle.")

# La fonction menu() gère le lancement et la boucle.
menu()