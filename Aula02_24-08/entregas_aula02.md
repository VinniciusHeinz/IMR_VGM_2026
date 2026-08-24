**Entregas Aula 02**

**Estado do Robô e Pose 2D**

O estado do robô representa as informações necessárias para saber sua posição e orientação em determinado momento. Na pose 2D, utilizamos três valores: x, y e theta. Os valores x e y indicam a posição do robô no plano, enquanto theta representa sua orientação em relação ao eixo de referência. Assim, a pose permite saber não apenas onde o robô está, mas também para qual direção ele está apontando.

**Cinemática Diferencial**

A cinemática diferencial descreve o movimento de um robô que possui duas rodas motorizadas, uma de cada lado. A velocidade de cada roda influencia diretamente o movimento do robô. Quando as duas rodas possuem a mesma velocidade, o robô se movimenta em linha reta. Quando possuem velocidades diferentes, o robô realiza uma curva. Se as rodas tiverem velocidades iguais em sentidos opostos, o robô consegue girar em torno do próprio eixo.

**Odometria Discreta**

A odometria é utilizada para estimar a posição e a orientação do robô a partir de seu movimento. No modelo discreto, essa atualização é realizada em pequenos intervalos de tempo dt. A cada intervalo, são utilizadas a velocidade linear e a velocidade angular para atualizar os valores de x, y e theta. Como essa posição é estimada a partir do movimento, pequenos erros podem se acumular ao longo do tempo.

**Navegação GO-TO-GOAL**

A navegação GO-TO-GOAL tem como objetivo fazer o robô chegar a um ponto determinado. Para isso, calcula-se a direção do alvo e compara-se essa direção com a orientação atual do robô. A diferença entre os dois ângulos é utilizada para corrigir o movimento. No controlador proporcional utilizado na aula, quanto maior o erro de orientação, maior é a correção aplicada à velocidade angular. Quando o robô chega próximo o suficiente do ponto desejado, ele para.

De forma geral, os tópicos estão relacionados: a pose representa o estado do robô, a cinemática determina como as velocidades das rodas produzem movimento, a odometria estima como a pose muda ao longo do tempo e o GO-TO-GOAL utiliza essas informações para orientar o robô até um destino.