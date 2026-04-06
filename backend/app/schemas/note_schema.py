from marshmallow import fields, validates, ValidationError
from ..extensions import ma
from ..models.note import Note


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = False
        fields = ('id', 'application_id', 'content', 'created_at')


class CreateNoteSchema(ma.Schema):
    content = fields.String(required=True)

    @validates('content')
    def validate_content(self, value: str) -> str:
        if not value or not value.strip():
            raise ValidationError('Note content cannot be empty or whitespace only.')
        return value


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
create_note_schema = CreateNoteSchema()
