import json

from flask import Blueprint, abort, jsonify, render_template, request

from models import Client, Feature, ProductArea, db
from utils import insert_item_by_priority, rearrange_priorities_of_ordered_list

my_routes = Blueprint('routes', __name__, template_folder='templates')


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
            features = Feature.query.order_by(Feature.priority).filter_by(client_id=client_id).all()
            features = insert_item_by_priority(features, new_feature)
            features = rearrange_priorities_of_ordered_list(features)
            db.session.add(new_feature)
            db.session.commit()

            client = Client.query.get_or_404(client_id)
            product_area = ProductArea.query.get_or_404(product_area_id)
            if not client or not product_area:
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
            client = Client.query.get_or_404(feature.client_id)
            client_obj = {
                'id': client.id,
                'name': client.name
            }
            product_area = ProductArea.query.get_or_404(
                feature.product_area.id)
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
    feature = Feature.query.get_or_404(id)
    if request.method == 'DELETE':
        client_id = feature.client_id
        feature.delete()
        features = Feature.query.filter_by(client_id=client_id).order_by(Feature.priority).all()
        if features:
            features = rearrange_priorities_of_ordered_list(features)
        db.session.commit()
        response = jsonify({"message": "feature \"{}\" deleted successfully".format(feature.title)})
        response.status_code = 200
        return response

    elif request.method == 'PATCH':
        data = json.loads(request.get_data(as_text=True))
        old_id = feature.client_id
        new_id = int(data.get('clientId', '-1'))
        old_priority = feature.priority
        print(old_id, feature.client_id)
        if (old_id != new_id):
            print('cade')
            features = Feature.query.filter_by(client_id=new_id).order_by(Feature.priority).all()
            feature.title = str(data.get('title', ''))
            feature.description = str(data.get('description', ''))
            feature.date = str(data.get('date', ''))
            feature.product_area_id = int(data.get('productAreaId', '-1'))
            feature.priority = int(data.get('priority', '-1'))
            feature.client_id = new_id
            features = insert_item_by_priority(features, feature)
            features = rearrange_priorities_of_ordered_list(features)
            db.session.commit()
            features = Feature.query.filter_by(client_id=old_id).order_by(Feature.priority).all()
            features = rearrange_priorities_of_ordered_list(features)
            for f in features:
                print(f.priority)
            db.session.commit()
        else:
            features = Feature.query.filter_by(client_id=old_id).order_by(Feature.priority).all()
            del features[old_priority - 1]
            features = rearrange_priorities_of_ordered_list(features)
            feature.title = str(data.get('title', ''))
            feature.description = str(data.get('description', ''))
            feature.date = str(data.get('date', ''))
            feature.product_area_id = int(data.get('productAreaId', '-1'))
            feature.priority = int(data.get('priority', '-1'))
            feature.client_id = new_id
            features = insert_item_by_priority(features, feature)
            features = rearrange_priorities_of_ordered_list(features)
            db.session.commit()
        client = Client.query.get_or_404(feature.client_id)
        client_obj = {
            'id': client.id,
            'name': client.name
        }
        product_area = ProductArea.query.get_or_404(feature.product_area_id)
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
        client = Client.query.get_or_404(feature.client_id)
        client_obj = {
            'id': client.id,
            'name': client.name
        }
        product_area = ProductArea.query.get_or_404(feature.product_area_id)
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
            max_priorities = Client.query.get_or_404(
                client.id).features.count() + 1
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
