import csv
import logging
from datetime import timedelta
from typing import TypeVar, List, Dict, Optional

import inflect
from GuardiPy import Centra, CentraEntity, CentraApiPayload
from GuardiPy.CentraObject import Incident, LabelMinimal

from BlacklistReport.BlacklistEntry import BlacklistEntry
from BlacklistReport.__threat_data import ThreatData
from BlacklistReport.schema import GC_CSV_SCHEMA, CENTRA_SCHEMA, is_valid_format

AnyCentraEntity = TypeVar("AnyCentraEntity", bound=CentraEntity)


def generate_blacklist_report(gc_host: Dict, hours: int, opswat_key: str, gc_customer_name: str, severity: List[str] = None):
    if is_valid_format(gc_host, CENTRA_SCHEMA):

        gc = Centra(username=gc_host['username'],
                    hostname=gc_host['dev_host'],
                    password=gc_host['password'])

        converter = inflect.engine()

        ThreatData.set_opswat_key(opswat_key=opswat_key)

        blr = BlacklistReport(gc=gc, gc_customer_name=gc_customer_name)
        incident_count = blr.fetch_incidents(hours, severity=severity)
        incident_count_str = converter.number_to_words(incident_count)
        blr.build_report()

        source_ip_count = len(blr.report.keys())
        source_ip_count_str = converter.number_to_words(source_ip_count)

        output = {
            "hours": hours,
            "incident_count": incident_count,
            "incident_count_str": incident_count_str,
            "report": blr.build_report_str(incident_count_str, incident_count, source_ip_count_str, source_ip_count)
        }
        return output
    else:
        logging.error("Failed to instantiate Centra instance.", exc_info=True)


class BlacklistReport:
    def __init__(self, gc: Centra, gc_customer_name: str):
        self.gc: Centra = gc
        self.incidents: List[Dict] = []
        self.report: Dict = {}
        self.hours: int = -1
        self.customer_label = self.fetch_customer_label(gc_customer_name)

    def fetch_customer_label(self, gc_customer_name: str) -> Optional[str]:
        query: CentraApiPayload = LabelMinimal.list(
            assets='on,off',
            find_matches=True,
            dynamic_criteria_limit=500,
            key='Customers', value=gc_customer_name
        )
        res = self.gc.execute(query)
        return str(res[0]) if res else None

    def fetch_incidents(self, hours: int = 24, severity: List[str] = ["Medium, High"]) -> int:
        self.hours = abs(hours)
        query = Incident.list(
            from_time=timedelta(hours=-self.hours),
            incident_type='Reveal',
            tags_include='Reputation',
            severity=severity,
            prefixed_filter='bad_reputation'
        )
        if self.customer_label:
            query.params['any_side'] = self.customer_label
        result = self.gc.export_to_csv(query).splitlines()

        csv_reader = csv.DictReader(result, delimiter=',')
        self.incidents = [_parse_reported_fields(row) for row in csv_reader]
        logging.debug("Number of blacklisted IP incidents fetched: %d", len(self.incidents))
        return len(self.incidents)

    def build_report(self):
        for incident in self.incidents:
            src = incident['src']
            dst = incident['dst']
            ports = self._fetch_destination_ports_for_incident(incident['id'])
            if src in self.report:
                self.report[src].add_destination(dst=dst, ports=ports)
            else:
                self.report[src] = BlacklistEntry(src=src, dst=dst, ports=ports)
        return self.report.copy()

    def _fetch_destination_ports_for_incident(self, target_id) -> List[int]:
        incident: Incident = self.gc.execute(Incident.get_all_info(id=target_id))
        ports = list(set([e.destination_port for e in incident.events
                          if e.destination_port is not None and e.destination_port >= 0]))
        return ports

    def build_report_str(self, incident_count_str: str, incident_count: int, source_ip_count_str: str, source_ip_count: int):
        report_summary = self._plaintext_header(incident_count_str, incident_count, source_ip_count_str, source_ip_count)
        report_summary += ''.join([_plaintext_entry(ip, entry) for ip, entry in self.report.items()])
        return report_summary

    def _plaintext_header(self, incident_count_str, incident_count, source_ip_count_str, source_ip_count) -> str:
        return f"In the past {self.hours} hours, we have seen {incident_count_str} ({incident_count}) " \
               f"reputation incidents from {source_ip_count_str} ({source_ip_count}) sources.\n\n"


def _parse_reported_fields(entity: Dict) -> Dict:
    parsed_entity = {}
    if is_valid_format(entity, GC_CSV_SCHEMA):
        affected_assets = [asset.strip() for asset in entity.get('affected_assets', '').split('),')]
        src = affected_assets[0].split(' ')[0]
        dst = affected_assets[1].split(' ')[0]
        if "\\" in dst:
            dst = dst.split("\\")[1]
        parsed_entity = {
            'id': entity['id'],
            'src': src,
            'dst': dst
        }
    return parsed_entity


def _plaintext_entry(ip, ip_entry: BlacklistEntry) -> str:
    text = ""
    text += f"Source: {ip} ({ip_entry.src.origin_country})\n"
    if ip_entry.src.origin_country != 'Internal':
        text += f"\tOPSWAT: {ip_entry.src.opswat}\n"
        text += f"\tTalos: {ip_entry.src.talos}\n"
    text += f"Destination(s):\n"
    for destination in ip_entry.destinations:
        text += f"\tDestination: {destination.ip} ({destination.origin_country})\n"
        text += f"\tDestination Port(s): {destination.ports}"
        if destination.origin_country != 'Internal':
            text += f"\n\tOPSWAT: {destination.opswat}"
            text += f"\n\tTalos: {destination.talos}\n"
        else:
            text += "\n"
        text += "\n"
    text += "\n"
    return text
