from constants import BUY, SELL, TRACTORS

class TractorMarket:
    prices = [[130],[100]]

    @staticmethod
    def buyTractors( amount ):
        return TractorMarket.prices[BUY][TRACTORS] * amount
    
    @staticmethod
    def sellTractors( amount ):
        return TractorMarket.prices[SELL][TRACTORS] * amount