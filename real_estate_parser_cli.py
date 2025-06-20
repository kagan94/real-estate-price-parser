import argparse
from parsers.kvee_parser import KvEeParser
from parsers.city24_parser import City24Parser
from parsers.kinnisvara24_parser import Kinnisvara24Parser
from db import Database


def main():
    parser = argparse.ArgumentParser(description='Parse real estate listings from portals.')
    parser.add_argument('portal', choices=['kvee', 'city24', 'kinnisvara24'], help='Portal to parse')
    args = parser.parse_args()

    db = Database()

    if args.portal == 'kvee':
        listings = KvEeParser().parse()
        db.save_kvee_listings(listings)
    if args.portal == 'city24':
        listings = City24Parser().parse()
        db.save_city24_listings(listings)
    if args.portal == 'kinnisvara24':
        listings = Kinnisvara24Parser().parse()
        db.save_kinnisvara24_listings(listings)
    print(f"Parsed and saved {len(listings)} listings from {args.portal}")


if __name__ == '__main__':
    main()
