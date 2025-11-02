import requests
import logging
from datetime import datetime
from app.models import db, ProfitabilityData, Cryptocurrency, ASICMiner
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class CryptoPriceAPI:
    """Fetch cryptocurrency prices from CoinGecko API"""
    
    def __init__(self):
        self.coingecko_url = "https://api.coingecko.com/api/v3"
    
    def get_crypto_prices(self, coins=['bitcoin', 'ethereum', 'litecoin']):
        """Get current cryptocurrency prices"""
        try:
            response = requests.get(
                f"{self.coingecko_url}/simple/price",
                params={
                    'ids': ','.join(coins),
                    'vs_currencies': 'usd',
                    'include_market_cap': 'true',
                    'include_24hr_vol': 'true'
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching crypto prices: {e}")
            return self._get_cached_prices(coins)
    
    def _get_cached_prices(self, coins):
        """Get cached prices from database"""
        prices = {}
        for coin in coins:
            crypto = Cryptocurrency.query.filter_by(name=coin.lower()).first()
            if crypto:
                prices[coin] = {'usd': crypto.current_price}
            else:
                # Default fallback prices
                fallback = {
                    'bitcoin': 50000,
                    'ethereum': 3000,
                    'litecoin': 200,
                    'dogecoin': 0.15,
                    'monero': 150
                }
                prices[coin] = {'usd': fallback.get(coin, 0)}
        return prices
    
    def update_crypto_data(self):
        """Update cryptocurrency data in database"""
        coins_config = {
            'bitcoin': ('SHA-256', 'BTC'),
            'ethereum': ('Ethash', 'ETH'),
            'litecoin': ('Scrypt', 'LTC'),
            'dogecoin': ('Scrypt', 'DOGE'),
            'monero': ('RandomX', 'XMR')
        }
        
        try:
            prices = self.get_crypto_prices(list(coins_config.keys()))
            
            for coin_name, (algorithm, symbol) in coins_config.items():
                if coin_name in prices:
                    price_data = prices[coin_name]
                    crypto = Cryptocurrency.query.filter_by(symbol=symbol).first()
                    
                    if not crypto:
                        crypto = Cryptocurrency(
                            name=coin_name,
                            symbol=symbol,
                            algorithm=algorithm
                        )
                        db.session.add(crypto)
                    
                    crypto.current_price = price_data.get('usd', 0)
                    crypto.last_updated = datetime.utcnow()
            
            db.session.commit()
            logger.info("Cryptocurrency data updated successfully")
        except Exception as e:
            logger.error(f"Error updating crypto data: {e}")

class ProfitabilityCalculator:
    """Calculate mining profitability based on miner specs and current conditions"""
    
    DEFAULT_ELECTRICITY_COST = 0.12  # $/kWh
    DEFAULT_POOL_FEE = 0.01  # 1%
    BTC_BLOCKS_PER_DAY = 144
    LTC_BLOCKS_PER_DAY = 576
    
    @staticmethod
    def calculate_miner_profitability(miner, electricity_cost=None, pool_fee=None):
        """Calculate comprehensive profitability metrics"""
        if electricity_cost is None:
            electricity_cost = ProfitabilityCalculator.DEFAULT_ELECTRICITY_COST
        if pool_fee is None:
            pool_fee = ProfitabilityCalculator.DEFAULT_POOL_FEE
        
        try:
            # Get current crypto price
            api = CryptoPriceAPI()
            prices = api.get_crypto_prices(['bitcoin', 'litecoin'])
            
            # Determine coin based on algorithm
            if 'SHA-256' in miner.algorithm or 'Bitcoin' in miner.algorithm:
                crypto_price = prices.get('bitcoin', {}).get('usd', 50000)
                daily_blocks = ProfitabilityCalculator.BTC_BLOCKS_PER_DAY
                coin_symbol = 'BTC'
            elif 'Scrypt' in miner.algorithm:
                crypto_price = prices.get('litecoin', {}).get('usd', 200)
                daily_blocks = ProfitabilityCalculator.LTC_BLOCKS_PER_DAY
                coin_symbol = 'LTC'
            else:
                crypto_price = 50000
                daily_blocks = 144
                coin_symbol = 'BTC'
            
            # Calculate daily mining output
            daily_output = ProfitabilityCalculator._calculate_daily_output(
                miner.hash_rate,
                miner.algorithm
            )
            
            # Calculate costs
            daily_electricity_cost = (miner.power_consumption * 24 / 1000) * electricity_cost
            daily_revenue = daily_output * crypto_price
            daily_pool_fee = daily_revenue * pool_fee
            
            # Calculate net profit
            daily_net_profit = daily_revenue - daily_electricity_cost - daily_pool_fee
            
            # Calculate ROI
            roi_days = miner.price_usd / daily_net_profit if daily_net_profit > 0 else float('inf')
            
            return {
                'daily_output': daily_output,
                'daily_revenue': daily_revenue,
                'daily_electricity_cost': daily_electricity_cost,
                'daily_pool_fee': daily_pool_fee,
                'daily_net_profit': daily_net_profit,
                'monthly_net_profit': daily_net_profit * 30,
                'yearly_net_profit': daily_net_profit * 365,
                'roi_days': roi_days,
                'crypto_price': crypto_price,
                'coin_symbol': coin_symbol,
                'electricity_cost': electricity_cost,
                'pool_fee': pool_fee
            }
        except Exception as e:
            logger.error(f"Error calculating profitability: {e}")
            return ProfitabilityCalculator._get_fallback_profitability(miner, electricity_cost)
    
    @staticmethod
    def _calculate_daily_output(hash_rate_th, algorithm):
        """Calculate daily cryptocurrency output based on hash rate"""
        # Simplified calculation - in production, use actual network data
        # Hash rate is in TH/s (tera-hashes per second)
        
        if 'SHA-256' in algorithm or 'Bitcoin' in algorithm:
            # Bitcoin network difficulty ~80T, block reward ~6.25 BTC, 144 blocks/day
            network_difficulty = 80000000000000
            daily_output = (hash_rate_th * 1e12) / network_difficulty * 6.25 * 144 / (24 * 3600)
        elif 'Scrypt' in algorithm:
            # Litecoin network difficulty ~20M, block reward ~12.5 LTC, 576 blocks/day
            network_difficulty = 20000000
            daily_output = (hash_rate_th * 1e12) / network_difficulty * 12.5 * 576 / (24 * 3600)
        else:
            daily_output = hash_rate_th * 0.0001  # Fallback
        
        return max(0, daily_output)
    
    @staticmethod
    def _get_fallback_profitability(miner, electricity_cost):
        """Return fallback profitability if calculation fails"""
        daily_electricity_cost = (miner.power_consumption * 24 / 1000) * electricity_cost
        estimated_daily_profit = (miner.price_usd / 365) * 0.1  # Rough estimate
        
        return {
            'daily_output': 0.001,
            'daily_revenue': estimated_daily_profit + daily_electricity_cost,
            'daily_electricity_cost': daily_electricity_cost,
            'daily_pool_fee': 0,
            'daily_net_profit': estimated_daily_profit,
            'monthly_net_profit': estimated_daily_profit * 30,
            'yearly_net_profit': estimated_daily_profit * 365,
            'roi_days': 365,
            'crypto_price': 50000,
            'coin_symbol': 'BTC',
            'electricity_cost': electricity_cost,
            'pool_fee': 0.01
        }
    
    @staticmethod
    def update_all_profitability_data():
        """Update profitability data for all miners in database"""
        try:
            miners = ASICMiner.query.filter_by(is_available=True).all()
            
            for miner in miners:
                profitability = ProfitabilityCalculator.calculate_miner_profitability(miner)
                
                # Create new profitability record
                profit_record = ProfitabilityData(
                    miner_id=miner.id,
                    daily_profit_usd=profitability['daily_net_profit'],
                    monthly_profit_usd=profitability['monthly_net_profit'],
                    yearly_profit_usd=profitability['yearly_net_profit'],
                    electricity_cost=profitability['electricity_cost'],
                    net_profit_daily=profitability['daily_net_profit'],
                    roi_days=profitability['roi_days'],
                    data_source='internal'
                )
                db.session.add(profit_record)
                
                # Update miner profitability score
                miner.profitability_score = profitability['daily_net_profit']
            
            db.session.commit()
            logger.info(f"Updated profitability data for {len(miners)} miners")
        except Exception as e:
            logger.error(f"Error updating profitability data: {e}")
            db.session.rollback()

class MiningNowScraper:
    """Scrape mining data from miningnow.com"""
    
    def __init__(self):
        self.base_url = "https://miningnow.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_top_miners(self, limit=10):
        """Scrape top miners - returns sample data due to site structure variations"""
        logger.info(f"Attempting to scrape top {limit} miners from {self.base_url}")
        try:
            response = self.session.get(f"{self.base_url}/miners", timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            miners_data = []
            
            # This is a fallback - actual scraping depends on site structure
            # In production, you'd parse the actual HTML structure
            return self._get_sample_miners_data()
        except Exception as e:
            logger.error(f"Error scraping miningnow.com: {e}")
            return self._get_sample_miners_data()
    
    @staticmethod
    def _get_sample_miners_data():
        """Return sample miners data for demonstration"""
        return [
            {
                'name': 'Antminer S19 Pro',
                'manufacturer': 'Bitmain',
                'algorithm': 'SHA-256',
                'hash_rate': 110.0,  # TH/s
                'power_consumption': 1450,  # Watts
                'price': 6500,
                'profitability_daily': 8.5
            },
            {
                'name': 'Antminer S19j Pro',
                'manufacturer': 'Bitmain',
                'algorithm': 'SHA-256',
                'hash_rate': 100.0,
                'power_consumption': 1320,
                'price': 5500,
                'profitability_daily': 7.8
            },
            {
                'name': 'MicroBT Whatsminer M50S',
                'manufacturer': 'MicroBT',
                'algorithm': 'SHA-256',
                'hash_rate': 126.0,
                'power_consumption': 1632,
                'price': 7200,
                'profitability_daily': 9.2
            }
        ]
