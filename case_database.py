import re

from database import Database
from database_schema import TestCase


class CaseDatabase(Database):
    def __init__(self, database_name):
        super(CaseDatabase, self).__init__(database_name)

    def get_domains(self):
        domains = []
        cases = self.session.query(TestCase).filter(TestCase.host_status_on_zabbix == 'Enabled')
        for case in cases:
            domain = self.extract_domain(case.test_steps)
            if domain:
                entry = {'app': case.application, 'domain': domain}
                domains.append(entry)
        domains = self.filter_port(domains)
        domains = self.remove_duplicate(domains)
        return domains

    def extract_domain(self, text):
        pattern_url = r'(?:https?://)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(?::\d{2,5})?(?:/[^\s]*)?$'
        pattern_domain = r'(?:https?://)?([^/]+)'
        match_url = re.search(pattern_url, text)
        if match_url:
            match_domain = re.search(pattern_domain, match_url.group(0))
            if match_domain:
                return match_domain.group(1)
        else:
            return None

    def filter_port(self, data):
        filtered_data = []
        for entry in data:
            domain = entry['domain']
            if ':' in domain:
                domain_part, port = domain.split(':')
                if port in ['80', '443']:
                    entry['domain'] = domain_part
                    filtered_data.append(entry)
            else:
                filtered_data.append(entry)
        return filtered_data

    def remove_duplicate(self, data):
        checked_domains = set()
        unique_data = []
        for entry in data:
            domain = entry['domain']
            if domain not in checked_domains:
                unique_data.append(entry)
                checked_domains.add(domain)
        return unique_data
