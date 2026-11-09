# -*- coding: utf-8 -*-
"""Persistência independente do ranking: descobertas, conquistas e dados da oficina."""
import json
import os


class ProgressStore:
    FILE_NAME = "eco_progress.json"
    VERSION = 1

    def __init__(self, path=None):
        self.path = path or self.default_path()
        self.discovered_ids = set()
        self.achievement_levels = set()
        self.workshop_completions = 0
        self.workshop_best_score = 0
        self.workshop_perfect_runs = 0
        self.load_error = None          # texto do problema, se o arquivo estava ilegivel
        self.load()

    @classmethod
    def default_path(cls):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not os.access(base, os.W_OK):
            base = os.path.expanduser("~")
        return os.path.join(base, cls.FILE_NAME)

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as stream:
                data = json.load(stream)
            if not isinstance(data, dict):
                raise ValueError("Formato de progresso inválido")
            self.discovered_ids = {str(x) for x in data.get("discovered_ids", []) if isinstance(x, str)}
            self.achievement_levels = {
                int(x) for x in data.get("achievement_levels", [])
                if str(x).isdigit()
            }
            self.workshop_completions = max(0, int(data.get("workshop_completions", 0)))
            self.workshop_best_score = max(0, int(data.get("workshop_best_score", 0)))
            self.workshop_perfect_runs = max(0, int(data.get("workshop_perfect_runs", 0)))
        except FileNotFoundError:
            self._save()
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            # Mantém o jogo jogável quando o arquivo está corrompido, mas guarda uma cópia para
            # que as descobertas antigas não sejam perdidas no próximo salvamento.
            self.discovered_ids = set()
            self.achievement_levels = set()
            self.workshop_completions = 0
            self.workshop_best_score = 0
            self.workshop_perfect_runs = 0
            self.load_error = "arquivo de progresso ilegível"
            self._backup_corrupt()

    def _backup_corrupt(self):
        try:
            os.replace(self.path, self.path + ".corrompido")
        except OSError:
            pass

    def _save(self):
        folder = os.path.dirname(self.path)
        try:
            if folder:
                os.makedirs(folder, exist_ok=True)
            payload = {
                "version": self.VERSION,
                "discovered_ids": sorted(self.discovered_ids),
                "achievement_levels": sorted(self.achievement_levels),
                "workshop_completions": self.workshop_completions,
                "workshop_best_score": self.workshop_best_score,
                "workshop_perfect_runs": self.workshop_perfect_runs,
            }
            tmp = self.path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as stream:
                json.dump(payload, stream, ensure_ascii=False, indent=2)
            os.replace(tmp, self.path)
            return True
        except OSError:
            return False

    def discover(self, item_id):
        """Registra uma descoberta e retorna True somente na primeira vez."""
        if not item_id or item_id in self.discovered_ids:
            return False
        self.discovered_ids.add(str(item_id))
        self._save()
        return True

    def unlock_achievement(self, level):
        level = int(level)
        if level in self.achievement_levels:
            return False
        self.achievement_levels.add(level)
        self._save()
        return True

    def register_workshop_completion(self, score=0, perfect=False):
        self.workshop_completions += 1
        self.workshop_best_score = max(self.workshop_best_score, int(score))
        if perfect:
            self.workshop_perfect_runs += 1
        self._save()
