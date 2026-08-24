import pygame
import math
import numpy as np  

# Configurações de Display
LARGURA, ALTURA = 900, 650
FPS = 60
COR_FUNDO = (20, 24, 30)
COR_ROBO = (0, 200, 255)
COR_RODA_ESQ = (255, 100, 100)
COR_RODA_DIR = (100, 255, 100)
COR_VETOR = (255, 230, 0)
COR_RASTRO = (0, 150, 100)
COR_ALVO = (255, 0, 255)

class DemoRobot:
    def __init__(self, x, y, theta=0.0, wheelbase=40.0, radius=20.0):
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)
        self.L = float(wheelbase)
        self.radius = float(radius)
        
        self.v_l = 0.0
        self.v_r = 0.0
        self.v = 0.0
        self.omega = 0.0
        self.history = []

    def set_wheels(self, v_left, v_right):
        self.v_l = v_left
        self.v_r = v_right

        # Equações de Cinemática Direta
        self.v = (self.v_r + self.v_l) / 2.0
        self.omega = (self.v_r - self.v_l) / self.L

    def set_wheel_velocities(self, v_left, v_right):
        self.set_wheels(v_left, v_right)

    def update(self, dt):
        self.theta += self.omega * dt
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi
        
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt
        
        # Guarda histórico para visualização de trajetória
        if len(self.history) == 0 or np.hypot(
            self.x - self.history[-1][0],
            self.y - self.history[-1][1]
        ) > 3:
            self.history.append((self.x, self.y))
            if len(self.history) > 800:
                self.history.pop(0)

    def draw(self, surface):
        # 1. Rastro
        if len(self.history) > 1:
            pygame.draw.lines(
                surface, COR_RASTRO,
                False, self.history, 2
            )
            
        pos = (int(self.x), int(self.y))
        
        # 2. Corpo do robô
        pygame.draw.circle(
            surface, COR_ROBO,
            pos, int(self.radius), 2
        )
        pygame.draw.circle(
            surface, (40, 60, 80),
            pos, int(self.radius) - 2
        )
        
        # 3. Desenho das Rodas
        cos_t = math.cos(self.theta)
        sin_t = math.sin(self.theta)
        
        w_esq_x = self.x - (self.L / 2) * sin_t
        w_esq_y = self.y + (self.L / 2) * cos_t
        w_dir_x = self.x + (self.L / 2) * sin_t
        w_dir_y = self.y - (self.L / 2) * cos_t
        
        pygame.draw.circle(
            surface, COR_RODA_ESQ,
            (int(w_esq_x), int(w_esq_y)), 5
        )

        pygame.draw.circle(
            surface, COR_RODA_DIR,
            (int(w_dir_x), int(w_dir_y)), 5
        )
        
        # 4. Vetor Direção
        frente_x = self.x + (self.radius + 15) * cos_t
        frente_y = self.y + (self.radius + 15) * sin_t
        
        pygame.draw.line(
            surface, COR_VETOR,
            pos,
            (int(frente_x), int(frente_y)),
            3
        )


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(
        "DEMO PROFESSOR: Controle Proporcional"
    )
    clock = pygame.time.Clock()
    font_bold = pygame.font.SysFont("monospace", 16, bold=True)
    font = pygame.font.SysFont("monospace", 14)

    robot = DemoRobot(
        x=LARGURA // 2,
        y=ALTURA // 2,
        theta=0.0
    )

    modo_atual = "Clique na tela para definir o alvo"

    # Ponto alvo
    alvo = None

    # Ganho proporcional
    Kp = 3.0

    # Distância mínima para considerar que chegou
    distancia_minima = 10.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    alvo = event.pos
                    robot.history.clear()
                    modo_atual = "Alvo definido - seguindo"

        # Controle proporcional
        if alvo is not None:

            # Calcula distância até o alvo
            dx = alvo[0] - robot.x
            dy = alvo[1] - robot.y

            distancia = math.hypot(dx, dy)

            # Verifica se chegou ao destino
            if distancia < distancia_minima:

                robot.set_wheel_velocities(0.0, 0.0)
                modo_atual = "Alvo alcançado!"

            else:
                # Ângulo desejado para apontar para o alvo
                theta_desejado = math.atan2(dy, dx)

                # Erro angular
                erro_theta = theta_desejado - robot.theta

                # Normaliza o erro para [-pi, pi]
                erro_theta = (
                    erro_theta + math.pi
                ) % (2 * math.pi) - math.pi

                # Controlador proporcional
                omega = Kp * erro_theta

                # Limita a velocidade angular
                omega_max = 3.0
                omega = max(
                    -omega_max,
                    min(omega, omega_max)
                )

                # Velocidade linear
                velocidade = 60.0

                # Cinemática inversa:
                # v_l = v - omega*L/2
                # v_r = v + omega*L/2
                v_left = velocidade - (
                    omega * robot.L / 2
                )

                v_right = velocidade + (
                    omega * robot.L / 2
                )

                # Limita velocidades das rodas
                v_left = max(-100.0, min(100.0, v_left))
                v_right = max(-100.0, min(100.0, v_right))

                robot.set_wheel_velocities(
                    v_left,
                    v_right
                )

                modo_atual = (
                    f"Seguindo alvo | "
                    f"Distância: {distancia:.1f} px"
                )

        robot.update(dt)

        # Renderização
        screen.fill(COR_FUNDO)

        # Desenha o alvo
        if alvo is not None:
            pygame.draw.circle(
                screen,
                COR_ALVO,
                alvo,
                8
            )

            pygame.draw.circle(
                screen,
                COR_ALVO,
                alvo,
                int(distancia_minima),
                1
            )

        robot.draw(screen)

        # Painel Didático de Telemetria
        distancia_texto = (
            f"{distancia:5.1f} px"
            if alvo is not None
            else "-----"
        )

        painel = [
            f"ESTADO: {modo_atual}",
            f"-----------------------------------------------------------------",
            f"Pose Real: x = {robot.x:6.1f} px | y = {robot.y:6.1f} px | theta = {math.degrees(robot.theta):6.1f}° ({robot.theta:5.2f} rad)",
            f"Alvo: x = {alvo[0]:6.1f} px | y = {alvo[1]:6.1f} px" if alvo else "Alvo: Nenhum",
            f"Distância até o alvo: {distancia_texto}",
            f"Kp = {Kp:.2f} | Velocidade Linear = {robot.v:5.1f} px/s | omega = {robot.omega:5.2f} rad/s",
            f"-----------------------------------------------------------------",
            f"Controle: Clique com o mouse para definir o ponto alvo"
        ]

        for i, linha in enumerate(painel):
            cor = (
                (255, 215, 0)
                if i == 0
                else (220, 220, 220)
            )

            f = (
                font_bold
                if i in [0, 2, 4]
                else font
            )

            rendered = f.render(
                linha,
                True,
                cor
            )

            screen.blit(
                rendered,
                (20, 20 + i * 22)
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
