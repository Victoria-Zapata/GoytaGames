import ctypes
import pygame
import sys
from perguntas import perguntas

#inicializacao do pygame
largura = 1920
altura = 1080
pygame.init() 

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
tela = pygame.display.set_mode((true_res))

fundoInicial = pygame.image.load("assets/images/imagemDeFundo.png")

pygame.display.set_caption("Meninas em STEM: As Goytatecs")
clock = pygame.time.Clock() 
#font = pygame.font.Font("MochiyPopOne-Regular.ttf", 36)
corFonte = (60, 44, 92)
fonteTitulo = pygame.font.Font("MochiyPopOne-Regular.ttf", 36)
fontePergunta = pygame.font.Font("MochiyPopOne-Regular.ttf", 28)
fonteOpcoes = pygame.font.Font("MochiyPopOne-Regular.ttf", 24)

fundo = pygame.image.load("assets/images/imagemDeFundo.png").convert()
balaoPergunta = pygame.image.load("assets/images/balaoFalaPersonagem.png").convert_alpha()
botaoOpcao = pygame.image.load("assets/images/balaoOpcao.png").convert_alpha()
botaoAvancar = pygame.image.load("assets/images/botaoAvancar.png").convert_alpha()
decoracaoEstrela = pygame.image.load("assets/images/decoracaoEstrela.png").convert_alpha()
balaoTitulo = pygame.image.load("assets/images/balaoTitulo.png").convert_alpha()
personagemTecnologia = pygame.image.load("assets/images/personagemTec.png").convert_alpha()
# personagemMatematica = pygame.image.load("assets/images/personagemMat.png").convert_alpha()
# personagemEngenharia = pygame.image.load("assets/images/personagemEng.png").convert_alpha()
personagemCiencia = pygame.image.load("assets/images/personagemCien.png").convert_alpha()

