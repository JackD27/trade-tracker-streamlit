import sqlite3
from typing import Optional, List, Dict
from trade_models import Account, Trade, Security
from datetime import datetime


DB_TRADE_FILE = 'trades.db'

def init_db():
    with sqlite3.connect(DB_TRADE_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        initial_balance REAL,
                        current_balance REAL
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS securities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ticker TEXT UNIQUE,
                        name TEXT,
                        type TEXT,
                        description TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS trades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_id INTEGER,
                        security_id INTEGER,
                        entry_price REAL,
                        exit_price REAL,
                        quantity INTEGER,
                        entry_date TEXT,
                        exit_date TEXT,
                        details TEXT,
                        FOREIGN KEY(account_id) REFERENCES accounts(id),
                        FOREIGN KEY(security_id) REFERENCES securities(id)
                    )''')
        conn.commit()

def save_account(account: Account) -> int:
    with sqlite3.connect(DB_TRADE_FILE) as conn:
        c = conn.cursor()
        if account.id is None:  # new account
            c.execute('''INSERT INTO accounts (name, initial_balance, current_balance)
                         VALUES (?, ?, ?)''',
                      (account.name, account.initial_balance, account.initial_balance))
            account.id = c.lastrowid
        else:  # update balance
            c.execute('''UPDATE accounts SET current_balance=? WHERE id=?''',
                      (account.current_balance, account.id))
        conn.commit()
    return account.id

def save_security(security: Security) -> int:
    with sqlite3.connect(DB_TRADE_FILE) as conn:
        c = conn.cursor()
        if security.id is None:
            c.execute('''INSERT OR IGNORE INTO securities (ticker, name, type, description)
                         VALUES (?, ?, ?, ?)''',
                      (security.ticker, security.name, security.type, security.description))
            # fetch existing or new id
            c.execute("SELECT id FROM securities WHERE ticker=?", (security.ticker,))
            security.id = c.fetchone()[0]
        conn.commit()
    return security.id

def get_security_by_ticker(ticker: str) -> Optional[Security]:
    with sqlite3.connect(DB_TRADE_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id, ticker, name, type, description FROM securities WHERE ticker=?", (ticker,))
        row = c.fetchone()
        if row:
            return Security(id=row[0], ticker=row[1], name=row[2], type=row[3], description=row[4])
    return None

def save_trade(trade: Trade) -> int:
    if trade.security.id is None:
        trade.security.id = save_security(trade.security)
    security_id = get_security_by_ticker(trade.security.ticker)
    with sqlite3.connect(DB_TRADE_FILE) as conn:
        c = conn.cursor()
        if trade.id is None:
            c.execute('''INSERT INTO trades 
                         (account_id, security_id, entry_price, exit_price, quantity, entry_date, exit_date, details)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (trade.account_id, security_id,
                       trade.entry_price, trade.exit_price, trade.quantity,
                       trade.entry_date.isoformat(),
                       trade.exit_date.isoformat() if trade.exit_date else None,
                       trade.details))
            trade.id = c.lastrowid
        conn.commit()
    return trade.id


def get_accounts() -> List[Account]:
    accounts = []
    with sqlite3.connect(DB_TRADE_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, initial_balance, current_balance FROM accounts")
        for acc_id, name, init_bal, cur_bal in c.fetchall():
            accounts.append(Account(acc_id, name, init_bal, cur_bal))
    return accounts

def get_account_by_id(account_id: int) -> Optional[Account]:
    with sqlite3.connect(DB_TRADE_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, initial_balance, current_balance FROM accounts WHERE id=?", (account_id,))
        row = c.fetchone()
        if row:
            return Account(id=row[0], name=row[1], initial_balance=row[2], current_balance=row[3])
    return None

def get_all_trades_by_account(account_id: int) -> List[Trade]:
    trades = []
    with sqlite3.connect(DB_TRADE_FILE) as conn:
        c = conn.cursor()
        c.execute('''SELECT t.id, t.entry_price, t.exit_price, t.quantity, 
                            t.entry_date, t.exit_date, t.details, 
                            s.ticker, s.name, s.type, s.description
                     FROM trades t
                     JOIN securities s ON t.security_id = s.id
                     WHERE t.account_id=?''', (account_id,))
        for row in c.fetchall():
            trade = Trade(
                id=row[0],
                account_id=account_id,
                security=Security(id=None, ticker=row[7], name=row[8], type=row[9], description=row[10]),
                entry_price=row[1],
                exit_price=row[2],
                quantity=row[3],
                entry_date=datetime.fromisoformat(row[4]),
                exit_date=datetime.fromisoformat(row[5]) if row[5] else None,
                details=row[6]
            )
            trades.append(trade)
    return trades