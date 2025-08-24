import os
import json
from typing import List, Dict
from trade_models import Trade, Security, Account
from pathlib import Path
from dataclasses import asdict
from datetime import datetime
from db_helper import save_account, get_accounts, save_trade, get_all_trades_by_account, init_db

def create_account(account: Account) -> None:
    """Create a new account and save it to the file."""
    accounts = get_accounts()
    if any(acc.id == account.id for acc in accounts):
        raise ValueError(f"Account '{account.name}' already exists.")
    save_account(account)


def add_trades_to_account(account_id: int, trades: List[Trade]) -> None:
    """Add trades to an existing account."""
    accounts = get_accounts()
    if not any(acc.id == account_id for acc in accounts):
        raise ValueError(f"Account with ID {account_id} does not exist.")
    for trade in trades:
        trade.account_id = account_id
        save_trade(trade)

def get_trades_by_account(account_id: int) -> List[Trade]:
    """Retrieve all trades for a specific account."""
    return get_all_trades_by_account(account_id)


init_db()
account = Account(    name="Jackson's Account",
    initial_balance=10000.0,
)

print(get_accounts())