from .models import db, User, Profile

# --- USER CRUD ---
def create_user(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return user

def get_user(user_id):
    return User.query.get(user_id)

def update_user(user_id, username):
    user = User.query.get(user_id)
    if user:
        user.username = username
        db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user

# --- PROFILE CRUD ---
def create_profile(user_id, bio):
    profile = Profile(user_id=user_id, bio=bio)
    db.session.add(profile)
    db.session.commit()
    return profile

def get_profile(profile_id):
    return Profile.query.get(profile_id)

def update_profile(profile_id, bio):
    profile = Profile.query.get(profile_id)
    if profile:
        profile.bio = bio
        db.session.commit()
    return profile

def delete_profile(profile_id):
    profile = Profile.query.get(profile_id)
    if profile:
        db.session.delete(profile)
        db.session.commit()
    return profile
