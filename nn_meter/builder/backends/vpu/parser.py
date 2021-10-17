from nn_meter.builder.utils.latency import Latency
import re


class VPUParser:
    def __init__(self):
        pass

    def parse(self, output):
        self.layers = self._parse_layers(output)
        self.comp_layer_latency = sum(
            Latency(layer['realtime'])
            for layer in self.layers
            if layer['layer_name'] != '<Extra>'
        )
        return self

    def _parse_layers(self, output):
        layer_regex = r'^([^;]+);([^;]+);([^;]+);([^;]+);([^;]+);([^;]+);$'
        layers = []
        for match in re.findall(layer_regex, output, re.MULTILINE):
            try:
                layers.append({
                    'layer_name': match[0],
                    'exec_status': match[1],
                    'layer_type': match[2],
                    'exec_type': match[3],
                    'realtime': float(match[4]),
                    'cputime': float(match[5]),
                })
            except:
                pass
        return layers

    @property
    def latency(self):
        return self.comp_layer_latency
