from sqlalchemy.orm import sessionmaker
from models import Team
from connection import engine

Session = sessionmaker(bind=engine)

def create_team(name, city=None, coach_name=None):
    if not name:
        raise ValueError("Please provide a team name")
    
    session = Session()
    try:
        exists = session.query(Team).filter(Team.name == name).first()
        if exists:
            raise ValueError({"message": "Team already exists"})
        
        new_team = Team(name=name, city=city, coach_name=coach_name)
        session.add(new_team)
        session.commit()
        session.refresh(new_team)
        return new_team
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def read_teams():
    session = Session()
    try:
        return session.query(Team).all()
    except Exception:
        raise
    finally:
        session.close()


def read_team(id):
    if not id:
        raise ValueError({"message": "Please provide an id"})
    
    session = Session()
    try:
        team = session.query(Team).filter(Team.id == id).first()
        if not team:
            raise ValueError({"message": "Team not found"})
        return team
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def update_team(id, name=None, city=None, coach_name=None):
    if not id:
        raise ValueError({"message": "Please provide an id"})
    
    session = Session()
    try:
        team = session.query(Team).filter(Team.id == id).first()
        if not team:
            raise ValueError({"message": "Team not found"})
        
        if name:
            team.name = name
        if city is not None:
            team.city = city
        if coach_name is not None:
            team.coach_name = coach_name
        
        session.commit()
        session.refresh(team)
        return team
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_team(id):
    if not id:
        raise ValueError({"message": "Please provide an id"})
    
    session = Session()
    try:
        team = session.query(Team).filter(Team.id == id).first()
        if not team:
            raise ValueError({"message": "Team not found"})
        
        session.delete(team)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
