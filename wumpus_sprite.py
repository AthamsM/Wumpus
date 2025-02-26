# Segunda versao (mais fofa)
# E so Deus continua entendendo esse codigo :)

import pygame
import random

# Configurações do jogo
LARGURA, ALTURA = 600, 600  # Tamanho da janela
tamanho_celula = LARGURA // 4

# Inicializa o pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mundo de Wumpus")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Carregar imagens
fundo_img = pygame.image.load("sprites/sprite_0.png")  # Carregar imagem de fundo
fundo_img = pygame.transform.scale(fundo_img, (LARGURA, ALTURA))

agente_img = pygame.image.load("sprites/sprite_3.png")
wumpus_img = pygame.image.load("sprites/sprite_1.png")
tesouro_img = pygame.image.load("sprites/sprite_2.png")
buraco_img = pygame.image.load("sprites/sprite_4.png")

# Redimensionar sprites
agente_img = pygame.transform.scale(agente_img, (tamanho_celula, tamanho_celula))
wumpus_img = pygame.transform.scale(wumpus_img, (tamanho_celula, tamanho_celula))
tesouro_img = pygame.transform.scale(tesouro_img, (tamanho_celula, tamanho_celula))
buraco_img = pygame.transform.scale(buraco_img, (tamanho_celula, tamanho_celula))

# Posicionamento inicial
posicao_inicial = [0, 0]
posicao_agente = [0, 0]
posicao_wumpus = [2, 1]
posicao_buraco = [1, 3]
posicao_ouro = [2, 2]
posicao_segura = [(posicao_agente[0], posicao_agente[0])]
posicao_perigo = []
posicao_proibida = []

def desenhar_tabuleiro():
    tela.blit(fundo_img, (0, 0))  # Desenha a imagem de fundo
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(tela, PRETO, (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula), 1)
    tela.blit(wumpus_img, (posicao_wumpus[1] * tamanho_celula, posicao_wumpus[0] * tamanho_celula))
    tela.blit(buraco_img, (posicao_buraco[1] * tamanho_celula, posicao_buraco[0] * tamanho_celula))
    tela.blit(tesouro_img, (posicao_ouro[1] * tamanho_celula, posicao_ouro[0] * tamanho_celula))
    tela.blit(agente_img, (posicao_agente[1] * tamanho_celula, posicao_agente[0] * tamanho_celula))


def mover_agente(direcao):
  global posicao_agente, posicao_segura, posicao_proibida
  if direcao == "cima" and posicao_agente[0] > 0:
    if (posicao_agente[0] - 1, posicao_agente[1]) in (posicao_proibida):
      print("Você não pode ir para essa posição")
      posicao_segura.append((posicao_agente[0], posicao_agente[1]))    
    else:
      posicao_agente[0] -= 1
  elif direcao == "baixo" and posicao_agente[0] < 3:
    if (posicao_agente[0] + 1, posicao_agente[1]) in posicao_proibida:
      print("Você não pode ir para essa posição")
      posicao_segura.append((posicao_agente[0], posicao_agente[1]))
    else:
      posicao_agente[0] += 1
  elif direcao == "esquerda" and posicao_agente[1] > 0:
    if (posicao_agente[0], posicao_agente[1] - 1) in posicao_proibida:
      print("Você não pode ir para essa posição")
      posicao_segura.append((posicao_agente[0], posicao_agente[1]))
    else:
      posicao_agente[1] -= 1
  elif direcao == "direita" and posicao_agente[1] < 3:
    if (posicao_agente[0], posicao_agente[1] + 1) in (posicao_proibida):
      print("Você não pode ir para essa posição")
      posicao_segura.append((posicao_agente[0], posicao_agente[1]))
    else:
      posicao_agente[1] += 1

def mover_agente_ouro(direcao):
  global posicao_agente, posicao_segura, posicao_proibida
  if direcao == "cima" and posicao_agente[0] > 0:
    if (posicao_agente[0] - 1, posicao_agente[1]) in (posicao_segura):
      posicao_agente[0] -= 1
    else:
      print("Você não pode ir para essa posição")
  elif direcao == "baixo" and posicao_agente[0] < 3:
    if (posicao_agente[0] + 1, posicao_agente[1]) in posicao_segura:
      posicao_agente[0] += 1
    else:
      print("Você não pode ir para essa posição")
  elif direcao == "esquerda" and posicao_agente[1] > 0:
    if (posicao_agente[0], posicao_agente[1] - 1) in posicao_segura:
      posicao_agente[1] -= 1
    else:
      print("Você não pode ir para essa posição")
  elif direcao == "direita" and posicao_agente[1] < 3:
    if (posicao_agente[0], posicao_agente[1] + 1) in (posicao_segura):
      posicao_agente[1] += 1
    else:
      print("Você não pode ir para essa posição")
 
