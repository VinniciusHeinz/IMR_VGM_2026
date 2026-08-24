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
            pygame.draw.lines(surface, COR_RASTRO, False, self.history, 2)
            
        pos = (int(self.x), int(self.y))
        
        # 2. Corpo do robô
        pygame.draw.circle(surface, COR_ROBO, pos, int(self.radius), 2)
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
            surface, COR_VETOR, pos,
            (int(frente_x), int(frente_y)), 3
        )


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(
        "DEMO PROFESSOR: Quadrado em Malha Aberta"
    )
    clock = pygame.time.Clock()
    font_bold = pygame.font.SysFont("monospace", 16, bold=True)
    font = pygame.font.SysFont("monospace", 14)

    robot = DemoRobot(
        x=LARGURA // 2,
        y=ALTURA // 2,
        theta=0.0
    )

    modo_atual = "Iniciando..."

    # Máquina de estados
    estado = "MOVENDO"
    tempo_estado = 0.0
    lado_atual = 1

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Máquina de estados
        tempo_estado += dt

        if estado == "MOVENDO":
            # Anda para frente durante 2 segundos
            robot.set_wheel_velocities(60.0, 60.0)
            modo_atual = f"Lado {lado_atual}/4 - Movendo"

            if tempo_estado >= 2.0:
                estado = "GIRANDO"
                tempo_estado = 0.0

        elif estado == "GIRANDO":
            # Gira no próprio eixo durante 1 segundo
            robot.set_wheel_velocities(-60.0, 60.0)
            modo_atual = f"Lado {lado_atual}/4 - Girando"

            if tempo_estado >= 1.0:
                tempo_estado = 0.0
                lado_atual += 1

                if lado_atual > 4:
                    estado = "FINALIZADO"
                else:
                    estado = "MOVENDO"

        elif estado == "FINALIZADO":
            # Para o robô após completar os 4 lados
            robot.set_wheel_velocities(0.0, 0.0)
            modo_atual = "Quadrado finalizado"

        robot.update(dt)

        # Renderização
        screen.fill(COR_FUNDO)
        robot.draw(screen)

        # Painel Didático de Telemetria
        painel = [
            f"ESTADO: {modo_atual}",
            f"-----------------------------------------------------------------",
            f"Pose Real: x = {robot.x:6.1f} px | y = {robot.y:6.1f} px | theta = {math.degrees(robot.theta):6.1f}° ({robot.theta:5.2f} rad)",
            f"Entradas de Roda:   v_Esquerda (Vermelha) = {robot.v_l:5.1f} px/s | v_Direita (Verde) = {robot.v_r:5.1f} px/s",
            f"Cinemática Direta:  v Linear = {robot.v:5.1f} px/s | omega Angular = {robot.omega:5.2f} rad/s",
            f"Tempo no estado: {tempo_estado:5.2f} s",
            f"-----------------------------------------------------------------",
            f"Quadrado: 2s andando + 1s girando | Lado: {min(lado_atual, 4)}/4"
        ]

        for i, linha in enumerate(painel):
            cor = (255, 215, 0) if i == 0 else (220, 220, 220)
            f = font_bold if i in [0, 2, 4] else font
            rendered = f.render(linha, True, cor)
            screen.blit(rendered, (20, 20 + i * 22))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
