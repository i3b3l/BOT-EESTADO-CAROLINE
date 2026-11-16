# ============================================================
# FEITO COM <3 POR IZABEL GALVAO :3
# ATUALIZACOES NO MEU GITHUB: https://github.com/i3b3l
# ============================================================

# ===============================================
# BIBLIOTECAS UTILIZADAS
# ===============================================
from playwright.sync_api import sync_playwright, TimeoutError
import pyautogui
import keyboard
import time
import sys
import re # Nova biblioteca para expressões regulares (usada na checagem de página)
import hashlib

# Camada visual isolada: preserva todas as ações do robô.
from painel_terminal import painel
from historico_bloqueios import HistoricoBloqueios
from seletor_conferir import localizar_botao_conferir
print = painel.registrar

# ===============================================
# VARIÁVEIS DE CONFIGURAÇÃO
# ===============================================
robo_deve_parar = False
CHROME_DEBUG_URL = "http://localhost:9222"
tecla_de_panico = "Esc"
NOME_DO_DEPARTAMENTO = "SESDEC-NPA"

### Histórico permanente: ID bloqueado não será repetido em novas execuções.
historico_bloqueios = HistoricoBloqueios()
ids_bloqueados_a_pular = historico_bloqueios.carregar()
print(f"[HISTÓRICO] {len(ids_bloqueados_a_pular)} bens bloqueados carregados de bens_bloqueados.json.")

# ===============================================
# FUNÇÕES DE SEGURANÇA E PÂNICO
# ===============================================
def parar_execucao():
    """Função chamada pela tecla de pânico."""
    global robo_deve_parar
    print("\n!!! TECLA ESC ACIONADA! ENCERRANDO AUTOMACAO !!!")
    robo_deve_parar = True

def verificar_panico_e_sair():
    """Verifica se a tecla de pânico foi acionada e encerra o script."""
    global robo_deve_parar
    if robo_deve_parar:
        print("Encerrando a execução por comando de pânico.")
        pyautogui.alert('Tecla ESC acionada. Automação encerrada.', title='Pânico Acionado')
        sys.exit()

# Adiciona a tecla de pânico ao teclado
try:
    keyboard.add_hotkey(tecla_de_panico, parar_execucao)
except Exception as erro_atalho:
    print(f"[AVISO] Atalho ESC indisponível: {erro_atalho}. Use Ctrl+C no terminal.")
print(f"Robô iniciado. Pressione a tecla '{tecla_de_panico}' a qualquer momento para abortar com seguranca.")

# Aviso inicial para o usuário
pyautogui.confirm(text='Aperte OK quando o E-ESTADO estiver logado na página inicial no depurador do Google Chrome', title='Depurador do Chrome' , buttons=['OK'])

