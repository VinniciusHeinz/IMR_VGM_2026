import numpy as np

def processar_scan(leituras_lidar):
    leituras = np.array(leituras_lidar, dtype=float)

    # Frente: 345° a 359° e 0° a 15°
    idx_frente = list(range(345, 360)) + list(range(0, 16))
    frente = leituras[idx_frente]
    frente_val = frente[(frente >= 0.1) & (frente <= 5.0)]
    min_frente = float(np.min(frente_val)) if len(frente_val) > 0 else 5.0

    # Esquerda: 45° a 135°
    esq = leituras[45:136]
    esq_val = esq[(esq >= 0.1) & (esq <= 5.0)]
    min_esq = float(np.min(esq_val)) if len(esq_val) > 0 else 5.0

    # Direita: 225° a 315°
    dir_ = leituras[225:316]
    dir_val = dir_[(dir_ >= 0.1) & (dir_ <= 5.0)]
    min_dir = float(np.min(dir_val)) if len(dir_val) > 0 else 5.0

    return {'frente': min_frente, 'esquerda': min_esq, 'direita': min_dir}

if __name__ == "__main__":
    scan_exemplo = np.full(360, 4.0)
    scan_exemplo[0] = 0.0     # Ruído nulo descartado
    scan_exemplo[10] = 0.35   # Obstáculo na frente
    scan_exemplo[90] = 1.20   # Obstáculo à esquerda
    scan_exemplo[270] = 2.10  # Obstáculo à direita
    res = processar_scan(scan_exemplo)
    print(res)