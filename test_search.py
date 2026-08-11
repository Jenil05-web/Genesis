from src.db.session import get_session
from src.db.models import Incident
from sqlmodel import select

session = next(get_session())
incidents = session.exec(select(Incident)).all()
for i in incidents:
    print(i.thread_id, i.situation, i.approved)