import logging
from typing import Optional

from GuardiPy import CentraApiPayload, Centra
from GuardiPy.CentraObject import Agent, LabelMinimal

from secrets import dev_host, host


def fetch_customer_label(gc: Centra, gc_customer_name: str) -> Optional[str]:
    query: CentraApiPayload = LabelMinimal.list(
        assets='on,off',
        find_matches=True,
        dynamic_criteria_limit=500,
        key='Customers', value=gc_customer_name
    )
    res = gc.execute(query)
    return [str(res[0])] if res else None


def fetch_agents(gc: Centra, cus_name: str = None) -> int:
    cus_label = fetch_customer_label(gc=gc, gc_customer_name=cus_name)
    print(cus_label)
    query = Agent.list(sort_by_property='display_name', labels=cus_label)
    result = gc.export_to_csv(query)
    line_count = len(result.splitlines()) - 1
    return line_count if line_count > 0 else 0


def main():
    gc = Centra(hostname=dev_host['dev_host'], username=dev_host['username'], password=dev_host['password'])
    agent_count = fetch_agents(gc=gc, cus_name=dev_host['name'])
    print(f"{agent_count} agents found for unshared instance")

    gc = Centra(hostname=host['dev_host'], username=host['username'], password=host['password'])
    agent_count = fetch_agents(gc=gc, cus_name=host['name'])
    print(f"{agent_count} agents found for {host['name']} on shared instance")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    main()
