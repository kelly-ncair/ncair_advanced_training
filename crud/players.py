from sqlalchemy.orm import sessionmaker
from models import Player
from connection import engine

Session = sessionmaker(bind=engine)

def create_player(name, position, age, jersey_number, team_id):
    if not all([name, position, age, jersey_number, team_id]):
        raise ValueError("Please provide name, position, age, jersey_number, and team_id")
    
    session = Session()
    try:
        exists = session.query(Player).filter(Player.jersey_number == jersey_number).first()
        if exists:
            raise ValueError({"message": "Jersey number already in use"})
        
        new_player = Player(
            name=name,
            position=position,
            age=age,
            jersey_number=jersey_number,
            team_id=team_id
        )
        session.add(new_player)
        session.commit()
        session.refresh(new_player)
        return new_player
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def read_players():
    session = Session()
    try:
        return session.query(Player).all()
    except Exception:
        raise
    finally:
        session.close()


def read_player(id):
    if not id:
        raise ValueError({"message": "Please provide an id"})
    
    session = Session()
    try:
        player = session.query(Player).filter(Player.id == id).first()
        if not player:
            raise ValueError({"message": "Player not found"})
        return player
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def update_player(id, name=None, position=None, age=None, jersey_number=None, team_id=None):
    if not id:
        raise ValueError({"message": "Please provide an id"})
    
    session = Session()
    try:
        player = session.query(Player).filter(Player.id == id).first()
        if not player:
            raise ValueError({"message": "Player not found"})
        
        if jersey_number is not None:
            # ensures new jersey_number is not already taken by another player
            conflict = session.query(Player).filter(
                Player.jersey_number == jersey_number,
                Player.id != id
            ).first()
            if conflict:
                raise ValueError({"message": "Jersey number already in use"})
            player.jersey_number = jersey_number
        
        if name:
            player.name = name
        if position:
            player.position = position
        if age is not None:
            player.age = age
        if team_id is not None:
            player.team_id = team_id
        
        session.commit()
        session.refresh(player)
        return player
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_player(id):
    if not id:
        raise ValueError({"message": "Please provide an id"})
    
    session = Session()
    try:
        player = session.query(Player).filter(Player.id == id).first()
        if not player:
            raise ValueError({"message": "Player not found"})
        
        session.delete(player)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
