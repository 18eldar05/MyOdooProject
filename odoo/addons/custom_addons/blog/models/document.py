from odoo import api, fields, models
import uuid


class BlogDocument(models.Model):
    _name = "blog.document"
    _description = "Documents"

    uuid = fields.Char(default=str(uuid.uuid4()))
    name = fields.Char(required=True)
    description = fields.Text()
    version = fields.Float()
    active = fields.Boolean(default=True)
    attribute_ids = fields.Many2many("blog.attribute", "document_attribute_list_relation", "document_id", "attribute_id")
