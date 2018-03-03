"""
Network interactor - should be mocked in tests
"""

import json
from urllib.request import urlopen
from .models import Rig


class Network:
    def fetch_rigs(self, panel_id) -> [Rig]:
        panel_url = "http://%s.ethosdistro.com/?json=yes" % (panel_id)
        ethos_response_raw = urlopen(panel_url)
        ethos_response = json.loads(ethos_response_raw.read().decode())
        rigs = ethos_response["rigs"].items()
        return sorted([Rig(u, p) for u, p in rigs], key=lambda r: r.uid)
