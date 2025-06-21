import argparse

import urllib3

from database import Database
from parsers.city24_parser import City24Parser
from parsers.kinnisvara24_parser import Kinnisvara24Parser
from parsers.kvee_parser import KvEeParser


def main():
    parser = argparse.ArgumentParser(description='Parse real estate listings from portals.')
    parser.add_argument('--portal', choices=['kvee', 'city24', 'kinnisvara24'], required=True, help='Portal to parse')
    args = parser.parse_args()

    db = Database()
    portal = args.portal

    if portal == 'kvee':
        listings = KvEeParser().parse()
        db.save_kvee_listings(listings)
    if portal == 'city24':
        listings = City24Parser().parse()
        db.save_city24_listings(listings)
    if portal == 'kinnisvara24':
        listings = Kinnisvara24Parser().parse()
        db.save_kinnisvara24_listings(listings)
    print(f"Processed {len(listings)} listings from {portal}")


if __name__ == '__main__':
    # disable warnings for "not able to verify SSL self-signed certificate"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    main()
