from app.app import create_app
from app.simple_pages.models import User, Entries
from app.extensions.database import db
from datetime import datetime, timezone

if __name__ == '__main__':
    app = create_app()
    app.app_context().push()


entries = {
    "01/01/2024": {"TITLE": "title", "CONTENT": "blablablablablabla"}
}

for date, entry in entries.items():
    datetime_object = datetime.strptime(date, '%d/%m/%Y').date()

    new_entry = Entries(
        date=datetime_object, 
        title=entry["TITLE"], 
        content=entry["CONTENT"], 
        user_id=1
    )
    db.session.add(new_entry)

db.session.commit()