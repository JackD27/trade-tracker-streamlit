from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
os.makedirs(base_dir, exist_ok=True)

db_path = os.path.join(base_dir, "portfolio.db")

Base = declarative_base()
engine = create_engine(f"sqlite:///{db_path}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    security_id = Column(Integer, ForeignKey("securities.id"))
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    entry_date = Column(DateTime, default=datetime.utcnow)
    exit_date = Column(DateTime, nullable=True)
    details = Column(String, default="")

    account = relationship("Account", back_populates="trades")
    security = relationship("Security")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    initial_balance = Column(Float, nullable=False)
    current_balance = Column(Float, nullable=False)

    # Cascade delete: all trades deleted if account deleted
    trades = relationship(
        "Trade",
        back_populates="account",
        cascade="all, delete, delete-orphan"
    )

    def add_trade(self, session: Session, trade: Trade):
        """
        Adds a Trade object to this account:
        - Ensures the security exists (or creates it)
        - Links the trade to this account
        - Updates current balance
        - Commits the changes
        """
        # Ensure entry_date is set
        if trade.entry_date is None:
            trade.entry_date = datetime.utcnow()

        # Get or create the security
        security = get_or_create_security(
            session,
            trade.security.ticker,
            trade.security.name,
            trade.security.type,
            trade.security.description
        )

        trade.security = security
        trade.account = self
        session.add(trade)

        # Update account balance
        pnl = (trade.exit_price - trade.entry_price) * trade.quantity
        self.current_balance += pnl

        # Add trade and commit
        session.commit()

        return trade

class Security(Base):
    __tablename__ = "securities"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, default="", nullable=True)


Base.metadata.create_all(engine)

def get_or_create_security(session, ticker: str, name: str, type_: str, description: str = ""):
    """
    Returns a Security object. If the ticker exists in DB, returns the existing one.
    Otherwise, creates a new Security and adds it to the session.
    """
    security = session.query(Security).filter_by(ticker=ticker.upper()).first()
    if security is None:
        security = Security(ticker=ticker.upper(), name=name, type=type_, description=description)
        session.add(security)
        session.commit()  # commit so it gets an id
    return security

acc = Account(name="Jackson's Account", initial_balance=10000, current_balance=10000)

# Create security
sec1 = get_or_create_security(session, "AAPL", "Apple Inc.", "Stock")
sec2 = get_or_create_security(session, "AAPL", "Apple Inc.", "Stock")  # returns the same record

print("Yo", sec1.id, sec2.id)

sec = get_or_create_security(session, "AAPL", "Apple Inc.", "Stock")

# Create trade
trade = Trade(
    id=None,
    account_id=None,  # will be linked automatically
    security=Security(id=None, ticker="AAPL", name="Apple Inc.", type="Stock"),
    entry_price=150,
    exit_price=160,
    quantity=10,
    entry_date=datetime.now(),
    details="Swing trade"
)

trade2 = Trade(
    id=None,
    account_id=None,  # will be linked automatically
    security=Security(id=None, ticker="AAPL", name="Apple Inc.", type="Stock"),
    entry_price=155,
    exit_price=165,
    quantity=5,
    entry_date=datetime.now(),
    details="Day trade"
)

acc.add_trade(session, trade)
acc.add_trade(session, trade2)

# Add to session
session.add_all([acc, sec, trade])
session.commit()

# Check trades
print(f"Account {acc.name} has {len(acc.trades)} trade(s).")

# Delete account
session.delete(acc)
session.commit()

# Check trades after deletion
remaining_trades = session.query(Trade).all()
print(f"Remaining trades: {len(remaining_trades)}")  # should be 0