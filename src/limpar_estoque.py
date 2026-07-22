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
from config import COORDENADAS
import time

print("Iniciando automação em 5 segundos...")
time.sleep(5)
i = 0
try:
    while True:
        clicar_coordenada(*COORDENADAS["primeira_linha_tabela"])
        tem_item = esperar("informacoes_gerais_produto")

        if tem_item is None:
            log("Não há mais produtos para processar. Encerrando automação.")
            break

        i += 1
        if not clicar("tres_pontos_produto"):
            log("Não foi possível localizar os três pontos.", nivel="error")
            break

        if not clicar("botao_excluir_produto"):
            log("Não foi possível localizar o botão de Excluir.", nivel="error")
            break

        if esperar("exclusao_bloqueada", timeout=3):
            clicar_coordenada(*COORDENADAS["botao_arquivar_produto_popup"])
            clicar("botao_confirmar_acao")
            log(f"Produto n°{i} arquivado com sucesso.")
        else:
            clicar("botao_confirmar_acao")
            log(f"Produto n°{i} excluído com sucesso.")

        if esperar("titulo_tabela_produtos", timeout=6) is None:
            log("A lista de produtos não voltou.", nivel="error")
            break
except Exception as e:
    log(f"Ocorreu um erro inesperado: {e}", nivel="error")
    raise
finally:
    log(f"Automação finalizada. Total de Itens processados: {i} itens.")
