DB_PATH = "sqlite:///real_estate_prices.db"

# kv.ee
KVEE_BASE_URL = "https://www.kv.ee"
KVEE_SEARCH_URL = "https://www.kv.ee/ru/search?orderby=cawl&deal_type=1&county=1&parish=1061&start="

# city24.ee
CITY24_BASE_URL = "https://www.city24.ee/ru"
CITY24_API_SEARCH_URL = "https://api.city24.ee/ru_RU/search/realties?address%5Bcc%5D=1&address%5Bparish%5D%5B%5D=181&tsType=sale&unitType=Apartment&order%5BdatePublished%5D=desc&adReach=0&itemsPerPage={limit}&page={page}"

# kinnisvara24.ee
KINNISVARA24_BASE_URL = "https://kinnisvara24.ee/ru"
KINNISVARA24_API_SEARCH_URL = "https://kinnisvara24.ee/search"
KINNISVARA24_API_PAYLOAD = {
    "deal_types": ["sale"],
    "object_types": ["apartment"],
    "addresses": [{"A1": "Harju maakond", "A2": "Tallinn"}],
    "sort_by": "created_at",
    "sort_order": "desc"
}
