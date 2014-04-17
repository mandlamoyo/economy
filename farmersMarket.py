from constants import BUY, SELL, SEEDS, PRODUCE

class FarmersMarket:
    prices = [[6,3],[4,2]]
    
    @staticmethod
    def buySeeds( amount ):
        return FarmersMarket.prices[BUY][SEEDS] * amount
        
    @staticmethod
    def sellSeeds( amount ):
        return FarmersMarket.prices[SELL][SEEDS] * amount
        
    @staticmethod
    def buyProduce( amount ):
        return FarmersMarket.prices[BUY][PRODUCE] * amount
        
    @staticmethod
    def sellProduce( amount ):
        return FarmersMarket.prices[SELL][PRODUCE] * amount
    
    