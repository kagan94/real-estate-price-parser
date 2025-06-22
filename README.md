# Parse apartment prices in Tallinn from kv.ee, city24.ee, kinnisvara24.ee

Application is parsing and storing real estate prices from main Estonian real estate portals:

- [kv.ee](https://www.kv.ee)
- [city24.ee](https://www.city24.ee)
- [kinnisvara24.ee](https://kinnisvara24.ee)

## Project goal

The goal is to validate and find apartments which are posted not all portals. For example, apartment has listing on city24.ee, but not on kv.ee.

The motivation behind this experiment is to check if there are some mispriced apartments which are posted only on 1 portal.   

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

## Testing

Run tests using one of the following commands:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/parsers/test_city24_parser.py -v

# Run tests using the test runner script
python run_tests.py
```


# Data validation (for Tallinn apartment prices only)

## 1. Query total number of listings
```
select 'kvee', count(1) as portal from kvee_listing
union all
select 'city24', count(1) as portal from city24_listing
union all
select 'kinnisvara24', count(1) as portal from kinnisvara24_listing;
```

**Result**:
```
kvee, 4766
city24, 4242
kinnisvara24, 3221
```

## 2. Query to validate if apartment ad is posted only on single portal

### 2.1. Find listings on "kinnisvara24.ee" which are not present on "kv.ee"
```
select *
from kinnisvara24_listing k24
where not exists(
    select 1
    from kvee_listing kvee
    where 1=1
      and k24.city = kvee.city
      and REPLACE(REPLACE(kvee.street_with_building, ' tn', ''), ' mnt', '') =
          REPLACE(REPLACE(k24.street_with_building, ' tn', ''), ' mnt', '')
);
```
<small>* NB: we don't join data by "apartment number" because on some portals it's present, on some it's not. We simplified the validation request to check only by city, street, and building number.</small>  
**Result**: 328.

### 2.2. Find listings on "city24.ee" which are not present on "kv.ee"
```
select count(1)
from city24_listing city24
where not exists(
    select 1
    from kvee_listing kv
    where 1=1
      and city24.city = kv.city
      and
        REPLACE(REPLACE(kv.street_with_building, ' tn', ''), ' mnt', '') =
        REPLACE(REPLACE(city24.street_with_building, ' tn', ''), ' mnt', '')
--       and (
--         (city24.apartment_number is null and kv.apartment_number is null)
--             or (city24.apartment_number is not null and city24.apartment_number = kv.apartment_number)
--         )
);
```
**Result**: 434.
