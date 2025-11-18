# AlgorithmeNumeriqueRENLfinal

# 🚀 Résolveur d'Équations Non Linéaires

Ce programme Python est un outil complet pour trouver les racines d'une fonction non linéaire $f(x)=0$ sur un intervalle spécifié. Il implémente quatre méthodes numériques fondamentales pour la résolution d'équations.

---

## ✨ Fonctionnalités Principales

Le programme offre un **menu interactif** permettant à l'utilisateur de définir l'équation, l'intervalle de recherche, la précision et de choisir la méthode de résolution.

### 1. Pré-traitement et Saisie 🔍

* **Saisie de Fonction Symbolique :** L'utilisateur entre la fonction $f(x)$ sous forme d'une chaîne de caractères (ex: `x**2 - sp.cos(x)`). La librairie **SymPy** est utilisée pour la manipulation symbolique et le calcul des dérivées.
* **Balayage Automatique (Bracketing) :** La fonction `balayage` recherche un sous-intervalle $\mathbf{[a, b]}$ où un **changement de signe** est détecté ($f(a) \cdot f(b) < 0$), garantissant l'existence d'au moins une racine (Théorème des Valeurs Intermédiaires).

---

### 2. Méthodes Numériques Implémentées 🔢

Le programme permet de choisir parmi les méthodes suivantes pour affiner la solution dans l'intervalle $\mathbf{[a, b]}$ :

| Méthode | Principe | Caractéristiques |
| :--- | :--- | :--- |
| **Dichotomie** | Division répétée de l'intervalle $\mathbf{[a, b]}$ par deux. | **Toujours convergente** (la plus robuste). Convergence linéaire lente. |
| **Point Fixe** | Cherche la racine comme point fixe d'une fonction $g(x)$ où $x=g(x)$. | Convergence si $|\mathbf{g'(x) < 1}|$. Implémentation d'un générateur de $g(x)$ candidates. |
| **Newton-Raphson** | Utilise la tangente en $x_n$ pour déterminer $\mathbf{x_{n+1}}$. | **Convergence quadratique** (très rapide). Nécessite la dérivée $f'(x)$ et un bon point initial $x_0$. |
| **Corde (ou Sécante)** | Remplace la dérivée de Newton par une approximation basée sur deux points. | Plus rapide que la dichotomie. Ne nécessite **pas** le calcul formel de la dérivée. |

---

## 🛠️ Exigences et Utilisation

### Prérequis

Le programme nécessite les bibliothèques Python suivantes :

* **`sympy`** : Pour la manipulation symbolique.
* **`numpy`** : Pour les calculs numériques.

Installation des dépendances :
```bash
pip install sympy numpy


## Auteur  Syntroπ_dev
