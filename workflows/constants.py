MARKET_NAME_MAP = {
    'WTI-PHYSICAL - NEW YORK MERCANTILE EXCHANGE': 'USOil',
    'GOLD - COMMODITY EXCHANGE INC.': 'XAU',
    'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE': 'CAD',
    'SWISS FRANC - CHICAGO MERCANTILE EXCHANGE': 'CHF',
    'BRITISH POUND - CHICAGO MERCANTILE EXCHANGE': 'GBP',
    'JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE': 'JPY',
    'USD INDEX - ICE FUTURES U.S.': 'USD',
    'EURO FX - CHICAGO MERCANTILE EXCHANGE': 'EUR',
    'NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE': 'NZD',
    'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE': 'AUD',
    'BITCOIN - CHICAGO MERCANTILE EXCHANGE': 'BTC',
    'NASDAQ MINI - CHICAGO MERCANTILE EXCHANGE': 'NAS100',
    'S&P 500 Consolidated - CHICAGO MERCANTILE EXCHANGE': 'SP500',
    'DJIA x $5 - CHICAGO BOARD OF TRADE': 'US30',
    'UST 10Y NOTE - CHICAGO BOARD OF TRADE': 'US10'
}

MARKETS_TO_KEEP = list(MARKET_NAME_MAP.keys())

MARKET_TYPE = {
    'USOil': 'Commodity',
    'XAU': 'Commodity',
    'CAD': 'Forex',
    'CHF': 'Forex',
    'GBP': 'Forex',
    'JPY': 'Forex',
    'USD': 'Forex',
    'EUR': 'Forex',
    'NZD': 'Forex',
    'AUD': 'Forex',
    'BTC': 'Crypto',
    'NAS100': 'Indices',
    'SP500': 'Indices',
    'US30': 'Indices',
    'US10': 'Bonds'
}

RENAME_COLUMNS = {
    "Market_and_Exchange_Names": "Market_Names",
    "Report_Date_as_MM_DD_YYYY": "Date",
    "NonComm_Positions_Long_All": "NonComm_Long",
    "NonComm_Positions_Short_All": "NonComm_Short",
    "Change_in_NonComm_Long_All": "Change_Long",
    "Change_in_NonComm_Short_All": "Change_Short"
}