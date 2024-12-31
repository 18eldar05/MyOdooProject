from odoo import http
from odoo.http import request


class Blog(http.Controller):

    @http.route('/blog/attribute', auth='public', csrf=False, type='http', methods=['POST'])
    def create_attribute(self, **kw):
        try:
            print("HERE", kw)
            data = {
                'name': kw['name'],
                'type': kw['type'],
                'data_type': kw['data_type'],
                'required': bool(kw['required']),
                'length': int(kw['length']),
            }
            attribute = request.env['blog.attribute'].sudo().create(data)
            data.update({'id': attribute.id})
        except Exception as e:
            return request.make_json_response(repr(e), headers={"Content-Type": "application/json"}, cookies=None, status=400)
        return request.make_json_response(data, headers={"Content-Type": "application/json"}, cookies=None, status=200)

    @http.route('/blog/document', auth='public', csrf=False, type='http', methods=['POST'])
    def create_document(self, **kw):
        try:
            data = {
                'name': kw['name'],
                'description': kw['description'],
                'version': float(kw['version']),
                'active': bool(kw['active']),
                'attribute_ids': [int(x) for x in kw['attribute_ids'].split()],
            }
            document = request.env['blog.document'].sudo().create(data)
            data.update({'id': document.id})
        except Exception as e:
            return request.make_json_response(repr(e), headers={"Content-Type": "application/json"}, cookies=None, status=400)
        return request.make_json_response(data, headers={"Content-Type": "application/json"}, cookies=None, status=200)

    @http.route('/blog/attribute/get_all', auth='public', csrf=False, type='json', methods=['GET'])
    def get_all_attributes(self, **kw):
        attributes = request.env['blog.attribute'].sudo().search([])
        attributes_list = []
        for attribute in attributes:
            attributes_list.append({
                'uuid': attribute.uuid,
                'name': attribute.name,
                'type': attribute.type,
                'data_type': attribute.data_type,
                'required': attribute.required,
                'length': attribute.length,
                'id': attribute.id,
            })
        return attributes_list

    @http.route('/blog/document/get_all', auth='public', csrf=False, type='json', methods=['GET'])
    def get_all_documents(self, **kw):
        documents = request.env['blog.document'].sudo().search([])
        documents_list = []
        for document in documents:
            documents_list.append({
                'uuid': document.uuid,
                'name': document.name,
                'description': document.description,
                'version': document.version,
                'active': document.active,
                'attribute_ids': [attribute_id.id for attribute_id in document.attribute_ids],
                'id': document.id,
            })
        return documents_list

    @http.route('/blog/attribute', auth='public', csrf=False, type='http', methods=['GET'])
    def get_attribute(self, **kw):
        try:
            attribute = request.env['blog.attribute'].sudo().search([('id', '=', int(kw['id']))])
        except Exception as e:
            return request.make_json_response(repr(e), headers={"Content-Type": "application/json"}, cookies=None, status=404)
        data = {
            'uuid': attribute.uuid,
            'name': attribute.name,
            'type': attribute.type,
            'data_type': attribute.data_type,
            'required': attribute.required,
            'length': attribute.length,
        }
        return request.make_json_response(data, headers={"Content-Type": "application/json"}, cookies=None, status=200)

    @http.route('/blog/document', auth='public', csrf=False, type='http', methods=['GET'])
    def get_document(self, **kw):
        try:
            document = request.env['blog.document'].sudo().search([('id', '=', int(kw['id']))])
        except Exception as e:
            return request.make_json_response(repr(e), headers={"Content-Type": "application/json"}, cookies=None, status=404)
        data = {
            'uuid': document.uuid,
            'name': document.name,
            'description': document.description,
            'version': document.version,
            'active': document.active,
            'attribute_ids': [attribute_id.id for attribute_id in document.attribute_ids],
        }
        return request.make_json_response(data, headers={"Content-Type": "application/json"}, cookies=None, status=200)

    @http.route('/blog/document/update', auth='public', csrf=False, type='http', methods=['POST'])
    def update_document(self, **kw):
        try:
            document = request.env['blog.document'].sudo().search([('id', '=', int(kw['id']))])
        except Exception as e:
            return request.make_json_response(repr(e), headers={"Content-Type": "application/json"}, cookies=None, status=404)
        data = {
            'name': document['name'],
            'description': document['description'],
            'version': document['version'] + 1.0,
            'active': True,
            'attribute_ids': document['attribute_ids'],
        }
        try:
            request.env['blog.document'].sudo().create(data)
            data['attribute_ids'] = [attribute_id.id for attribute_id in document.attribute_ids]
            document.write({'active': False})
        except Exception as e:
            return request.make_json_response(repr(e), headers={"Content-Type": "application/json"}, cookies=None, status=400)
        return request.make_json_response(data, headers={"Content-Type": "application/json"}, cookies=None, status=200)
