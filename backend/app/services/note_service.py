from ..models.note import Note
from ..models.application import Application
from ..extensions import db


class NoteService:

    @staticmethod
    def _get_application(application_id: str, user_id: str) -> Application | None:
        return Application.query.filter_by(id=application_id, user_id=user_id).first()

    @staticmethod
    def get_all(application_id: str, user_id: str) -> tuple[list | None, int | None]:
        app = NoteService._get_application(application_id, user_id)
        if not app:
            return None, None
        return app.notes, len(app.notes)

    @staticmethod
    def create(application_id: str, user_id: str, content: str) -> Note | None:
        app = NoteService._get_application(application_id, user_id)
        if not app:
            return None

        note = Note(
            application_id=application_id,
            user_id=user_id,
            content=content.strip(),
        )
        db.session.add(note)
        db.session.commit()
        return note

    @staticmethod
    def delete(note_id: str, application_id: str, user_id: str) -> tuple[bool, str | None]:
        app = NoteService._get_application(application_id, user_id)
        if not app:
            return False, 'application_not_found'

        note = Note.query.filter_by(id=note_id, application_id=application_id).first()
        if not note:
            return False, 'note_not_found'

        db.session.delete(note)
        db.session.commit()
        return True, None
