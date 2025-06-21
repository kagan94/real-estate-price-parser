# Parse apartment prices in Tallinn from kv.ee, city24.ee, kinnisvara24.ee

Application is parsing and storing real estate prices from main Estonian real estate portals:

- [kv.ee](https://www.kv.ee)
- [city24.ee](https://www.city24.ee)
- [kinnisvara24.ee](https://kinnisvara24.ee)

## Features

- Stores the results for each portal in separate tables in DB.

## Usage

```
python real_estate_parser_cli.py --portal [PORTAL_TYPE]
```

Example:

```
python real_estate_parser_cli.py --portal kvee
python real_estate_parser_cli.py --portal city24
python real_estate_parser_cli.py --portal kinnisvara24
```
