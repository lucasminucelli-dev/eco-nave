# -*- coding: utf-8 -*-
"""Ranking dos melhores jogadores, salvo em arquivo TXT (campos separados por tabulacao)."""
import csv
import os
from datetime import datetime

from .config import NAME_MAX, RANKING_SIZE


class RankEntry:
    """Uma linha do ranking."""
    __slots__ = ("name", "score", "level", "date")

    def __init__(self, name, score, level, date):
        self.name = name
        self.score = score
        self.level = level
        self.date = date

    @classmethod
    def create(cls, name, score, level):
        """Nova entrada com a data de hoje; nome vazio vira 'Jogador'."""
        return cls(name.strip() or "Jogador", score, level, datetime.now().strftime("%d/%m/%Y"))


class RankingStore:
    """Carrega, guarda e atualiza o top do ranking."""
    FILE_NAME = "ranking.txt"

    def __init__(self, path=None, size=RANKING_SIZE):
        self.path = path or self.default_path()
        self.size = size
        self.entries = []
        self.load()

    @classmethod
    def default_path(cls):
        """Pasta do projeto (a que tem o main.py); se nao der para gravar, a pasta do usuario."""
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not os.access(base, os.W_OK):
            base = os.path.expanduser("~")
        return os.path.join(base, cls.FILE_NAME)

    def load(self):
        out = []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for row in csv.reader(f, delimiter="\t"):
                    if len(row) != 4:
                        continue
                    name, score, level, date = row
                    out.append(RankEntry(name[:NAME_MAX], int(score), int(level), date))
            out.sort(key=lambda e: -e.score)
            self.entries = out[:self.size]
        except Exception:
            self.entries = []

    def save(self):
        try:
            tmp = self.path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter="\t", lineterminator="\n")
                for e in self.entries:
                    writer.writerow((e.name, e.score, e.level, e.date))
            os.replace(tmp, self.path)
            return True
        except Exception:
            return False

    def add(self, entry):
        """Insere a entrada, mantem so o top e grava. Devolve True se ela entrou no top."""
        self.entries.append(entry)
        self.entries.sort(key=lambda e: -e.score)
        self.entries = self.entries[:self.size]
        kept = any(e is entry for e in self.entries)
        self.save()
        return kept
