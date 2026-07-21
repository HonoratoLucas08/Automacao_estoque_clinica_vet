import pyautogui
import time
import logging
import os

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

from config import (
    PASTA_IMAGENS,
    CONFIANCA_PADRAO,
    TIMEOUT_PADRAO,
    INTERVALO_POLL,
)


logging.basicConfig(
    filename="logs/automacao.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def _caminho(elemento):
    if elemento.endswith(".png"):   
        return os.path.join(PASTA_IMAGENS, elemento)
    return os.path.join(PASTA_IMAGENS, f"{elemento}.png")


def existe(elemento, confianca=CONFIANCA_PADRAO):
    try:
        return pyautogui.locateOnScreen(
            _caminho(elemento),
            confidence=confianca
        ) is not None
    except pyautogui.ImageNotFoundException:
        return False


# espera ate que a imagem apareça ou o tempo limite seja atingido e retorna a posição
def esperar(elemento, timeout=TIMEOUT_PADRAO, confianca=CONFIANCA_PADRAO):
    tempo_inicio = time.time()

    while time.time() - tempo_inicio < timeout:
        try:
            pos = pyautogui.locateOnScreen(
                _caminho(elemento),
                confidence=confianca
            )
            return pos
        except pyautogui.ImageNotFoundException:
            time.sleep(INTERVALO_POLL)

    return None


def esperar_sumir(elemento, timeout=TIMEOUT_PADRAO, confianca=CONFIANCA_PADRAO):
    tempo_inicio = time.time()
    while time.time() - tempo_inicio < timeout:
        if not existe(elemento, confianca):
            return True
        time.sleep(INTERVALO_POLL)
    return False


def clicar(elemento, timeout=TIMEOUT_PADRAO, confianca=CONFIANCA_PADRAO):
    pos = esperar(elemento, timeout, confianca)
    if pos is None:
        log(f"Não foi possível clicar em '{elemento}': elemento não encontrado", nivel="error")
        return False
    centro = pyautogui.center(pos)
    pyautogui.click(centro)
    log(f"Clicou em '{elemento}' ({centro.x},{centro.y})")
    return True


def clicar_coordenada(x, y):
    pyautogui.click(x, y)
    log(f"Clicou na coordenada fixa ({x},{y})")


def log(texto, nivel="info"):
    print(f"LOG: {texto}")
    getattr(logging, nivel)(texto)


def escrever(texto):
    pyautogui.write(str(texto))


def pressionar(tecla):
    pyautogui.press(tecla)
