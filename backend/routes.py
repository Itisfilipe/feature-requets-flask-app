import json
from flask import request, jsonify, abort, render_template, Blueprint
from model import Feature, Client, ProductArea

my_routes = Blueprint('routes', __name__, template_folder='templates')


def reorganize_priorities(features, new_feature):
    '''Reorganize feature prioties and save it into db'''
    for feature in features:
        if feature.priority >= new_feature.priority:
            feature.priority += 1
            feature.save()
    new_feature.save()


@my_routes.route('/api/features', methods=['POST', 'GET'], strict_slashes=False)
def features():
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        title = str(data.get('title', ''))
        description = str(data.get('description', ''))
        date = str(data.get('date', ''))
        priority = int(data.get('priority', '-1'))
        product_area_id = int(data.get('productAreaId', '-1'))
        client_id = int(data.get('clientId', '-1'))
        if title and description and date and product_area_id != -1 and client_id != -1 and priority != -1:
            new_feature = Feature(
                title=title,
                description=description,
                date=date,
                priority=priority,
                product_area_id=product_area_id,
                client_id=client_id
            )
            features = Feature.query.filter_by(client_id=client_id)
            reorganize_priorities(features, new_feature)
            client = Client.query.filter_by(id=new_feature.client_id).first()
            product_area = ProductArea.query.filter_by(id=new_feature.client_id).first()
            if not client or not product_area:
                # it would be better use 424 but for simplicity lets use
                # already implemented codes
                abort(404)
            client_obj = {
                'id': client.id,
                'name': client.name
            }
            product_area_obj = {
                'id': product_area.id,
                'name': product_area.name
            }
            response = jsonify({
                'id': new_feature.id,
                'title': new_feature.title,
                'description': new_feature.description,
                'date': new_feature.date,
                'productArea': product_area_obj,
                'client': client_obj,
                'priority': new_feature.priority
            })
            response.status_code = 201
            return response
        else:
            abort(400)
    else:  # GET
        features = Feature.get_all()
        results = []
        for feature in features:
            client = Client.query.filter_by(id=feature.client_id).first()
            client_obj = {
                'id': client.id,
                'name': client.name
            }
            product_area = ProductArea.query.filter_by(id=feature.client_id).first()
            product_area_obj = {
                'id': product_area.id,
                'name': product_area.name
            }
            obj = {
                'id': feature.id,
                'title': feature.title,
                'description': feature.description,
                'date': feature.date,
                'productArea': product_area_obj,
                'client': client_obj,
                'priority': feature.priority
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response


@my_routes.route('/api/features/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def feature(id, **kwargs):
    feature = Feature.query.filter_by(id=id).first()
    if not feature:
        abort(404)

    if request.method == 'DELETE':
        feature.delete()
        response = jsonify({"message": "feature \"{}\" deleted successfully".format(feature.title)})
        response.status_code = 200
        return response

    elif request.method == 'PATCH':
        data = json.loads(request.get_data(as_text=True))
        feature.title = str(data.get('title', ''))
        feature.description = str(data.get('description', ''))
        feature.date = str(data.get('date', ''))
        feature.priority = int(data.get('priority', '-1'))
        feature.product_area_id = int(data.get('productAreaId', '-1'))
        feature.client_id = int(data.get('clientId', '-1'))
        feature.save()
        client = Client.query.filter_by(id=feature.client_id).first()
        client_obj = {
            'id': client.id,
            'name': client.name
        }
        product_area = ProductArea.query.filter_by(id=feature.product_area_id).first()
        product_area_obj = {
            'id': product_area.id,
            'name': product_area.name
        }
        response = jsonify({
            'id': feature.id,
            'title': feature.title,
            'description': feature.description,
            'date': feature.date,
            'productArea': product_area_obj,
            'client': client_obj,
            'priority': feature.priority
        })
        response.status_code = 200
        return response
    else:  # GET
        client = Client.query.filter_by(id=feature.client_id).first()
        client_obj = {
            'id': client.id,
            'name': client.name
        }
        product_area = ProductArea.query.filter_by(id=feature.client_id).first()
        product_area_obj = {
            'id': product_area.id,
            'name': product_area.name
        }
        response = jsonify({
            'id': feature.id,
            'title': feature.title,
            'description': feature.description,
            'date': feature.date,
            'productArea': product_area_obj,
            'client': client_obj,
            'priority': feature.priority
        })
        response.status_code = 200
        return response


@my_routes.route('/api/clients', methods=['POST', 'GET'], strict_slashes=False)
def clients():
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        name = str(data.get('name', ''))
        if name:
            client = Client(name=name)
            client.save()
            response = jsonify({
                'id': client.id,
                'name': client.name
            })
            response.status_code = 201
            return response
    else:  # GET
        clients = Client.get_all()
        results = []
        for client in clients:
            max_priorities = Feature.query.filter_by(client_id=client.id).count() + 1
            obj = {
                'id': client.id,
                'name': client.name,
                'maxPriorities': max_priorities
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response


@my_routes.route('/api/product-areas', methods=['POST', 'GET'], strict_slashes=False)
def product_areas():
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        name = str(data.get('name', ''))
        if name:
            product_area = ProductArea(name=name)
            product_area.save()
            response = jsonify({
                'id': product_area.id,
                'name': product_area.name
            })
            response.status_code = 201
            return response
    else:  # GET
        product_areas = ProductArea.get_all()
        results = []

        for product_area in product_areas:
            obj = {
                'id': product_area.id,
                'name': product_area.name
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response


@my_routes.route('/')
def index():
    return render_template('index.html')