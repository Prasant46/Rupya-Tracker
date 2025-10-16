from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str(data_key="$id")
    accountId = fields.Str()
    name = fields.Str()
    email = fields.Email()
    avatarUrl = fields.Str(allow_none=True)

class ExpenseSchema(Schema):
    id = fields.Str(data_key="$id")
    owner = fields.Str()
    title = fields.Str()
    description = fields.Str(allow_none=True)
    amount = fields.Float()
    date = fields.DateTime()
    isTrashed = fields.Bool(data_key="isTrashed")