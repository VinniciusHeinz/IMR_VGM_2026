def converter_cmd_vel(v, omega, L=0.3, max_wheel_speed=1.5):
    # Velocidades individuais (cinemática inversa diferencial)
    v_e = v - (omega * L / 2.0)
    v_d = v + (omega * L / 2.0)

    # Identificar se alguma roda ultrapassa o limite
    maior_vel = max(abs(v_e), abs(v_d))
    if maior_vel > max_wheel_speed:
        fator = max_wheel_speed / maior_vel
        v_e *= fator
        v_d *= fator

    return v_e, v_d

if __name__ == "__main__":
    ve, vd = converter_cmd_vel(1.2, 3.0)
    print(f"v_e: {ve:.4f} m/s | v_d: {vd:.4f} m/s")