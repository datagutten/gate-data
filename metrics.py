import prometheus_client

registry = prometheus_client.CollectorRegistry()
labels = {'direction': 'Direction', 'gate_id': 'Gate ID', 'detector': 'Radar detector'}
people = prometheus_client.Gauge('people_counter', 'People counter', labels, registry=registry)
