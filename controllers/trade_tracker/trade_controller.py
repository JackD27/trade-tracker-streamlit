from models.account import Account
from models.base import SessionLocal
from models.trade import Trade
from security_controller import SecurityController


class TradeController:
    def __init__(self):
        self.session = SessionLocal()
        self.security_controller = SecurityController()

    def add_trade(self, account_id: int,
                  security_ticker: str,
                  security_name: str,
                  security_type: str,
                  entry_price: float,
                  exit_price: float,
                  fees: float,
                  quantity: int,
                  details=""):
        account = self.session.query(Account).get(account_id)
        if not account:
            return None

        # Ensure security exists
        security = self.security_controller.get_or_create_security(security_ticker, security_name, security_type)

        trade = Trade(
            account=account,
            security=security,
            entry_price=entry_price,
            exit_price=exit_price,
            fees=fees,
            quantity=quantity,
            details=details,
        )

        self.session.add(trade)
        # Update balance
        pnl = ((exit_price - entry_price) * quantity) - fees
        account.current_balance += pnl
        self.session.commit()
        return trade