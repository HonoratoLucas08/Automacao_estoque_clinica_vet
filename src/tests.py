from utils import (
    clicar,
    clicar_coordenada,
    esperar,
    esperar_sumir,
    existe,
    log,
    escrever,
    pressionar,
)
import time
import pyautogui
from config import COORDENADAS

print("Iniciando teste em 5 segundos...")
time.sleep(5)

# clicar_coordenada(*COORDENADAS["primeira_linha_tabela"])

# # testando a função esperar para verificar se a imagem "informacoes_gerais_produto" aparece na tela - Teste OK
# print(esperar("informacoes_gerais_produto"))