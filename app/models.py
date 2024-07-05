from sqlalchemy import Column, Integer, String, Boolean, Float
from .database import Base

class MarketData(Base):
    """
    SQLAlchemy model for storing market data.

    This model represents the market data for a specific trading pair,
    including buy and sell prices, high and low prices, open and last prices,
    volume, and the date of the data.

    Attributes:
        id (int): Primary key of the table.
        symbol (str): Trading pair symbol (e.g., BTC-BRL).
        buy (float): Last buy price.
        sell (float): Last sell price.
        high (float): Highest price during the period.
        low (float): Lowest price during the period.
        open (float): Opening price.
        last (float): Last traded price.
        volume (float): Trading volume.
        date (int): Date of the market data (in nanoseconds since epoch).
    """
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    buy = Column(Float)
    sell = Column(Float)
    high = Column(Float)
    low = Column(Float)
    open = Column(Float)
    last = Column(Float)
    volume = Column(Float)
    date = Column(Integer)


class Symbol(Base):
    """
    SQLAlchemy model for storing symbol information.

    This model represents the information for a specific trading symbol,
    including base currency, quote currency, description, and various trading
    attributes such as minimum movement, price scale, session, timezone, and
    fees.

    Attributes:
        id (int): Primary key of the table.
        base_currency (str): Base currency of the symbol (e.g., BTC).
        currency (str): Quote currency of the symbol (e.g., BRL).
        symbol (str): Unique trading symbol (e.g., BTC-BRL).
        description (str): Description of the symbol.
        exchange_listed (bool): Whether the symbol is listed on the exchange.
        exchange_traded (bool): Whether the symbol is tradable on the exchange.
        min_movement (str): Minimum price difference between two consecutive orders.
        price_scale (float): Number of decimal digits allowed for the symbol price.
        session_regular (str): Regular trading session times.
        timezone (str): Timezone where the symbol is trading.
        type (str): Type of symbol (e.g., CRYPTO, DEFI).
        deposit_minimum (float): Minimum value for deposit.
        withdraw_minimum (float): Minimum value for withdrawal.
        withdrawal_fee (float): Withdrawal fee on the exchange.
    """
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String)
    currency = Column(String)
    symbol = Column(String, unique=True, index=True)
    description = Column(String)
    exchange_listed = Column(Boolean)
    exchange_traded = Column(Boolean)
    min_movement = Column(String)
    price_scale = Column(Float)
    session_regular = Column(String)
    timezone = Column(String)
    type = Column(String)
    deposit_minimum = Column(Float)
    withdraw_minimum = Column(Float)
    withdrawal_fee = Column(Float)
