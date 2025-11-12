import pygame
import sys
from perguntas import perguntas

#inicializacao do pygame
pygame.init() 
tela = pygame.display.set_mode((800, 500)) 
pygame.display.set_caption("Meninas em STEM: As Goytatecs")
clock = pygame.time.Clock() 
font = pygame.font.SysFont("Arial", 24)
smallFont = pygame.font.SysFont("Arial", 20) 

#variaveis globais
score = 0
questaoAtual = 0 
feedback = ""
feedbackTimer = 0 

#funcoes
def draw_text_wrapped(surface, text, color, rect, font, line_spacing=5):
    words = text.split(' ')
    lines = []
    line = ''
    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < rect.width:
            line = test_line
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)

    y = rect.top
    for l in lines:
        text_surface = font.render(l, True, color)
        surface.blit(text_surface, (rect.left, y))
        y += font.get_height() + line_spacing

def desenharTelaInicial():
    imagemFundo = pygame.image.load("fundo.jpg")   
    imagemFundo = pygame.transform.scale(imagemFundo, (800, 500)) 
    tela.blit(imagemFundo, (0, 0))

    caixaTitulo = pygame.Rect(220, 80, 400, 80)
    pygame.draw.rect(tela, (255, 255, 255), caixaTitulo, border_radius=12)
    titulo = font.render("Meninas em STEM: As Goytatecs", True, (0,0,0))
    tela.blit(titulo, (280, 100))

    botaoJogar = pygame.Rect(250, 200, 300, 60)
    botaoSair = pygame.Rect(250, 300, 300, 60)

    pygame.draw.rect(tela, (255,255,255), botaoJogar, border_radius=10)
    pygame.draw.rect(tela, (255,255,255), botaoSair, border_radius=10)

    jogarTxt = smallFont.render("Jogar", True, (100, 150, 250))
    sairTxt = smallFont.render("Sair", True, (100, 150, 250))
    tela.blit(jogarTxt, (botaoJogar.x + 120, botaoJogar.y + 15))
    tela.blit(sairTxt, (botaoSair.x + 130, botaoSair.y + 15))

def desenharPergunta(q):
    tela.fill((240, 240, 240)) 
    draw_text_wrapped(tela, q["pergunta"], (0,0,0), pygame.Rect(50, 50, 700, 100), font) 
    
    # Desenha opções
    for i, opcao in enumerate(q["opcoes"]): 
        botao_rect = pygame.Rect(50, 150 + i*70, 600, 60) 
        pygame.draw.rect(tela, (100, 150, 250), botao_rect, border_radius=8) 
        draw_text_wrapped(
            tela,
            opcao,
            (255, 255, 255),  
            pygame.Rect(
                botao_rect.x + 10,        
                botao_rect.y + 8,         
                botao_rect.width - 20,    
                botao_rect.height - 16    
            ),
            smallFont,
            line_spacing=2
        )

def desenharResultado():
    #mostrar resultado
    tela.fill((240, 240, 240)) 
    resultadoSurface = font.render(f"Quiz finalizado! Pontuação: {score}/{len(perguntas)}", True, (0, 0, 0)) 
    tela.blit(resultadoSurface, (50, 200)) 

    #botao Jogar Novamente
    pygame.draw.rect(tela, (100, 150, 250), (50, 280, 200, 50))
    jogarNovamenteSurface = smallFont.render("Jogar Novamente", True, (255, 255, 255))
    tela.blit(jogarNovamenteSurface, (80, 290))

def checkClickInicio(posicao_click):
    global estadoJogo, running
    botaoJogar = pygame.Rect(250, 200, 300, 60)
    botaoSair = pygame.Rect(250, 300, 300, 60)

    if botaoJogar.collidepoint(posicao_click):
        estadoJogo = "jogo"
    elif botaoSair.collidepoint(posicao_click):
        running = False
        
def checkClickPerguntas(posicao_click): 
    global score, questaoAtual, feedback, feedbackTimer, estadoJogo 
    q = perguntas[questaoAtual]
    for i in range(4): 
        botao_area = pygame.Rect(50, 150 + i*70, 600, 60) 
        if botao_area.collidepoint(posicao_click): 
            if i == q["resposta"]: 
                score += 1
                feedback = f"Correto! {q['explicacao']}"
            else:
                feedback = f"Errado!"
                
            feedbackTimer = pygame.time.get_ticks() 
            break

def checkClickJogarNovamente(clik):
    global score, questaoAtual, feedback, feedbackTimer, estadoJogo
    botaoAreaJogarNovamente = pygame.Rect(50, 280, 200, 50)
   
    if botaoAreaJogarNovamente.collidepoint(clik):
        score = 0
        questaoAtual = 0
        feedback = ""
        feedbackTimer = 0
        estadoJogo = "jogo"
        print("Clicou no botao Jogar Novamente!")


#loop principal
estadoJogo = 'inicio'
running = True
while running: #loop principal do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if estadoJogo == "inicio":
                checkClickInicio(event.pos)
            elif estadoJogo == "jogo":
                if questaoAtual < len(perguntas):
                    checkClickPerguntas(event.pos)
                else:
                    checkClickJogarNovamente(event.pos)
            elif estadoJogo == "resultado":
                checkClickJogarNovamente(event.pos)
            
    if estadoJogo == "inicio":
        desenharTelaInicial()
    elif estadoJogo == "jogo":
        if questaoAtual < len(perguntas):
            desenharPergunta(perguntas[questaoAtual])
        else:
            desenharResultado()
    elif estadoJogo == "resultado":
        desenharResultado()

        
    # Mostra feedback por 2 segundos
    if feedback != "":
        tempoExecucao = pygame.time.get_ticks() 
        if tempoExecucao - feedbackTimer < 2000: 
            draw_text_wrapped(tela, feedback, (255, 0, 0), pygame.Rect(50, 430, 700, 80), smallFont)
            
        else:
            feedback = ""
            questaoAtual += 1
            if questaoAtual >= len(perguntas):
                estadoJogo = "resultado"

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()