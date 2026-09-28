def controle_reativo(distancias):
    df = distancias.get('frente', 5.0)
    de = distancias.get('esquerda', 5.0)
    dd = distancias.get('direita', 5.0)

    if df < 0.4:
        v = 0.0
        omega = 1.0 if de >= dd else -1.0
    else:
        v = 0.5
        omega = 0.8 * (de - dd)

    return v, omega

if __name__ == "__main__":
    print("Crítico:", controle_reativo({'frente': 0.3, 'esquerda': 1.5, 'direita': 0.5}))
    print("Livre:", controle_reativo({'frente': 2.0, 'esquerda': 1.0, 'direita': 1.5}))