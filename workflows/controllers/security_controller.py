from ..models.base import SessionLocal
from ..models.security import Security

class SecurityController:
    def __init__(self):
        self.session = SessionLocal()

    def get_or_create_security(self, ticker: str, name: str, type_: str, description: str = ""):
        security = self.session.query(Security).filter_by(ticker=ticker.upper()).first()
        if not security:
            security = Security(ticker=ticker.upper(), name=name, type=type_, description=description)
            self.session.add(security)
            self.session.commit()
        return security