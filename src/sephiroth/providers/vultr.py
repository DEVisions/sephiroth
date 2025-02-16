from typing import TypedDict

import requests

from sephiroth.providers.base_provider import BaseProvider


class VultrIPRange(TypedDict):
    ip_prefix: str
    alpha2code: str
    region: str
    city: str
    postal_code: str


class VultrRanges(TypedDict):
    description: str
    asn: int
    email: str
    updated: str
    subnets: list[VultrIPRange]


class Vultr(BaseProvider):
    def __init__(self, excludeip6=False):
        self.source_ranges = self._get_ranges()
        self.processed_ranges = self._process_ranges()

    def _get_ranges(self) -> VultrRanges:
        """
        Input: None
        Output: List of ip addresses
        """
        print(
            "(vultr) Fetching Vulr address ranges from https://geofeed.constant.com/?json"
        )
        url = "https://geofeed.constant.com/?json"
        r = requests.get(url)
        return VultrRanges(r.json())

    def _process_ranges(self):
        """
        Input: Dict of ip-ranges.json, optionally exclude ip6 ranges
        Output: Dict with header_comments and list of dicts for ip ranges
        """
        header_comments = [
            "(vultr) Addresses collected from https://geofeed.constant.com/?json",
            f"(vultr) Description: {self.source_ranges['description']}",
            f"(vultr) ASN: {self.source_ranges['asn']}",
            f"(vultr) Email: {self.source_ranges['email']}",
            f"(vultr) Updated: {self.source_ranges['updated']}",
        ]
        out_ranges = []
        for address in self.source_ranges["subnets"]:
            if not address:
                continue
            item = {
                "range": address["ip_prefix"],
                "comment": f"{address['alpha2code']},{address['region']}, {address['city']},{address['postal_code']}",
            }
            out_ranges.append(item)
        return {"header_comments": header_comments, "ranges": out_ranges}
