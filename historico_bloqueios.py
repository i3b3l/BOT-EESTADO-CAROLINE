# -*- coding: utf-8 -*-
"""Histórico persistente dos IDs de bens bloqueados no E-ESTADO.

Armazena somente o identificador do bem, data e motivo do bloqueio.
Não altera nenhum status no E-ESTADO.
"""
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path


def pasta_do_programa():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


class HistoricoBloqueios:
    def __init__(self, caminho=None):
        self.caminho = Path(caminho) if caminho else pasta_do_programa() / "bens_bloqueados.json"

    def _ler_registros(self):
        if not self.caminho.exists():
            return []
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8-sig"))
        except (ValueError, UnicodeError, OSError) as erro:
            raise RuntimeError(
                f"Não foi possível ler {self.caminho.name}. "
                "Por segurança, não apagarei o histórico. Verifique o arquivo."
            ) from erro
        if not isinstance(dados, dict) or not isinstance(dados.get("bens_bloqueados"), list):
            raise RuntimeError("Histórico inválido: esperado objeto com lista 'bens_bloqueados'.")
        registros = dados["bens_bloqueados"]
        if any(
            not isinstance(item, dict)
            or not isinstance(item.get("id"), str)
            or not re.fullmatch(r"\d{5,}", item["id"])
            for item in registros
        ):
            raise RuntimeError("Histórico contém registro de bem inválido. Revise o JSON.")
        return registros

    def carregar(self):
        """IDs persistentes, consultados antes de tentar reclassificar."""
        return {item["id"] for item in self._ler_registros()}

    def registrar(self, identificador):
        """Grava bloqueio de um ID estável, após aviso explícito do E-ESTADO."""
        identificador = str(identificador)
        if not re.fullmatch(r"\d{5,}", identificador):
            return False  # hashes de linhas variáveis permanecem apenas em memória
        registros = self._ler_registros()
        if any(item["id"] == identificador for item in registros):
            return False
        registros.append({
            "id": identificador,
            "registrado_em": datetime.now().astimezone().isoformat(timespec="seconds"),
            "motivo": "Bloqueado no E-ESTADO",
        })
        registros.sort(key=lambda item: int(item["id"]))
        dados = {"versao": 1, "bens_bloqueados": registros}
        arquivo_temp = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="\n",
                prefix=".bens_bloqueados_", suffix=".tmp",
                dir=str(self.caminho.parent), delete=False
            ) as arquivo:
                arquivo_temp = arquivo.name
                json.dump(dados, arquivo, indent=2, ensure_ascii=False)
                arquivo.write("\n")
                arquivo.flush()
                os.fsync(arquivo.fileno())
            os.replace(arquivo_temp, self.caminho)
        except OSError as erro:
            raise RuntimeError(
                f"Falha ao salvar histórico em {self.caminho}. "
                "Interrompendo para evitar perda silenciosa dos bloqueios."
            ) from erro
        finally:
            if arquivo_temp and os.path.exists(arquivo_temp):
                os.unlink(arquivo_temp)
        return True