# ===============================================
# INÍCIO DA AUTOMAÇÃO
# ===============================================
with sync_playwright() as p:
    try:
        verificar_panico_e_sair()

        # CONECTAR AO NAVEGADOR JÁ ABERTO:
        print(f"Tentando se conectar ao Chrome na porta de depuração: {CHROME_DEBUG_URL}")
        browser = p.chromium.connect_over_cdp(CHROME_DEBUG_URL)
        print("Conexão estabelecida com sucesso!")

        # OBTER A PÁGINA DO E-ESTADO:
        janela = browser.contexts[0]

        if not janela.pages:
            raise Exception("Nenhuma página encontrada na instância de depuração do Chrome.")

        guia = next((page for page in janela.pages if "e-estado.ro.gov.br" in page.url), janela.pages[0])
        print(f"Assumindo o controle da página com o título: '{guia.title()}'")

        guia.wait_for_load_state('domcontentloaded', timeout=30000)

        # ----------------------------------------------------
        # 3. LOOP DE PROCESSAMENTO E PAGINAÇÃO (CORREÇÃO DE ESTABILIDADE E INDENTAÇÃO)
        # ----------------------------------------------------

        print("\n3. Iniciando Loop de Processamento e Paginação...")

        # SELETORES
        SELETOR_PROXIMA_PAGINA = 'li.page-item:not(.disabled) button[aria-label="Go to next page"]'
        SELETOR_PAGINA_ATIVA = 'li.page-item.active button[aria-label^="Go to page"]'
        SELETOR_LINHAS_A_PROCESSAR = 'tr:has-text("NÃO CONFERIDO"):has-text("NÃO RECLASSIFICADO")'
        SELETOR_MODAL_DIALOG = '[role="dialog"]'

        # === LÓGICA PARA ENCONTRAR A PÁGINA ATUAL CORRETAMENTE ===
        try:
            botao_pagina_ativa = guia.locator(SELETOR_PAGINA_ATIVA).first
            aria_label_pagina = botao_pagina_ativa.get_attribute("aria-label")
            match = re.search(r'page (\d+)', aria_label_pagina)
            if match:
                pagina_atual = int(match.group(1))
                print(f"[INÍCIO] Robô detectou que a página atual é a: {pagina_atual}")
            else:
                pagina_atual = 1
                print("[INÍCIO] Não foi possível ler a página ativa. Assumindo a página 1.")
        except:
            pagina_atual = 1
            print("[INÍCIO] Erro ao buscar o seletor da página ativa. Assumindo a página 1.")
        # ===============================================================

        # Inicia o loop externo de páginas
        while True:
            verificar_panico_e_sair()
            print(f"\n=======================================================")
            print(f"| INICIANDO PROCESSAMENTO DA PÁGINA Nº {pagina_atual} |")
            print(f"=======================================================")

            # ----------------------------------------------------
            # Loop interno: PROCESSAMENTO DE ITENS
            # ----------------------------------------------------

            itens_processados_nesta_pagina = 0
            itens_ignorados_nesta_pagina = set()
            bloqueados_exibidos_nesta_pagina = set()
            while True:
                verificar_panico_e_sair()

                # 1. TENTATIVA DE LOCALIZAÇÃO DO PRÓXIMO ITEM PENDENTE
                todos_itens_pendentes = guia.locator(SELETOR_LINHAS_A_PROCESSAR)

                time.sleep(2.0) # Pausa de 2s para estabilidade da lista

                if todos_itens_pendentes.count() == 0:
                    print(f"--- [FIM ITENS] Contagem zero de itens pendentes. Processados {itens_processados_nesta_pagina} itens nesta página. ---")
                    break # <--- SAI IMEDIATAMENTE do loop interno (de itens)

                # Escolhe um item pendente AINDA NÃO IGNORADO nesta página.
                # Assim um bem bloqueado não mantém o loop preso na primeira linha.
                proximo_item = None
                id_do_bem_atual = None
                for indice in range(todos_itens_pendentes.count()):
                    candidato = todos_itens_pendentes.nth(indice)
                    try:
                        texto_linha = candidato.inner_text(timeout=3000)
                        texto_id = candidato.locator("p.font-responsive strong").first.text_content(timeout=1000)
                        encontrado = re.search(r'(\d{5,})', texto_id or "")
                        identidade = encontrado.group(1) if encontrado else "linha:" + hashlib.sha256(texto_linha.encode("utf-8")).hexdigest()[:20]
                        if identidade in ids_bloqueados_a_pular:
                            if identidade not in bloqueados_exibidos_nesta_pagina:
                                print(f"[HISTÓRICO] Bem {identidade} já bloqueado anteriormente: pulando sem reclassificar.")
                                bloqueados_exibidos_nesta_pagina.add(identidade)
                            continue
                        if identidade in itens_ignorados_nesta_pagina:
                            continue
                        proximo_item = candidato
                        id_do_bem_atual = identidade
                        break
                    except Exception as erro_linha:
                        print(f"    [AVISO] Não foi possível identificar a linha {indice + 1}: {erro_linha}")
                        continue

                if proximo_item is None:
                    print("[FIM ITENS] Todos os itens restantes foram ignorados ou não podem ser identificados.")
                    break
                print(f"    ID/identificador do bem: {id_do_bem_atual}")

                # Se não está na lista, continua o processamento...

                print("    Forçando rolagem da página para o topo...")
                guia.evaluate("window.scrollTo(0, 0)")
                time.sleep(0.5)

                itens_processados_nesta_pagina += 1
                print(f"--- Processando Item {itens_processados_nesta_pagina} (ID: {id_do_bem_atual}) ---")

                # 2. Localiza o botão 'Reclassificar'
                alvo_reclassificar = proximo_item.get_by_role("button", name="Reclassificar")

                alvo_reclassificar.wait_for(state="visible", timeout=5000)

                print("    Rolando a tela para garantir a visibilidade do item...")
                alvo_reclassificar.scroll_into_view_if_needed()

                time.sleep(2.0) # Pausa maior (2s) para o navegador estabilizar.

                # 3. CLIQUE 7: RECLASSIFICAR
                print("    Clicando em 'Reclassificar'...")
                alvo_reclassificar.click(force=True, timeout=10000)

                # ----------------------------------------------------
                # 4. PREENCHIMENTO DO MODAL E DETECÇÃO DE ERRO
                # ----------------------------------------------------

                print("    Aguardando o modal aparecer...")
                try:
                    guia.locator(SELETOR_MODAL_DIALOG).wait_for(state="visible", timeout=10000)
                except TimeoutError:
                    print("[ERRO FATAL] Modal de Reclassificação NÃO ABRIU. (Bug do último item?).")
                    itens_ignorados_nesta_pagina.add(id_do_bem_atual)
                    continue # Pula esta iteração

                print("    Modal abriu. Preenchendo campos...")
                time.sleep(2.0) # Pausa para os campos carregarem

                print("    Selecionando opções...")
                seletores_dropdown = guia.locator(SELETOR_MODAL_DIALOG).locator('select')

                seletores_dropdown.nth(0).select_option(label="Servível", force=True)
                time.sleep(0.2)
                seletores_dropdown.nth(1).select_option(label="Localizado", force=True)
                time.sleep(0.2)
                seletores_dropdown.nth(2).select_option(label="Uso e usufruto do bem", force=True)
                time.sleep(0.2)
                seletores_dropdown.nth(3).select_option(label="Bom", force=True)
                time.sleep(0.2)

                verificar_panico_e_sair()

                # ----------------------------------------------------
                # 5. LÓGICA DE SALVAMENTO (ERRO vs SUCESSO)
                # ----------------------------------------------------

                print("    Clicando em 'Salvar'...")
                guia.locator(SELETOR_MODAL_DIALOG).get_by_role("button", name="Salvar").click()

                # Pausa CRÍTICA: Espera 3 segundos para o TOAST de erro aparecer
                print("    Aguardando resposta do servidor (Erro ou Sucesso)...")
                time.sleep(3.0)

                SELETOR_TOAST_BLOQUEADO = 'div.toast-message:has-text("este bem está bloqueado")'

                if guia.locator(SELETOR_TOAST_BLOQUEADO).is_visible():
                    # --- CENÁRIO DE ERRO (O TOAST APARECEU) ---
                    print("\n!!! ERRO DETECTADO: BEM BLOQUEADO. PULANDO ESTE ITEM. !!!")

                    # Persiste IDs numéricos confirmados como bloqueados.
                    # Se a gravação falhar, interrompe: não perder histórico silenciosamente.
                    if id_do_bem_atual not in ids_bloqueados_a_pular:
                        if historico_bloqueios.registrar(id_do_bem_atual):
                            print(f"[HISTÓRICO] Bem {id_do_bem_atual} registrado em bens_bloqueados.json.")
                        else:
                            print(f"[HISTÓRICO] Bem {id_do_bem_atual} sem ID numérico estável: bloqueio apenas nesta execução.")
                        ids_bloqueados_a_pular.add(id_do_bem_atual)

                    # Fechar a janela de reclassificação pelo botão vermelho informado.
                    # O E-ESTADO pode manter o modal no DOM depois de ocultá-lo;
                    # portanto, devemos esperar "hidden", não "detached".
                    print("    Clicando no botão vermelho 'Fechar' da janela aberta...")
                    modal_visivel = guia.locator(f'{SELETOR_MODAL_DIALOG}:visible')
                    botao_fechar = modal_visivel.locator(
                        'button.btn.btn-danger:visible'
                    ).filter(has_text=re.compile(r'^\s*Fechar\s*$', re.I))
                    if botao_fechar.count() == 0:
                        # Compatibilidade com páginas cujo botão está fora do role=dialog.
                        botao_fechar = guia.locator(
                            'button.btn.btn-danger:visible'
                        ).filter(has_text=re.compile(r'^\s*Fechar\s*$', re.I))

                    if botao_fechar.count() != 1:
                        raise RuntimeError(
                            f"Não é seguro fechar a janela: encontrados {botao_fechar.count()} botões vermelhos 'Fechar' visíveis."
                        )

                    botao_fechar.click(timeout=7000)
                    try:
                        botao_fechar.wait_for(state="hidden", timeout=10000)
                        modal_visivel.wait_for(state="hidden", timeout=10000)
                        print("    Janela fechada e conferida. Bem bloqueado ignorado.")
                    except TimeoutError as erro_fechamento:
                        raise RuntimeError(
                            "O botão Fechar foi acionado, mas a janela continua aberta. "
                            "Automação interrompida para não operar outro bem com modal pendente."
                        ) from erro_fechamento

                    continue # Pula para o próximo item (NÃO CLICA EM CONFERIR)

                else:
                    # --- CENÁRIO DE SUCESSO (Nenhum toast de erro apareceu) ---
                    print("    Salvamento bem-sucedido. Clicando em 'Conferir'...")

                    # O modal deve FECHAR para considerar a gravação confirmada na interface.
                    try:
                        guia.locator(SELETOR_MODAL_DIALOG).wait_for(state="hidden", timeout=10000)
                        print("    Modal de preenchimento fechado.")
                    except TimeoutError:
                        print("    [AVISO] Salvamento não confirmado: o modal continua aberto. Ignorando bem.")
                        itens_ignorados_nesta_pagina.add(id_do_bem_atual)
                        continue

                    # Verifica erros genéricos, não apenas o aviso de bloqueio.
                    erros_visiveis = guia.locator('div.toast-message, [role="alert"]')
                    erro_encontrado = False
                    for aviso in erros_visiveis.all():
                        try:
                            if aviso.is_visible() and re.search(r'erro|falha|inválid|obrigatóri|não foi possível|bloquead', aviso.inner_text(), re.I):
                                erro_encontrado = True
                                break
                        except Exception:
                            pass
                    if erro_encontrado:
                        print("    [AVISO] Sistema exibiu erro após salvar. Bem ignorado para conferência.")
                        itens_ignorados_nesta_pagina.add(id_do_bem_atual)
                        continue

                    # Seleciona o botão exato (btn btn-info btn-sm) da linha deste ID.
                    # Nunca usa o primeiro botão Conferir de outra linha.
                    try:
                        alvo_conferir = localizar_botao_conferir(guia, id_do_bem_atual)
                        alvo_conferir.scroll_into_view_if_needed(timeout=5000)
                        print(f"    Conferindo especificamente o bem {id_do_bem_atual}...")
                        alvo_conferir.click(timeout=10000)
                    except Exception as erro_conferencia:
                        print(f"    [AVISO] Conferência não segura ou indisponível: {erro_conferencia}")
                        itens_ignorados_nesta_pagina.add(id_do_bem_atual)
                        continue

                    guia.wait_for_load_state('domcontentloaded', timeout=30000)

                    # Espera o item sumir da lista
                    print("    Esperando o item ser processado e sumir da lista...")
                    try:
                        # alvo_reclassificar foi definido no início do loop do item
                        guia.locator(SELETOR_LINHAS_A_PROCESSAR).filter(
                            has_text=id_do_bem_atual if not id_do_bem_atual.startswith("linha:") else ""
                        ).first.wait_for(state="hidden", timeout=10000)
                    except TimeoutError:
                        print("[AVISO] Item ainda pode estar pendente após a conferência. Ignorando nesta página.")
                        itens_ignorados_nesta_pagina.add(id_do_bem_atual)

                    print("    Pausa de 1 segundo para estabilização da lista...")
                    time.sleep(1.0)

                    verificar_panico_e_sair()

            # ----------------------------------------------------
            # 6. LÓGICA DE PAGINAÇÃO
            # ----------------------------------------------------

            print("[PAGINAÇÃO] Verificando se há próxima página...")

            proxima_pagina_locator = guia.locator(SELETOR_PROXIMA_PAGINA).first

            try:
                proxima_pagina_locator.wait_for(state='visible', timeout=5000)

                print(f"[PAGINAÇÃO] Movendo para a página {pagina_atual + 1}...")
                proxima_pagina_locator.click()
                guia.wait_for_load_state('domcontentloaded', timeout=30000)

                print("[PAGINAÇÃO] Esperando o primeiro item da nova página...")
                # A nova página pode legitimamente não conter itens pendentes.
                guia.locator("body").wait_for(state='attached', timeout=10000)

                time.sleep(1)
                pagina_atual += 1

            except TimeoutError:
                print("[FIM] Botão 'Próximo' não encontrado ou desabilitado. Fim de todas as páginas.")
                break # Sai do loop while True (loop de páginas)

        print("\n[SUCESSO] Processamento de todos os páginas concluído.")
        pyautogui.alert('Automação E-ESTADO concluída com sucesso.', title='Automação Concluída', button='OK')

    except TimeoutError as te:
        print(f"\n[ERRO FATAL - TIMEOUT] O tempo de espera por um elemento expirou. {te}")
        pyautogui.alert('O robô falhou por tempo limite. Verifique se a página carregou ou se o seletor está visível.', title='Erro de Automação', button='OK')
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO FATAL] Ocorreu um erro inesperado: {e}")
        pyautogui.alert(f'O robô falhou. Erro: {e}', title='Erro de Automação', button='OK')
        sys.exit(1)
    finally:
        if 'browser' in locals():
            print("Fechando a conexão com o navegador...")
            browser.close()
