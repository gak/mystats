import json
import requests


def main(stats):
    if not stats.run_every_n_minutes(5):
        return

    url = 'http://www.bom.gov.au/fwo/IDN60901/IDN60901.95765.json'
    data = requests.get(url).content
    data = json.loads(data)
    current = data['observations']['data'][0]

    stats.gauge('outside.temperature', current['air_temp'])
    stats.gauge('outside.apparent_temperature', current['apparent_t'])
    stats.gauge('outside.wind_speed_kmh', current['wind_spd_kmh'])
    stats.gauge('outside.relative_humidity', current['rel_hum'])

