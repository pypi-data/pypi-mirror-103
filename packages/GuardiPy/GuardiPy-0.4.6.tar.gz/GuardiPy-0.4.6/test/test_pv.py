import logging
from datetime import timedelta
from typing import Optional

from GuardiPy import CentraApiPayload, Centra
from GuardiPy.CentraObject import Incident, LabelMinimal

from secrets import host, dev_host


def fetch_customer_label(gc: Centra, gc_customer_name: str) -> Optional[str]:
    query: CentraApiPayload = LabelMinimal.list(
        assets='on,off',
        find_matches=True,
        dynamic_criteria_limit=500,
        key='Customers', value=gc_customer_name
    )
    res = gc.execute(query)
    return str(res[0]) if res else None


def fetch_incidents(gc: Centra, hours: int = 24, customer_label: str = None) -> int:
    hours = abs(hours)
    query = Incident.list(
        from_time=timedelta(hours=-hours),
        incident_type='Reveal',
        tags_include='Policy Violation',
        severity=["Low", "Medium", "High"],
        prefixed_filter='policy_violations'
    )
    if customer_label:
        query.params['any_side'] = customer_label
    result = gc.export_to_csv(query)
    line_count = len(result.splitlines()) - 1
    return line_count if line_count > 0 else 0


def main():
    gc = Centra(hostname=dev_host['dev_host'], username=dev_host['username'], password=dev_host['password'])
    customer_label = fetch_customer_label(gc=gc, gc_customer_name=dev_host['name'])
    pv_incidents = fetch_incidents(gc=gc, hours=48, customer_label=customer_label)
    logging.info("Number of PV incidents fetched for dev instance: %d", pv_incidents)

    gc = Centra(hostname=host['dev_host'], username=host['username'], password=host['password'])
    customer_label = fetch_customer_label(gc=gc, gc_customer_name=host['name'])
    pv_incidents = fetch_incidents(gc=gc, hours=48, customer_label=customer_label)
    logging.info("Number of PV incidents fetched for %s in shared instance: %d", host['name'], pv_incidents)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    main()
