from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import make_transient


db = SQLAlchemy()


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

    def new_version(self):
        make_transient(self)
        self.id = None

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
