# -*- coding: utf-8 -*-
"""Painel de saída para o BOT E-ESTADO. Somente apresentação; sem automação."""
from __future__ import annotations

import builtins
import ctypes
import os
import re
import shutil
import sys
import threading
import textwrap
import time
from datetime import datetime


class PainelTerminal:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    MUTED = "\033[90m"
    BOLD = "\033[1m"

    def __init__(self):
        # UTF-8 também quando o .exe for chamado diretamente fora do inicializador.
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass
        self._lock = threading.RLock()
        self._start = time.monotonic()
        self._color = self._enable_colors()
        self._header = False
        self._page = None
        self._pages = 0
        self._current_id = None
        self._attempts = 0
        self._requested = 0
        self._blocked = set()
        self._ignored = set()
        self._errors = 0
        self._width = max(70, min(94, shutil.get_terminal_size((94, 35)).columns - 2))
        self._detailed = os.getenv("EESTADO_LOG_DETALHADO") == "1"

    def _enable_colors(self):
        if not sys.stdout.isatty() or os.getenv("NO_COLOR"):
            return False
        if os.name != "nt":
            return True
        try:
            output = ctypes.windll.kernel32.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            if not ctypes.windll.kernel32.GetConsoleMode(output, ctypes.byref(mode)):
                return False
            return bool(ctypes.windll.kernel32.SetConsoleMode(output, mode.value | 4))
        except Exception:
            return False

    def _c(self, text, color):
        return color + str(text) + self.RESET if self._color else str(text)

    def _raw(self, line=""):
        builtins.print(line, flush=True)

    def _line(self, color=None, character="─"):
        rule = character * min(self._width, 92)
        self._raw(" " + self._c(rule, color or self.MUTED))

    def _stamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def _entry(self, tag, message, color=None):
        color = color or self.CYAN
        chunks = textwrap.wrap(
            str(message), width=max(45, self._width - 24),
            break_long_words=False, break_on_hyphens=False
        ) or [""]
        prefix = self._c(self._stamp(), self.MUTED)
        label = self._c(f"{tag:<9}", color)
        self._raw(f"  {prefix}  {label} {chunks[0]}")
        for chunk in chunks[1:]:
            self._raw(f"  {' '*8}  {' '*9} {self._c(chunk, self.MUTED)}")

    def _section(self, text):
        self._raw()
        self._line(self.MUTED)
        self._raw("  " + self._c(text, self.BOLD + self.WHITE))
        self._line(self.MUTED)

    def _hero(self):
        if self._header:
            return
        self._header = True
        self._raw()
        self._line(self.CYAN, "═")
        self._raw("  " + self._c("E  -  E S T A D O", self.BOLD + self.CYAN))
        self._raw("  " + self._c("CONFERÊNCIA E RECLASSIFICAÇÃO DE BENS", self.WHITE))
        self._raw("  " + self._c("SESDEC · NPA    |    Painel de acompanhamento", self.MUTED))
        self._line(self.CYAN, "═")
        self._entry("CONTROLE", "ESC interrompe a automação; acompanhe o E-ESTADO durante a execução.", self.MAGENTA)

    def _page_start(self, number):
        if self._page is not None and self._page != number:
            self._raw()
        self._page = number
        self._pages += 1
        self._section(f"PÁGINA {number:02d}  /  Conferência patrimonial")

    def _item_start(self, number, item_id):
        self._attempts += 1
        self._current_id = item_id
        self._raw()
        self._raw("  " + self._c("●", self.CYAN) + " " +
                  self._c(f"BEM {item_id}", self.BOLD + self.WHITE) +
                  self._c(f"   •   item {number} nesta página", self.MUTED))
        self._entry("INICIADO", "Preparando reclassificação", self.BLUE)

    def _ignored_item(self, reason):
        item_id = self._current_id
        if item_id and item_id not in self._blocked:
            self._ignored.add(item_id)
        self._entry("ATENÇÃO", reason, self.YELLOW)

    def _blocking(self):
        if self._current_id:
            self._blocked.add(self._current_id)
        self._entry("BLOQUEADO", f"Bem {self._current_id or '?'}: bloqueio informado pelo sistema. Não conferir.", self.YELLOW)

    def _report(self, success=True):
        duration = int(time.monotonic() - self._start)
        minutes, seconds = divmod(duration, 60)
        self._section("RESUMO DA EXECUÇÃO")
        self._raw(f"  {self._c('Páginas visitadas', self.MUTED):<22} {self._pages}" if not self._color else
                  f"  {self._c('Páginas visitadas', self.MUTED)}: {self._pages}")
        self._raw("  " + self._c("Itens iniciados", self.MUTED) + f": {self._attempts}")
        self._raw("  " + self._c("Conferências acionadas", self.GREEN) + f": {self._requested}")
        self._raw("  " + self._c("Bens bloqueados", self.YELLOW) + f": {len(self._blocked)}")
        self._raw("  " + self._c("Outros itens ignorados", self.YELLOW) + f": {len(self._ignored)}")
        self._raw("  " + self._c("Tempo decorrido", self.MUTED) + f": {minutes:02d}min {seconds:02d}s")
        self._line(self.CYAN, "═")
        if success:
            self._entry("FINALIZADO", "Rotina terminou. Confirme os resultados no E-ESTADO.", self.GREEN)
        else:
            self._entry("INTERROMP.", "Execução interrompida; confira os avisos exibidos acima.", self.RED)
        self._raw()

    def registrar(self, *args, sep=" ", end="\n", file=None, flush=False):
        """Substituto apenas dos prints do robô; NÃO modifica nenhum clique ou regra."""
        if file is not None and file is not sys.stdout:
            return builtins.print(*args, sep=sep, end=end, file=file, flush=flush)
        raw = sep.join(str(a) for a in args)
        with self._lock:
            if not self._header:
                self._hero()
            # Preserva mensagens inesperadas/diagnóstico em um formato legível.
            lines = raw.splitlines()
            if not lines:
                return
            for line in lines:
                value = line.strip()
                if value:
                    self._route(value)

    def _route(self, msg):
        if re.fullmatch(r"[=+\- ]{10,}", msg):
            return
        if msg.startswith("Robô iniciado.") or msg.startswith("3. Iniciando Loop"):
            return
        if msg.startswith("Tentando se conectar ao Chrome"):
            self._entry("CONEXÃO", "Conectando ao Chrome · porta 9222", self.BLUE)
        elif "Conexão estabelecida com sucesso" in msg:
            self._entry("OK", "Chrome conectado.", self.GREEN)
        elif msg.startswith("Assumindo o controle da página"):
            self._entry("NAVEGADOR", "E-ESTADO identificado. Iniciando leitura.", self.GREEN)
        elif msg.startswith("[HISTÓRICO]"):
            self._entry("HISTÓRICO", msg.replace("[HISTÓRICO]", "").strip(), self.MAGENTA)
        elif msg.startswith("[INÍCIO]"):
            self._entry("PÁGINA", re.sub(r"^\[INÍCIO\]\s*", "", msg), self.MUTED)
        elif "INICIANDO PROCESSAMENTO DA PÁGINA Nº" in msg:
            match = re.search(r"Nº\s*(\d+)", msg)
            if match:
                self._page_start(int(match.group(1)))
        elif msg.startswith("--- [FIM ITENS]"):
            self._entry("PÁGINA", "Não há mais itens pendentes selecionáveis nesta página.", self.MUTED)
        elif msg.startswith("[FIM ITENS]"):
            self._entry("PÁGINA", "Itens restantes ignorados por segurança.", self.YELLOW)
        elif msg.startswith("ID/identificador do bem:") or msg.startswith("Forçando rolagem"):
            return
        elif msg.startswith("--- Processando Item"):
            m = re.search(r"Item\s+(\d+)\s+\(ID:\s*(.+?)\)\s*---", msg)
            if m:
                self._item_start(int(m.group(1)), m.group(2))
        elif "Rolando a tela" in msg or "Pausa de 1 segundo" in msg:
            return
        elif "Clicando em 'Reclassificar'" in msg:
            self._entry("ETAPA 1/3", "Abrindo a reclassificação...", self.CYAN)
        elif "Aguardando o modal aparecer" in msg or "Modal abriu. Preenchendo" in msg:
            return
        elif msg.startswith("Selecionando opções"):
            self._entry("CAMPOS", "Servível · Localizado · Uso e usufruto · Bom", self.BLUE)
        elif "Clicando em 'Salvar'" in msg:
            self._entry("ETAPA 2/3", "Enviando reclassificação...", self.CYAN)
        elif "Aguardando resposta do servidor" in msg:
            self._entry("SISTEMA", "Aguardando resposta do E-ESTADO...", self.MUTED)
        elif "ERRO DETECTADO: BEM BLOQUEADO" in msg:
            self._blocking()
        elif "adicionado à lista de pulo" in msg:
            return
        elif "Clicando no botão vermelho 'Fechar'" in msg:
            self._entry("FECHANDO", "Fechando a janela do bem bloqueado...", self.BLUE)
        elif "Janela fechada e conferida" in msg:
            self._entry("OK", "Janela fechada. Prosseguindo sem conferir o bem.", self.GREEN)
        elif "Salvamento bem-sucedido. Clicando" in msg:
            self._entry("SISTEMA", "Sem aviso de bloqueio; verificando o fechamento da janela.", self.MUTED)
        elif "Modal de preenchimento fechado" in msg:
            self._entry("OK", "Janela de reclassificação fechada.", self.GREEN)
        elif "Conferindo especificamente o bem" in msg:
            self._entry("ETAPA 3/3", "Acionando Conferir apenas para este bem...", self.CYAN)
        elif "Esperando o item ser processado e sumir da lista" in msg:
            self._requested += 1
            self._entry("ACIONADO", "Conferência solicitada; aguardando atualização da lista.", self.GREEN)
        elif "Esperando o primeiro item da nova página" in msg or "Verificando se há próxima página" in msg:
            return
        elif "[PAGINAÇÃO] Movendo para a página" in msg:
            next_page = re.search(r"página\s+(\d+)", msg)
            self._entry("PRÓXIMA", f"Avançando para a página {next_page.group(1) if next_page else '?'}...", self.BLUE)
        elif msg.startswith("[FIM] Botão 'Próximo'"):
            self._entry("PÁGINAS", "Última página alcançada.", self.MUTED)
        elif msg.startswith("[SUCESSO] Processamento"):
            self._report(success=True)
        elif msg.startswith("Fechando a conexão com o navegador"):
            return
        elif "TECLA ESC ACIONADA" in msg:
            self._entry("PARADA", "ESC acionado. Encerramento solicitado.", self.RED)
        elif msg.startswith("Encerrando a execução por comando"):
            self._report(success=False)
        elif "Modal de Reclassificação NÃO ABRIU" in msg:
            self._ignored_item("Janela não abriu; este bem foi ignorado.")
        elif "Salvamento não confirmado" in msg or "Sistema exibiu erro após salvar" in msg:
            self._ignored_item(msg.replace("[AVISO]", "").strip())
        elif "Conferência não segura ou indisponível" in msg:
            motivo = msg.partition("Conferência não segura ou indisponível:")[2].strip().splitlines()[0]
            self._ignored_item(f"Conferência não efetuada: {motivo[:210] or 'não foi possível identificar o botão.'}")
            if self._detailed:
                self._entry("DETALHE", msg, self.MUTED)
        elif "Item ainda pode estar pendente" in msg:
            self._ignored_item("O bem ainda aparece como pendente; revise no sistema.")
        elif msg.startswith("[ERRO FATAL") or msg.startswith("[ERRO]"):
            self._errors += 1
            self._entry("ERRO", msg, self.RED)
            self._report(success=False)
        elif "[AVISO]" in msg or msg.lower().startswith("aviso:"):
            self._entry("ATENÇÃO", msg.replace("[AVISO]", "").strip(), self.YELLOW)
        elif "ERRO" in msg.upper() or "FALHA" in msg.upper():
            self._entry("ERRO", msg, self.RED)
        else:
            if self._detailed:
                self._entry("DETALHE", msg, self.MUTED)


painel = PainelTerminal()
