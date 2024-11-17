import requests
import logging
from typing import List, Dict, NamedTuple, cast
from datetime import datetime
from pandas import DataFrame

# Some Vanguard-specific variables.
VANGUARD_PORTFOLIOS_URL = "https://www.vanguardinvestor.co.uk/api/productList"
VANGUARD_PRICING_URL = "https://www.vanguardinvestor.co.uk/gpx/graphql"
with open("data/requests/pricing.gql", "r") as f:
    VANGUARD_PRICE_GRAPHQL_QUERY = f.read()

# Responses.
FundPricing = NamedTuple("FundPricing", (("id", str), ("price", DataFrame)))
Fund = NamedTuple(
    "Fund",
    (
        ("id", str),
        ("name", str),
        ("allocation", str),
        ("creation_date", str),
        ("raw", Dict),
    ),
)


def __get_vanguard_body(
    portfolios: List[str], start_date: datetime, end_date: datetime
) -> Dict:
    return {
        "query": VANGUARD_PRICE_GRAPHQL_QUERY,
        "operationName": "PriceDetailsQuery",
        "variables": {
            "portIds": portfolios,
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "limit": 0,
        },
    }


def handle_response(response: requests.Response):
    if response.status_code >= 300:
        raise ValueError(
            f"No data from API. Response: {response.text}. Headers: {response.headers}"
        )


def get_portfolios_data(
    portfolios: List[str], start_date: datetime, end_date: datetime
) -> List[FundPricing]:
    # Prepare the body for the request.
    body = __get_vanguard_body(
        portfolios=portfolios, start_date=start_date, end_date=end_date
    )
    logging.info(f"Request for Vanguard Portfolios API: {body}")

    # Get the data from the API
    response = requests.post(
        VANGUARD_PRICING_URL,
        json=body,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    # Verify response status.
    handle_response(response)

    # Parse response.
    fund_data = cast(Dict, response.json()).get("data", {}).get("funds", [])

    # Convert to the correct structures.
    return [
        FundPricing(
            id=fund,
            price=DataFrame(
                fund_data[index]["pricingDetails"]["navPrices"]["items"],
                columns=["price", "asOfDate", "currencyCode", "__typename"],
            ),
        )
        for index, fund in enumerate(portfolios)
    ]


def get_portfolios_list() -> List[Fund]:
    # Get data from the API.
    response = requests.get(
        VANGUARD_PORTFOLIOS_URL,
        headers={"Accept": "application/json"},
    )

    # Handle the response.
    handle_response(response)

    return [
        Fund(
            id=fund["portId"],
            name=fund["name"],
            allocation=fund["allocation"],
            creation_date=fund["inceptionDate"],
            raw=fund,
        )
        for fund in response.json()
    ]
