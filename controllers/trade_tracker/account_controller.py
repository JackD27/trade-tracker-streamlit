from models.account import Account
from models.base import SessionLocal


class AccountController:
    def __init__(self):
        self.session = SessionLocal()

    def create_account(self, name: str, initial_balance: float):
        account = Account(name=name, initial_balance=initial_balance, current_balance=initial_balance)
        self.session.add(account)
        self.session.commit()
        return account

    def get_accounts(self):
        return self.session.query(Account).all()

    def delete_account(self, account_id: int):
        account = self.session.query(Account).get(account_id)
        if account:
            self.session.delete(account)
            self.session.commit()