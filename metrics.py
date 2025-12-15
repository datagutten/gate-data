import prometheus_client


class GateMetrics:
    def __init__(self):
        self.registry = prometheus_client.CollectorRegistry()
        self.labels = {'direction': 'Direction', 'gate_id': 'Gate ID', 'detector': 'Radar detector'}
        self.people = prometheus_client.Gauge('people_counter', 'People counter', self.labels, registry=self.registry)
