from utils import (
    clicar,
    clicar_coordenada,
    esperar,
    esperar_primeiro,
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

        if existe("tag_arquivado"):
            pressionar("esc")
            log(f"Produto já está arquivado. Pulando para o próximo item.")
            clicar_coordenada(*COORDENADAS["recarregar_pagina"])
            log(f"Recarregando a página para atualizar a lista de produtos.")
            esperar("linha_0_lista_produtos", timeout=5)
            continue
            
        i += 1
        if not clicar("tres_pontos_produto"):
            log("Não foi possível localizar os três pontos.", nivel="error")
            break

        if not clicar("botao_excluir_produto"):
            log("Não foi possível localizar o botão de Excluir.", nivel="error")
            break

        proximo_estado = esperar_primeiro(
            ("exclusao_bloqueada", "botao_confirmar_acao"),
            timeout=6,
        )

        if proximo_estado == "exclusao_bloqueada":
            clicar_coordenada(*COORDENADAS["botao_arquivar_produto_popup"])
            if clicar("botao_confirmar_acao", timeout=2):
                log(f"Produto n°{i} arquivado com sucesso.")
            else:
                log(f"Produto n°{i} não pôde ser arquivado.", nivel="error")
                break
        elif proximo_estado == "botao_confirmar_acao":
            if clicar("botao_confirmar_acao", timeout=2):
                log(f"Produto n°{i} excluído com sucesso.")
            else:
                log(f"Produto n°{i} não pôde ser excluído.", nivel="error")
                break
        else:
            log(f"Produto n°{i}: nenhuma ação de exclusão apareceu.", nivel="error")
            break

        if esperar("titulo_tabela_produtos", timeout=6) is None:
            log("A lista de produtos não voltou.", nivel="error")
            break
        # garante que o item foi realmente removido da tela antes de continuar
        esperar_sumir("linha_azul", timeout=3)
        
except Exception as e:
    log(f"Ocorreu um erro inesperado: {e}", nivel="error")
    raise
finally:
    log(f"Automação finalizada. Total de Itens processados: {i} itens.")
