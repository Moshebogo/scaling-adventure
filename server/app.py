#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Vendor, Sweet, VendorSweet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/vendors')
def vendors():
    venders = Vendor.query.all()
    venders_to_dict = [vender.to_dict() for vender in venders]
    return make_response(jsonify(venders_to_dict), 200)

@app.route('/vendors/<int:id>')
def vendor_by_id(id):
    vender = Vendor.query.get(id)
    if not vender:
        return make_response(jsonify({"error": "Vendor not found"}), 404)
    else:
        return make_response(jsonify(vender.to_dict()), 200)


@app.route('/sweets', methods =[])
def sweets():
    sweets = Sweet.query.all()
    sweets_to_dict = [sweet.to_dict() for sweet in sweets]
    return make_response(jsonify(sweets_to_dict), 200)

@app.route('/sweets/<int:id>')
def sweet_by_id(id):
    sweet = Sweet.query.get(id)
    if not sweet:
        return make_response(jsonify({"error": "Sweet not found"}), 404)
    if sweet:
        return make_response(jsonify(sweet.to_dict()), 200)
    return ''

@app.route('/vendor_sweets')
def vendor_sweets():
    data = request.get_json()
    new_vendor_sweet = VendorSweet()
    for key in data:
        setattr(new_vendor_sweet, key, data[key])
    db.session.add(new_vendor_sweet)
    db.session.commit()
    return make_response(jsonify(new_vendor_sweet.to_dict()), 201)   


@app.route('/vendor_sweets/<int:id>')
def vendor_sweet_by_id(id):
    vendor_sweets_exists = VendorSweet.query.get(id)
    if not vendor_sweets_exists:
        return make_response(jsonify({"error": "VendorSweet not found"}), 404)
    if vendor_sweets_exists:
        db.session.delete(vendor_sweets_exists)
        db.session.commit()
    return make_response(jsonify({}), 200)


if __name__ == '__main__':
    app.run(port=5555)
