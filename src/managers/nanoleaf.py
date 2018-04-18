import numpy as np
import requests
import json
import socket
from .manager_base import ManagerBase, Panel


class PanelLayout:
    def __init__(self, json):
        self.panels = sorted([Panel(p['panelId'], p['x'], p['y'], np.deg2rad(p['o'])) for p in json],
                             key=lambda v: v.center_x)
        self.panel_ids = [p.id for p in self.panels]

    @staticmethod
    def make_panel_info(panel_id, color):
        red, green, blue = color
        return bytes([panel_id, 1, red, green, blue, 0, 1])

    def make_frame(self, colors_list):
        return (bytes([len(self.panel_ids)]) +
                b''.join([PanelLayout.make_panel_info(i, c) for (i, c) in zip(self.panel_ids, colors_list)]))


class NanoleafManager(ManagerBase):
    def __init__(self, ip, port, token):
        self.ip = ip
        self.port = port
        self.token = token

        r = requests.get(f"http://{ip}:{port}/api/v1/{token}")
        if not r.ok:
            raise RuntimeError(f"Could not connect to Aurora: {r}")
        resp = json.loads(r.content.decode())
        self.layout = PanelLayout(resp['panelLayout']['layout']['positionData'])

        r = requests.put(f"http://{ip}:{port}/api/v1/{token}/effects",
                         json={"write": {"command": "display", "animType": "extControl"}})
        if not r.ok:
            raise RuntimeError(f"Error switching to manual mode: {r}")
        resp = r.json()
        udp_ip = resp['streamControlIpAddr']
        udp_port = resp['streamControlPort']
        self.addr = (udp_ip, udp_port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_num_panels(self):
        return len(self.layout.panels)

    def get_layout(self):
        return self.layout.panels

    def put_colors(self, colors):
        assert len(colors) == self.get_num_panels()

        # print(f"Putting {colors[-1]}")

        colors = np.array(colors)
        frame = self.layout.make_frame(np.rint(colors * 255).astype(int))
        self.sock.sendto(frame, self.addr)
