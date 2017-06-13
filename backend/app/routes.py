import json

from flask import Blueprint, render_template, request

from flask_api import status, exceptions

from .models import Client, Feature, ProductArea, db
from .utils import insert_item_by_priority, rearrange_priorities_of_ordered_list

my_routes = Blueprint('routes', __name__)


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
            client_obj = {
                'id': client.id,
                'name': client.name
            }
            product_area_obj = {
                'id': product_area.id,
                'name': product_area.name
            }
            response = {
                'id': new_feature.id,
                'title': new_feature.title,
                'description': new_feature.description,
                'date': new_feature.date,
                'productArea': product_area_obj,
                'client': client_obj,
                'priority': new_feature.priority
            }
            return response, status.HTTP_201_CREATED
        else:
            raise exceptions.ParseError()
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
        response = results
        return response, status.HTTP_200_OK


@my_routes.route('/api/features/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def feature(id, **kwargs):
    feature = Feature.query.get_or_404(id)
    if request.method == 'DELETE':
        client_id = feature.client_id
        feature.delete()
        features = Feature.query.filter_by(client_id=client_id).order_by(Feature.priority).all()
        # after one feature is deleted we need to rearrange the others
        if features:
            features = rearrange_priorities_of_ordered_list(features)
        db.session.commit()
        response = {"message": "feature \"{}\" deleted successfully".format(feature.title)}
        return response, status.HTTP_200_OK

    elif request.method == 'PATCH':
        data = json.loads(request.get_data(as_text=True))
        old_id = feature.client_id
        new_id = int(data.get('clientId', '-1'))
        old_priority = feature.priority
        # we need a different treatment if the client is changed
        if (old_id != new_id):
            # first we get all features of the new selected client
            features = Feature.query.filter_by(client_id=new_id).order_by(Feature.priority).all()
            feature.title = str(data.get('title', ''))
            feature.description = str(data.get('description', ''))
            feature.date = str(data.get('date', ''))
            feature.product_area_id = int(data.get('productAreaId', '-1'))
            feature.priority = int(data.get('priority', '-1'))
            feature.client_id = new_id
            # we insert our feature
            features = insert_item_by_priority(features, feature)
            # rearrange everything and then save
            features = rearrange_priorities_of_ordered_list(features)
            db.session.commit()
            # all the features from our client that was selected before
            # are desorganized so we rearrange it to be correct
            features = Feature.query.filter_by(client_id=old_id).order_by(Feature.priority).all()
            features = rearrange_priorities_of_ordered_list(features)
            db.session.commit()
        else:  # the client wasn't changed, just the priority and maybe other info
            features = Feature.query.filter_by(client_id=old_id).order_by(Feature.priority).all()
            # delete the priority from the list. Notice that the position of priority in the list
            # is equal of the priority itself - 1
            del features[old_priority - 1]
            # rearrange all priorities
            features = rearrange_priorities_of_ordered_list(features)
            feature.title = str(data.get('title', ''))
            feature.description = str(data.get('description', ''))
            feature.date = str(data.get('date', ''))
            feature.product_area_id = int(data.get('productAreaId', '-1'))
            feature.priority = int(data.get('priority', '-1'))
            feature.client_id = new_id
            # insert the edited priority in the right place
            features = insert_item_by_priority(features, feature)
            # rearrange it again
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
        response = {
            'id': feature.id,
            'title': feature.title,
            'description': feature.description,
            'date': feature.date,
            'productArea': product_area_obj,
            'client': client_obj,
            'priority': feature.priority
        }
        return response, status.HTTP_200_OK
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
        response = {
            'id': feature.id,
            'title': feature.title,
            'description': feature.description,
            'date': feature.date,
            'productArea': product_area_obj,
            'client': client_obj,
            'priority': feature.priority
        }
        return response, status.HTTP_200_OK


@my_routes.route('/api/clients', methods=['POST', 'GET'], strict_slashes=False)
def clients():
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        name = str(data.get('name', ''))
        if name:
            client = Client(name=name)
            client.save()
            response = {
                'id': client.id,
                'name': client.name
            }
            return response, status.HTTP_201_CREATED
        else:
            raise exceptions.ParseError()
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
        response = results
        return response, status.HTTP_200_OK


@my_routes.route('/api/product-areas', methods=['POST', 'GET'], strict_slashes=False)
def product_areas():
    if request.method == "POST":
        data = json.loads(request.get_data(as_text=True))
        name = str(data.get('name', ''))
        if name:
            product_area = ProductArea(name=name)
            product_area.save()
            response = {
                'id': product_area.id,
                'name': product_area.name
            }
            return response, status.HTTP_201_CREATED
        else:
            raise exceptions.ParseError()
    else:  # GET
        product_areas = ProductArea.get_all()
        results = []

        for product_area in product_areas:
            obj = {
                'id': product_area.id,
                'name': product_area.name
            }
            results.append(obj)
        response = results
        return response, status.HTTP_200_OK


@my_routes.route('/')
def index():
    return render_template('index.html')
