# Relatório de Atividades — AC-2 Parte Final (Aula 05)

**Identificação do Trio:**
* Integrante 1: Vinnicius Patera Heinz de Oliveira RA103003
* Integrante 2: Gabriel Silva do Nascimento RA104373
* Integrante 3: Matheus Rafaldini Nacacura Muniz RA98871

---

## Exercício 1: Nó Atuador — Conversor de `/cmd_vel` com Saturação dos Motores

### Explicação Técnica
A conversão de velocidades linear (v) e angular (omega) para as rodas esquerda (v_e) e direita (v_d) foi realizada pela cinemática diferencial inversa:
* v_e = v - (omega * L / 2)
* v_d = v + (omega * L / 2)

Para evitar distorção no raio de curvatura durante comandos agressivos, aplicou-se saturação proporcional: quando a roda mais veloz ultrapassa o limite físico de ±1.5 m/s, ambas as velocidades são escalonadas pelo fator (1.5 / max(|v_e|, |v_d|)).

### Saída da Execução (Terminal)
Entrada: v = 1.2 m/s, omega = 3.0 rad/s
Resultado Saturado: v_e = 0.9000 m/s, v_d = 1.5000 m/s

---

## Exercício 2: Nó Sensor — Processador e Filtro do Tópico `/scan`

### Explicação Técnica
O vetor de 360 amostras do sensor LiDAR foi filtrado eliminando leituras inválidas (< 0.1 m ou > 5.0 m) e particionado nos três setores operacionais do robô:
* Frente: Ângulos de 345° a 359° e 0° a 15°.
* Esquerda: Ângulos de 45° a 135°.
* Direita: Ângulos de 225° a 315°.

Em cada setor, o algoritmo extrai a distância mínima válida para alimentação dos controladores reativos.

### Saída da Execução (Terminal)
Distâncias Mínimas Filtradas:
  - Frente: 0.35 m
  - Esquerda: 1.20 m
  - Direita: 2.10 m

---

## Exercício 3: Lógica Reativa de Obstáculos (Braitenberg com Trava)

### Explicação Técnica
A lógica implementa duas camadas de segurança:
1. Trava Crítica (d_frente < 0.4 m): Freia completamente a velocidade linear (v = 0.0 m/s) e executa giro no próprio eixo (omega = ±1.0 rad/s) voltado para o lado com maior distância desimpedida.
2. Navegação Livre (d_frente >= 0.4 m): Robô avança a v = 0.5 m/s e ajusta sua trajetória com base na diferença lateral: omega = Kp * (d_esq - d_dir).

### Saída da Execução (Terminal)
Cenário 1 (Emergência): v = 0.00 m/s, omega = 1.00 rad/s
Cenário 2 (Frente Livre): v = 0.50 m/s, omega = -0.40 rad/s

---

## Exercício 4: Controlador Proporcional para Atração ao Alvo

### Explicação Técnica
O alinhamento angular até a coordenada de destino (x_alvo, y_alvo) foi calculado por:
* theta_alvo = atan2(y_alvo - y, x_alvo - x)
* e_theta = atan2(sin(theta_alvo - theta), cos(theta_alvo - theta))
* omega = Kp * e_theta (com Kp = 1.5)

A normalização com atan2 previne descontinuidades na transição de ±pi radianos, garantindo rotações sempre pelo menor ângulo.

### Saída da Execução (Terminal)
Pose: (1.0, 1.0, 0.0 rad) | Alvo: (3.0, 3.0)
Velocidade angular corretiva (omega): 1.1781 rad/s

---

## Exercício 5: Máquina de Estados Finitos do Robô Autônomo

### Explicação Técnica
A navegação global é gerenciada por uma FSM com três estados mutuamente exclusivos:
1. OBJETIVO_ALCANÇADO: Ativado quando a distância euclidiana até o alvo for inferior a 0.2 m (v = 0.0 m/s, omega = 0.0 rad/s).
2. DESVIAR_OBSTACULO: Prioridade de segurança ativada quando d_frente < 0.5 m, acionando a lógica reativa com freio e manobra de rotação.
3. IR_PARA_ALVO: Estado padrão onde o robô translada a 0.4 m/s orientando-se ativamente para as coordenadas do objetivo.

### Saída da Execução (Terminal)
Cenário 1: Estado = IR_PARA_ALVO | v = 0.40 m/s | omega = 1.18 rad/s
Cenário 2: Estado = DESVIAR_OBSTACULO | v = 0.00 m/s | omega = 1.00 rad/s
Cenário 3: Estado = OBJETIVO_ALCANÇADO | v = 0.00 m/s | omega = 0.00 rad/s
