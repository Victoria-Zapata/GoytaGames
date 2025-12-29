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
areaAtual = None
perguntasAtuais = []
perguntaAtual = 0

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
    
    botao_largura = 180
    botao_altura = 60
    espaco = 20

    total_largura = (4 * botao_largura) + (3 * espaco)
    x_inicial = (800 - total_largura) // 2  
    y = 300

    global botaoTecnologia, botaoMatematica, botaoEngenharia, botaoCiencia

    botaoTecnologia = pygame.Rect(x_inicial, y, botao_largura, botao_altura)
    botaoMatematica = pygame.Rect(x_inicial + (botao_largura + espaco), y, botao_largura, botao_altura)
    botaoEngenharia = pygame.Rect(x_inicial + 2 * (botao_largura + espaco), y, botao_largura, botao_altura)
    botaoCiencia = pygame.Rect(x_inicial + 3 * (botao_largura + espaco), y, botao_largura, botao_altura)

    pygame.draw.rect(tela, (255,255,255), botaoTecnologia, border_radius=10)
    pygame.draw.rect(tela, (255,255,255), botaoMatematica, border_radius=10)
    pygame.draw.rect(tela, (255,255,255), botaoEngenharia, border_radius=10)
    pygame.draw.rect(tela, (255,255,255), botaoCiencia, border_radius=10)

    tela.blit(smallFont.render("Tecnologia", True, (100,150,250)), (botaoTecnologia.x + 25, botaoTecnologia.y + 15))
    tela.blit(smallFont.render("Matemática", True, (100,150,250)), (botaoMatematica.x + 25, botaoMatematica.y + 15))
    tela.blit(smallFont.render("Engenharia", True, (100,150,250)), (botaoEngenharia.x + 25, botaoEngenharia.y + 15))
    tela.blit(smallFont.render("Ciências", True, (100,150,250)), (botaoCiencia.x + 40, botaoCiencia.y + 15))

def desenharPergunta(q):
    tela.fill((240, 240, 240)) 
    draw_text_wrapped(tela, q["pergunta"], (0,0,0), pygame.Rect(50, 50, 700, 100), font) 
    
    #desenha opções
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
    tela.fill((240, 240, 240))
    resultadoSurface = font.render(
        f"Quiz finalizado! Pontuação: {score}/{len(perguntasAtuais)}",
        True,
        (0, 0, 0)
    )
    tela.blit(resultadoSurface, (50, 200))

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
    global score, perguntaAtual, feedback, feedbackTimer, estadoJogo

    pergunta = perguntasAtuais[perguntaAtual]

    for i in range(4):
        botao_area = pygame.Rect(50, 150 + i*70, 600, 60)

        if botao_area.collidepoint(posicao_click):

            # Acertou
            if i == pergunta["resposta"]:
                score += 1
                feedback = pergunta["justificativas"][i]
            else:
                feedback = pergunta["justificativas"][i]

            feedbackTimer = pygame.time.get_ticks()

            break

def checkClickJogarNovamente(clik):
    global score, perguntaAtual, feedback, feedbackTimer, estadoJogo
    botaoAreaJogarNovamente = pygame.Rect(50, 280, 200, 50)
   
    if botaoAreaJogarNovamente.collidepoint(clik):
        score = 0
        perguntaAtual = 0
        feedback = ""
        feedbackTimer = 0
        estadoJogo = "jogo"
        print("Clicou no botao Jogar Novamente!")


#loop principal
estadoJogo = "tela_inicial"
running = True
while running:
    
    if estadoJogo == "tela_inicial":
        desenharTelaInicial()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

        if estadoJogo == "tela_inicial" and evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if botaoTecnologia.collidepoint(mouse):
                areaAtual = "tecnologia"
                perguntasAtuais = perguntas["tecnologia"]
                perguntaAtual = 0
                score = 0
                estadoJogo = "jogo"

            elif botaoMatematica.collidepoint(mouse):
                areaAtual = "matematica"
                perguntasAtuais = perguntas["matematica"]
                perguntaAtual = 0
                score = 0
                estadoJogo = "jogo"

            elif botaoEngenharia.collidepoint(mouse):
                areaAtual = "engenharia"
                perguntasAtuais = perguntas["engenharia"]
                perguntaAtual = 0
                score = 0
                estadoJogo = "jogo"

            elif botaoCiencia.collidepoint(mouse):
                areaAtual = "ciencia"
                perguntasAtuais = perguntas["ciencia"]
                perguntaAtual = 0
                score = 0
                estadoJogo = "jogo"

        elif estadoJogo == "jogo" and evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            checkClickPerguntas(mouse)

        elif estadoJogo == "resultado" and evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            checkClickJogarNovamente(mouse)

    #telas
    if estadoJogo == "jogo":
        if perguntaAtual < len(perguntasAtuais):
            desenharPergunta(perguntasAtuais[perguntaAtual])
        else:
            desenharResultado()
    elif estadoJogo == "resultado":
        desenharResultado()

    #feedback
    if feedback != "":
        tempoExecucao = pygame.time.get_ticks()
        if tempoExecucao - feedbackTimer < 2000:
            draw_text_wrapped(tela, feedback, (255, 0, 0), pygame.Rect(50, 430, 700, 80), smallFont)
        else:
            feedback = ""
            perguntaAtual += 1
            if questaoAtual >= len(perguntasAtuais):
                estadoJogo = "resultado"

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()