# ================================
# MODULE : _balayage.py
# ================================
import numpy as np

def balayage(f, inf, supr, h):

    x0 = inf

    while x0 + h <= supr:
        try:
            y1 = f(x0)
            y2 = f(x0 + h)

            # Ignore NaN, infinies
            if np.isnan(y1) or np.isnan(y2) or np.isinf(y1) or np.isinf(y2):
                x0 += h
                continue

            if y1 * y2 < 0:   # changement de signe
                return x0, x0 + h

        except Exception:
            # En cas d’erreur f(x) → passer au point suivant
            pass

        x0 += h

    return inf, supr