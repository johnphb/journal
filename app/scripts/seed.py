from app.extensions.database import db
from app.simple_pages.models import User, Entries
from datetime import datetime, timezone

def seed_database():
    # Check if the database is already seeded
    if User.query.filter_by(uname='john3').first():
        return 'Database is already seeded.'

    # Create a new user
    new_user = User(uname='user', pword='password', created_at=datetime.now(timezone.utc))
    db.session.add(new_user)
    db.session.commit()

    # Create an entry for the user
    new_entry = Entries(user_id=new_user.id, date=datetime.now().date(), title='Sample Entry', content='This is a sample entry.')
    db.session.add(new_entry)
    db.session.commit()

    return 'Database seed completed!'
