from odoo import api, fields, models
import uuid


class BlogAttribute(models.Model):
    _name = "blog.attribute"
    _description = "Attributes"

    uuid = fields.Char(default=str(uuid.uuid4()))
    name = fields.Char(required=True,)
    type = fields.Selection([("key_figure", "key_figure"), ("tag", "tag")])
    data_type = fields.Selection([("serial", "serial"), ("integer", "integer"), ("text", "text"), ("boolean", "boolean")])
    required = fields.Boolean(default=False)
    length = fields.Integer()
