"""
Object that continuously polls ethos for stats, and detects anomolies
"""

from collections import defaultdict
from .network import Network


class Monitor:
    def __init__(self, chat_id, bot):
        self.chat_id = chat_id
        self.bot = bot
        self.panels = []
        self.rigs = []

    @property
    def network(self):
        return self.bot.network

    def categorized_rigs(self, old_rigs, new_rigs) -> dict:
        lookup = defaultdict(lambda: [])
        for rig in old_rigs + new_rigs:
            lookup[rig.uid].append(rig)

        return {
            "removed": [r for r in old_rigs if len(lookup[r.uid]) == 1],
            "added": [r for r in new_rigs if len(lookup[r.uid]) == 1],
            "updated": [p for p in lookup.values() if len(p) == 2],
        }

    def fetch_rigs(self):
        rigs = [self.network.fetch_rigs(pid) for pid in self.panels]
        return [rig for subrigs in rigs for rig in subrigs]

    def send_stats(self, included):
        print("stats requested: " + repr(included))
        table = [r.row(included) for r in self.fetch_rigs()]
        self.bot.send_table(table, self.chat_id)

    # scheduler

    def update(self):
        old_rigs = self.rigs
        new_rigs = self.fetch_rigs()
        grouped_rigs = self.categorized_rigs(old_rigs, new_rigs)

        all_rows = []
        alerts = []

        for rig in grouped_rigs["removed"]:
            alerts.append(rig.name + " has been removed")

        for rig in grouped_rigs["added"]:
            alerts.append(rig.name + " has been added!")

        for old_rig, new_rig in grouped_rigs["updated"]:
            row = []
            old_mets = old_rig.all_metrics()
            new_mets = new_rig.all_metrics()
            for old_met, new_met in zip(old_mets, new_mets):
                alert = new_met.alert(old_met)
                if alert:
                    alerts.append(new_rig.name + ": " + alert)
                    row.append(str(new_met))
            if row:
                row = [new_rig.name] + row
                all_rows.append(row)

        if all_rows:
            self.bot.send_table(all_rows, self.chat_id)
        if alerts:
            self.bot.send_message("\n".join(alerts), self.chat_id)

        self.rigs = new_rigs
