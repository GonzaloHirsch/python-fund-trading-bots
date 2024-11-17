import json
from datetime import datetime
from logger.setup import logging
from time import sleep
from scraper.vanguard import get_portfolios_list, get_portfolios_data


def main():
    # Get a list of all the funds we have.
    funds = get_portfolios_list()

    # Store the data locally.
    with open("data/portfolios.json", "w") as f:
        f.write(json.dumps([fund.raw for fund in funds]))

    # Get just a list of the fund IDs for the other API.
    min_date = min([fund.creation_date for fund in funds])
    logging.info(f"Minimum date found: {min_date}")

    # Process all the funds.
    for fund in funds:
        logging.info(f"Processing Fund: {fund.name} ({fund.id})")

        # Get the actual fund data.
        pricing = get_portfolios_data(
            portfolios=[fund.id],
            start_date=datetime.strptime(fund.creation_date, "%Y-%m-%d").date(),
            end_date=datetime.today(),
        )

        # Write locally.
        pricing[0].price.to_csv(f"data/pricing/{fund.id}.csv", index=False)

        # Sleep to protect the API.
        sleep(5)


if __name__ == "__main__":
    main()
