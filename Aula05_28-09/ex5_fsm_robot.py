import math

def controle_reativo(distancias):
    df = distancias.get('frente', 5.0)
    de = distancias.get('esquerda', 5.0)
    dd = distancias.get('direita', 5.0)
    if df < 0.4:
        return 0.0, (1.0 if de >= dd else -1.0)
    return 0.5, 0.8 * (de - dd)

def calcular_orientacao_alvo(x, y, theta, x_alvo, y_alvo, Kp=1.5):
    e_theta = math.atan2(math.sin(math.atan2(y_alvo - y, x_alvo - x) - theta),
                         math.cos(math.atan2(y_alvo - y, x_alvo - x) - theta))
    return Kp * e_theta

def maquina_de_estados(x, y, theta, x_alvo, y_alvo, dist_frente, dist_esq, dist_dir):
    dist_alvo = math.hypot(x_alvo - x, y_alvo - y)

    if dist_alvo < 0.2:
        return "OBJETIVO_ALCANÇADO", 0.0, 0.0
    elif dist_frente < 0.5:
        v, w = controle_reativo({'frente': dist_frente, 'esquerda': dist_esq, 'direita': dist_dir})
        return "DESVIAR_OBSTACULO", v, w
    else:
        w = calcular_orientacao_alvo(x, y, theta, x_alvo, y_alvo)
        return "IR_PARA_ALVO", 0.4, w

if __name__ == "__main__":
    casos = [
        (0.0, 0.0, 0.0, 4.0, 4.0, 2.0, 1.0, 1.0),
        (1.0, 1.0, 0.0, 4.0, 4.0, 0.3, 1.5, 0.5),
        (3.95, 3.95, 0.0, 4.0, 4.0, 2.0, 1.0, 1.0)
    ]
    for c in casos:
        print(maquina_de_estados(*c))