#variaveis globais
botaoAvancarRect = pygame.Rect(1633, 965, 108, 104)
respondeu = False
score = 0
feedback = ""
areaAtual = None
perguntasAtuais = []
perguntaAtual = 0
tituloQuiz = ""
personagemAtual = None
acertou = False

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
    tela.blit(fundo, (0, 0))

    #balao titulo do jogo
    caixaTitulo = pygame.Rect(0, 0, 730, 100)
    caixaTitulo.center = (largura // 2, 250)
    pygame.draw.rect(tela, (255, 255, 255), caixaTitulo, border_radius=12)

    #titulo jogo
    titulo = fonteTitulo.render("Meninas em STEM: As Goytatecs", True, corFonte)
    titulo_rect = titulo.get_rect(center=caixaTitulo.center)
    tela.blit(titulo, titulo_rect)
    
    botao_largura = 200
    botao_altura = 70
    espaco = 30

    total_largura = (4 * botao_largura) + (3 * espaco)
    x_inicial = (largura - total_largura) // 2  
    y = altura // 2

    global botaoTecnologia, botaoMatematica, botaoEngenharia, botaoCiencia

    botaoTecnologia = pygame.Rect(x_inicial, y, botao_largura, botao_altura)
    botaoMatematica = pygame.Rect(x_inicial + (botao_largura + espaco), y, botao_largura, botao_altura)
    botaoEngenharia = pygame.Rect(x_inicial + 2 * (botao_largura + espaco), y, botao_largura, botao_altura)
    botaoCiencia = pygame.Rect(x_inicial + 3 * (botao_largura + espaco), y, botao_largura, botao_altura)

    pygame.draw.rect(tela, (255,255,255), botaoTecnologia, border_radius=10)
    pygame.draw.rect(tela, (255,255,255), botaoMatematica, border_radius=10)
    pygame.draw.rect(tela, (255,255,255), botaoEngenharia, border_radius=10)
    pygame.draw.rect(tela, (255,255,255), botaoCiencia, border_radius=10)

    # Tecnologia
    textoTec = fonteOpcoes.render("Tecnologia", True, corFonte)
    textoTec_rect = textoTec.get_rect(center=botaoTecnologia.center)
    tela.blit(textoTec, textoTec_rect)

    # Matemática
    textoMat = fonteOpcoes.render("Matemática", True, corFonte)
    textoMat_rect = textoMat.get_rect(center=botaoMatematica.center)
    tela.blit(textoMat, textoMat_rect)

    # Engenharia
    textoEng = fonteOpcoes.render("Engenharia", True, corFonte)
    textoEng_rect = textoEng.get_rect(center=botaoEngenharia.center)
    tela.blit(textoEng, textoEng_rect)

    # Ciências
    textoCien = fonteOpcoes.render("Ciências", True, corFonte)
    textoCien_rect = textoCien.get_rect(center=botaoCiencia.center)
    tela.blit(textoCien, textoCien_rect)

def desenharPergunta(q):
    tela.blit(fundo, (0, 0))

    #personagem do quiz 
    if personagemAtual: 
        tela.blit(personagemAtual, (106, 190))

    #balao da pergunta
    tela.blit(balaoTitulo, (640, 18))

    #titulo quiz
    tituloSurface = fonteTitulo.render(tituloQuiz, True, corFonte)
    tituloRect = tituloSurface.get_rect(center=(960, 52))
    tela.blit(tituloSurface, tituloRect)

    #balao pergunta
    tela.blit(balaoPergunta, (120, 750))

    #botao avancar
    if respondeu:
        tela.blit(botaoAvancar, botaoAvancarRect)

    #decoracao estrela
    tela.blit(decoracaoEstrela, (1740, 870))

    if not respondeu:
        textoMostrar = q["pergunta"]
        corTexto = corFonte
    else:
        textoMostrar = feedback
        corTexto = (0, 150, 0) if acertou else (180, 0, 0)

    draw_text_wrapped(tela, textoMostrar, corTexto, pygame.Rect(160, 850, 1600, 210), fontePergunta)

    #desenha opções
    posicoes_y = [167, 307, 447, 587]
    for i, opcao in enumerate(q["opcoes"]): 
        y_pos = posicoes_y[i]

        # desenhar balão PNG
        tela.blit(botaoOpcao, (649, y_pos))

        # texto dentro do balão
        draw_text_wrapped(
            tela,
            opcao,
            corFonte,
            pygame.Rect(
                669,              # margem interna X
                y_pos + 15,       # margem interna Y
                974,              # largura interna
                80                # altura interna
            ),
            fonteOpcoes,
        line_spacing=2
        )

def desenharResultado():
    tela.blit(fundoInicial, (0, 0))

    # Caixa resultado
    caixaResultado = pygame.Rect(0, 0, 800, 120)
    caixaResultado.center = (largura // 2, 250)
    pygame.draw.rect(tela, (255,255,255), caixaResultado, border_radius=12)

    resultadoSurface = fonteTitulo.render(
        f"Quiz finalizado! Pontuação: {score}/{len(perguntasAtuais)}",
        True,
        corFonte
    )
    tela.blit(resultadoSurface, resultadoSurface.get_rect(center=caixaResultado.center))

    # Botões
    larguraBotao = 300
    alturaBotao = 70
    espaco = 40

    global botaoJogarNovamente, botaoVoltarInicio

    botaoJogarNovamente = pygame.Rect(0, 0, larguraBotao, alturaBotao)
    botaoJogarNovamente.center = (largura // 2, 400)

    botaoVoltarInicio = pygame.Rect(0, 0, larguraBotao, alturaBotao)
    botaoVoltarInicio.center = (largura // 2, 400 + alturaBotao + espaco)

    pygame.draw.rect(tela, (255,255,255), botaoJogarNovamente, border_radius=10)
    pygame.draw.rect(tela, (255,255,255), botaoVoltarInicio, border_radius=10)

    textoJogar = fonteOpcoes.render("Jogar Novamente", True, corFonte)
    textoVoltar = fonteOpcoes.render("Voltar ao Início", True, corFonte)

    tela.blit(textoJogar, textoJogar.get_rect(center=botaoJogarNovamente.center))
    tela.blit(textoVoltar, textoVoltar.get_rect(center=botaoVoltarInicio.center))

        
def checkClickPerguntas(posicao_click):
    global score, perguntaAtual, feedback, estadoJogo, respondeu, acertou

    pergunta = perguntasAtuais[perguntaAtual]

    posicoes_y = [167, 307, 447, 587]

    for i in range(4):
        botao_area = pygame.Rect(
            649,
            posicoes_y[i],
            1014,
            112
        )

        if botao_area.collidepoint(posicao_click) and not respondeu:

            respondeu = True

            # Acertou
            if i == pergunta["resposta"]:
                score += 1
                acertou = True
            else:
                acertou = False

            feedback = pergunta["justificativas"][i]
            break

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
                tituloQuiz = "Quiz de Tecnologia"
                personagemAtual = personagemTecnologia
                score = 0
                estadoJogo = "jogo"

            elif botaoMatematica.collidepoint(mouse):
                areaAtual = "matematica"
                perguntasAtuais = perguntas["matematica"]
                perguntaAtual = 0
                tituloQuiz = "Quiz de Matemática"
                personagemAtual = personagemTecnologia
                score = 0
                estadoJogo = "jogo"

            elif botaoEngenharia.collidepoint(mouse):
                areaAtual = "engenharia"
                perguntasAtuais = perguntas["engenharia"]
                perguntaAtual = 0
                tituloQuiz = "Quiz de Engenharia"
                personagemAtual = personagemEngenharia
                score = 0
                estadoJogo = "jogo"

            elif botaoCiencia.collidepoint(mouse):
                areaAtual = "ciencia"
                perguntasAtuais = perguntas["ciencia"]
                perguntaAtual = 0
                tituloQuiz = "Quiz de Ciências"
                personagemAtual = personagemCiencia
                score = 0
                estadoJogo = "jogo"

        elif estadoJogo == "jogo" and evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            #tenta clicar nas opcaos
            checkClickPerguntas(mouse)

            # depois verifica botão avançar
            if respondeu and botaoAvancarRect.collidepoint(mouse):
                perguntaAtual += 1
                respondeu = False
                feedback = ""

                if perguntaAtual >= len(perguntasAtuais):
                    estadoJogo = "resultado"

        elif estadoJogo == "resultado" and evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if botaoJogarNovamente.collidepoint(mouse):
                perguntaAtual = 0
                score = 0
                respondeu = False
                feedback = ""
                estadoJogo = "jogo"

            elif botaoVoltarInicio.collidepoint(mouse):
                estadoJogo = "tela_inicial"

    #telas
    if estadoJogo == "jogo":
        desenharPergunta(perguntasAtuais[perguntaAtual])

    elif estadoJogo == "resultado":
        desenharResultado()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()