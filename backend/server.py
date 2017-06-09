from flask import Flask, request, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.Text)
    date = db.Column(db.String(10))
    priority = db.Column(db.Integer)
    # FKS
    product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __init__(self, title, description, date, priority, product_area_id, client_id):
        self.title = title
        self.description = description
        self.date = date
        self.priority = priority
        self.product_area_id = product_area_id
        self.client_id = product_area_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Feature.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Feature %r>' % self.title


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # FK
    features = db.relationship('Feature', backref='client', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Client.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Client %r>' % self.name


class ProductArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    features = db.relationship('Feature', backref='product_area', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return ProductArea.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<ProductArea %r>' % self.name


# create db if not exist
db.create_all()

###############################
# Routes
# #############################


@app.route('/features', methods=['POST', 'GET'])
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
            new_feature.save()
            client = Client.query.filter_by(id=new_feature.client_id).first()
            client_obj = {
                'id': client.id,
                'name': client.name
            }
            product_area = ProductArea.query.filter_by(id=new_feature.client_id).first()
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


@app.route('/features/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def feature(id, **kwargs):
    feature = Feature.query.filter_by(id=id).first()
    if not feature:
        abort(404)

    if request.method == 'DELETE':
        feature.delete()
        return {"message": "feature \"{}\" deleted successfully".format(feature.title)}, 200

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


@app.route('/clients', methods=['POST', 'GET'])
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


@app.route('/product-areas', methods=['POST', 'GET'])
def product_areas():
    if request.method == "POST":
        print(request.get_data)
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


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
