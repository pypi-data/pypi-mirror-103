import requests
import json
import logging

PROMETHEUS_URL = "http://alert-store.bigo.sg:8881/insert/42/prometheus"


def report_metric_to_prometheus(data, url=PROMETHEUS_URL):
    headers = {"content-type": "application/json"}
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    logging.info("[Report to Promxy] resp: %s", resp)
    logging.info("[Report] req.text: %s", json.dumps(data))
    logging.info("[Report] resp.text: %s", resp.text)
    resp.raise_for_status()
