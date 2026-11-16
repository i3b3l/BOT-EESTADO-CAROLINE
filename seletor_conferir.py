# -*- coding: utf-8 -*-
"""Seleção segura do botão Conferir usando o ID do bem. Não executa cliques."""
import re


def localizar_botao_conferir(guia, id_do_bem):
    """Retorna o único botão Conferir na mesma linha do bem numérico informado.

    Não seleciona botões globais. Se não identificar a linha com segurança,
    interrompe a conferência daquele bem.
    """
    identificador = str(id_do_bem)
    if not re.fullmatch(r"\d{5,}", identificador):
        raise RuntimeError("Bem sem ID numérico estável; conferência automática não é segura.")

    # Faz a busca por ID inteiro (evita coincidências parciais entre patrimônios).
    padrao_id = re.compile(r"(?<!\d)" + re.escape(identificador) + r"(?!\d)")

    # Preferência: mesmo elemento usado para extrair o ID antes de reclassificar.
    linhas = guia.locator("tr").filter(
        has=guia.locator("p.font-responsive strong", has_text=padrao_id)
    )
    quantidade = linhas.count()

    # Algumas interfaces mudam o HTML depois de salvar a reclassificação.
    # Só aceita a linha completa se o ID ainda for único.
    if quantidade != 1:
        linhas = guia.locator("tr").filter(has_text=padrao_id)
        quantidade = linhas.count()

    if quantidade != 1:
        raise RuntimeError(
            f"Bem {identificador}: encontrada(s) {quantidade} linha(s) com o ID após salvar; "
            "não clicarei no botão de outro patrimônio."
        )

    linha = linhas.first

    # Correspondência com o botão real do E-ESTADO:
    # <button type="button" class="btn btn-info btn-sm">... Conferir</button>
    botao = linha.locator('button.btn.btn-info.btn-sm:has-text("Conferir")')
    quantidade_botoes = botao.count()
    if quantidade_botoes == 0:
        # Compatibilidade caso a classe visual mude, mas sempre dentro da mesma linha.
        botao = linha.locator('button:has-text("Conferir")')
        quantidade_botoes = botao.count()
    if quantidade_botoes != 1:
        raise RuntimeError(
            f"Bem {identificador}: {quantidade_botoes} botão(ões) Conferir encontrados "
            "dentro da linha do próprio bem."
        )

    botao.wait_for(state="visible", timeout=10000)
    return botao
