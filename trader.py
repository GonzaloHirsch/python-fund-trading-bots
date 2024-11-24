from logger.setup import logging
from parser.loader import get_all_portfolios, get_all_portfolio_pricing
from strategies.moving_average_crossover import moving_average_crossover_strategy
from strategies.bollinger_bands import bollinger_bands_strategy
import matplotlib.pyplot as plt


def main():
    # Read all the porfolios and their pricing.
    portfolios = get_all_portfolios()
    pricing = get_all_portfolio_pricing([port["portId"] for port in portfolios])

    # Run the strategy against all.
    for price in pricing:
        price = moving_average_crossover_strategy(
            data=price, short_window=50, long_window=200, price_col="price"
        )
        price = bollinger_bands_strategy(
            data=price, window=20, num_std=2, price_col="price"
        )
        price[["signal", "price"]].plot()
        plt.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    main()
