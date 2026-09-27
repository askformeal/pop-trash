from tkinter import messagebox
import json
import os

from src.constants import STATS_CORRUPTED_PATH, STATS_PATH, DEFAULT_STATS, ENCODING

class Stats:
    def __init__(self, root):
        self.root = root

    def get_stats(self):
        try:
            with open(STATS_PATH, 'r', encoding=ENCODING) as f:
                stats = json.load(f)
        
        except FileNotFoundError:
            stats = dict(DEFAULT_STATS)

        except OSError as e:
            stats = dict(DEFAULT_STATS)
            msg = str(e)
            self.root.after(0, lambda: messagebox.showerror('Error', f'Failed to open stats file: {msg}'))

        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            stats = dict(DEFAULT_STATS)
            os.replace(STATS_PATH, STATS_CORRUPTED_PATH)
            msg = str(e)
            self.root.after(0, lambda: messagebox.showerror('Error', f'Failed to decode stats file: {msg}'))
        else:
            if isinstance(stats, dict):
                for key, value in DEFAULT_STATS.items():
                    if key not in stats.keys():
                        stats[key] = value
            else:
                stats = dict(DEFAULT_STATS)

        return stats

    def record_size(self, size):
        stats = self.get_stats()
        stats['total_size'] += size
        self._set_stats(stats)

    def _set_stats(self, stats):
        tmp_path = STATS_PATH.with_suffix('.tmp')
        try:
            with open(tmp_path, 'w', encoding=ENCODING) as f:
                json.dump(stats, f)
        except OSError as e:
            msg = str(e)
            self.root.after(0, lambda: messagebox.showerror('Error', f'Failed to write into {tmp_path}: {msg}'))
        else:
            os.replace(tmp_path, STATS_PATH)
