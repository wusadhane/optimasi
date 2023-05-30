import yfinance as yf
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta

# saham = ["NFCX", "MLPT"]
start = datetime.now()
end = start - relativedelta(years=1)
print(start)
print(end)



def kalkulasi(saham, biaya):
    saham = [stock + ".JK" for stock in saham]
    get_saham = yf.download(saham, start=end, end=start)
    harga = get_saham["Close"].dropna(how="all")
    mu = mean_historical_return(harga)
    cov = CovarianceShrinkage(harga).ledoit_wolf()

    ef = EfficientFrontier(mu, cov)
    weights = ef.min_volatility()

    harga_terbaru = get_latest_prices(harga)
    da = DiscreteAllocation(weights, harga_terbaru, total_portfolio_value=biaya)
    allocation, sisaUang = da.greedy_portfolio()
    lot = {key: math.floor(allocation[key] / 100) for key in allocation.keys()}
    anggaran = {
        key: format(math.floor(allocation[key] / 100) * 100 * harga_terbaru[key])
        for key in allocation.keys()
    }
    persensaham = {
        stock: round(ef.clean_weights()[stock] * 100) for stock in ef.clean_weights()
    }
    expectedReturn, volatility, sharpeRatio = ef.portfolio_performance(verbose=True)

    return (
        anggaran,
        lot,
        format(sisaUang),
        persensaham,
        expectedReturn,
        volatility,
        sharpeRatio,
        harga_terbaru,
    )
kalkulasi (100000000)
