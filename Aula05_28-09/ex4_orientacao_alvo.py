import math

def calcular_orientacao_alvo(x, y, theta, x_alvo, y_alvo, Kp=1.5):
    theta_alvo = math.atan2(y_alvo - y, x_alvo - x)
    e_theta = theta_alvo - theta
    e_theta = math.atan2(math.sin(e_theta), math.cos(e_theta))
    return Kp * e_theta

if __name__ == "__main__":
    w = calcular_orientacao_alvo(1.0, 1.0, 0.0, 3.0, 3.0)
    print(f"omega: {w:.4f} rad/s")