#========================================================
# Função para verificar se o agente encontrou ouro, wumpus ou buraco
def verificar_situacao():
  global ouro
  if posicao_agente == posicao_ouro:
    print("Você encontrou o ouro!")
    ouro = True
    return True
  elif posicao_agente == posicao_wumpus:
    print("Você foi devorado pelo Wumpus!")
    return False
  elif posicao_agente == posicao_buraco:
    print("Você caiu em um buraco!")
    return False
  elif tuple(posicao_agente) in [(posicao_ouro[0] - 1, posicao_ouro[1]),
                                 (posicao_ouro[0] + 1, posicao_ouro[1]),
                                 (posicao_ouro[0], posicao_ouro[1] - 1),
                                 (posicao_ouro[0], posicao_ouro[1] + 1)]:
    if tuple(posicao_agente) in [(posicao_buraco[0] - 1, posicao_buraco[1]),
                                 (posicao_buraco[0] + 1, posicao_buraco[1]),
                                 (posicao_buraco[0], posicao_buraco[1] - 1),
                                 (posicao_buraco[0], posicao_buraco[1] + 1),
                                 (posicao_wumpus[0] - 1, posicao_wumpus[1]),
                                 (posicao_wumpus[0] + 1, posicao_wumpus[1]),
                                 (posicao_wumpus[0], posicao_wumpus[1] - 1),
                                 (posicao_wumpus[0], posicao_wumpus[1] + 1)]:
      if (posicao_agente[0], posicao_agente[1]) in\
         (posicao_perigo or posicao_segura):
        print("to perto, mas cuidado...")
        return True
      else:
        posicao_perigo.append((posicao_agente[0], posicao_agente[1]))
        posicao_segura.append((posicao_agente[0], posicao_agente[1]))
        print("hummmm tem um ourinho perto, mas cuiado...")
        return True
    posicao_segura.append((posicao_agente[0], posicao_agente[1]))
    print("hummmm tem um ourinho perto")
    return True
  #indentifica caso tenha um perigo
  elif tuple(posicao_agente) in [(posicao_buraco[0] - 1, posicao_buraco[1]),
                                 (posicao_buraco[0] + 1, posicao_buraco[1]),
                                 (posicao_buraco[0], posicao_buraco[1] - 1),
                                 (posicao_buraco[0], posicao_buraco[1] + 1),
                                 (posicao_wumpus[0] - 1, posicao_wumpus[1]),
                                 (posicao_wumpus[0] + 1, posicao_wumpus[1]),
                                 (posicao_wumpus[0], posicao_wumpus[1] - 1),
                                 (posicao_wumpus[0], posicao_wumpus[1] + 1)]:
    if (posicao_agente[0], posicao_agente[1]) in posicao_perigo:
      print("denovo aqui??? cuidado...")
      return True
    else:
      print("ixi, que sensação estranha... tem um perigo perto")
      posicao_perigo.append((posicao_agente[0], posicao_agente[1]))
      return True
  else:
    if (posicao_agente[0], posicao_agente[1]) in posicao_segura:
      print("Sim está seguro!")
      return True
    else:
      posicao_segura.append((posicao_agente[0], posicao_agente[1]))
      print("Você está seguro!")
    return True


#========================================================  

def verificar_perigo():
  #ordena nossa lista de perigo
  ordena_posicao_perigo = sorted(posicao_perigo, key=lambda x: x[1])
  for i in range(len(ordena_posicao_perigo)):
    for j in range(i + 1, len(posicao_perigo)):
      par1 = ordena_posicao_perigo[i]
      par2 = ordena_posicao_perigo[j]
      if sum(par1) == sum(par2):
        copia_par1 = par1
        copia_par2 = par2
        if (copia_par1[0], copia_par2[0]) in posicao_proibida:
          return
        else:
          posicao_proibida.append((copia_par1[0], copia_par2[1]))
   
      
# Loop do jogo
ouro = False
vida = True
rodando = True
clock = pygame.time.Clock()
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    if vida:
        if ouro:
            clock.tick(1)
            movimento = random.choice(["cima", "baixo", "esquerda", "direita"])
            mover_agente_ouro(movimento)
            vida = verificar_situacao()
            verificar_perigo()
            desenhar_tabuleiro()
            pygame.display.flip()
            if posicao_agente == posicao_inicial:
                pygame.quit()
        else:
            clock.tick(1)
            movimento = random.choice(["cima", "baixo", "esquerda", "direita"])
            mover_agente(movimento)
            vida = verificar_situacao()
            verificar_perigo()
            desenhar_tabuleiro()
            pygame.display.flip()
    else:
        break

pygame.quit()