from ..models.security import Security

def get_or_create_security(session, ticker: str, name: str, type_: str, description: str = ""):
    security = session.query(Security).filter_by(ticker=ticker.upper()).first()
    if security is None:
        security = Security(ticker=ticker.upper(), name=name, type=type_, description=description)
        session.add(security)
        session.commit()
    return security