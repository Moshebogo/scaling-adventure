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

#  route for all VENDORS
@app.route('/vendors', methods = ['GET', 'POST'])
def vendors():
    # GET for all VENDORS
    if request.method == 'GET':
        vendors = Vendor.query.all()
        vendors_to_dict = [vendor.to_dict() for vendor in vendors]
        return make_response(jsonify(vendors_to_dict), 200)
    # POST for all VENDORS
    if request.method == 'POST':
        body = request.get_json()
        new_vendor = Vendor()
        for key in body:
            setattr(new_vendor, key, body[key])
        db.session.add(new_vendor) 
        db.session.commit()
        return make_response(jsonify(new_vendor.to_dict()), 201)  

#  route for VENDORS by ID
@app.route('/vendors/<int:id>', methods = ['GET', 'DELETE', 'PATCH'])
def vendor_by_id(id):
    vendor_exists = Vendor.query.get(id)
    # validates that 
    if not vendor_exists:
        return make_response(jsonify({"error": "Vendor not found"}), 404)
    elif vendor_exists:
        # GET for VENDOR by ID
        if request.method == 'GET':
            return make_response(jsonify(vendor_exists.to_dict()), 200)
        # DELETE for VENDOR by ID
        elif request.method == 'DELETE':  
            # first deletes all instances of this vendor in vendor_sweets
            VendorSweet.query.filter(id == VendorSweet.vendor_id).delete()
            # and then deletes the vendor 
            db.session.delete(vendor_exists)
            db.session.commit()
            return make_response(jsonify({"status": "DELETE succsessful"}), 200)
        # PATCH for VENDOR by ID
        elif request.method == 'PATCH':
            body = request.get_json()
            for key in body:
                setattr(vendor_exists, key, body[key])
            db.session.add(vendor_exists)
            db.session.commit()
            return make_response(jsonify(vendor_exists.to_dict()), 200)    

        

# route for all sweets
@app.route('/sweets', methods = ['GET', 'POST'])
def sweets():
    #  GET for all sweets 
    if request.method == 'GET':
        sweets = Sweet.query.all()
        sweets_to_dict = [sweet.to_dict() for sweet in sweets]
        return make_response(jsonify(sweets_to_dict), 200)
    #  POST for all sweets
    elif request.method == 'POST':
        body = request.get_json()
        new_sweet = Sweet()
        for key in body:
            setattr(new_sweet, key, body[key])
        db.session.add(new_sweet)    
        db.session.commit()
        return make_response(jsonify(new_sweet.to_dict()), 201)

# route for SWEET by ID
@app.route('/sweets/<int:id>', methods = ['GET', 'DELETE', 'PATCH'])
def sweet_by_id(id):
    sweet = Sweet.query.get(id)
    # validates if sweet exists 
    if not sweet:
        return make_response(jsonify({"error": "Sweet not found"}), 404)
    if sweet:
        # GET for SWEET by ID
        if request.method == 'GET':
            return make_response(jsonify(sweet.to_dict()), 200)
        elif request.method == 'DELETE':
            #  first deletes all instances of this sweet in vendor_sweets
            VendorSweet.query.filter(id == VendorSweet.sweet_id).delete()
            # and the delets the sweet
            db.session.delete(sweet)
            db.session.commit()
            return make_response(jsonify({"status": "DELETE succsessful"}), 200)
        #  PATCH for SWEET by ID
        elif request.method == 'PATCH':
            body = request.get_json()
            for key in body:
                setattr(sweet, key, body[key])
            db.session.add(sweet)
            db.session.commit()
            return make_response(jsonify(sweet.to_dict()), 200)


        
   
#  route for all VendorSweet
@app.route('/vendor_sweets', methods = ['GET', 'POST'])
def vendor_sweets():
    # GET for all vendor_sweets
    if request.method == 'GET':
        vendor_sweets = VendorSweet.query.all()
        vendor_sweets_dict = [vendor_sweet.to_dict() for vendor_sweet in vendor_sweets]
        return make_response(jsonify(vendor_sweets_dict), 200)
    # POST for all vendor_sweets
    elif request.method == 'POST':
        body = request.get_json()
        new_vendor_sweet = VendorSweet()
        try:
            for key in body:
                setattr(new_vendor_sweet, key, body[key])
        # raise ValueError on price
        except ValueError as e:
            return make_response(jsonify({'error': str(e)}), 404)
        # validate new_vendor_sweet, if ok, return its sweets, if not return correct error
        vendor_exists = Vendor.query.get(new_vendor_sweet.vendor_id)
        sweet_exist = Sweet.query.get(new_vendor_sweet.sweet_id)
        if not vendor_exists:
            return make_response(jsonify({"error": "vendor does not exist"}), 404)
        elif not sweet_exist:
            return  make_response(jsonify({"error": "sweet does not exist"}), 404)
        elif vendor_exists and sweet_exist:
            db.session.add(new_vendor_sweet)
            db.session.commit()
            return make_response(jsonify(new_vendor_sweet.sweet.to_dict()), 201)   

# route for VendorSweet by ID
@app.route('/vendor_sweets/<int:id>', methods = ['GET', 'DELETE', 'PATCH'])
def vendor_sweet_by_id(id):
    vendor_sweets_exists = VendorSweet.query.get(id)
    # validates if exists or not
    if not vendor_sweets_exists:
        return make_response(jsonify({"error": "VendorSweet not found"}), 404)
    # methods if vendor_sweets_exists
    if vendor_sweets_exists:
        # GET for VendorSweet by ID
        if request.method == 'GET':
             return make_response(jsonify(vendor_sweets_exists.to_dict()), 200)
        # DELETE for VendorSweet by ID
        elif request.method == 'DELETE':    
            db.session.delete(vendor_sweets_exists)
            db.session.commit()
            return make_response(jsonify({"status": "DELETE succsessful"}), 200)
        # PATCH for VendorSweet by ID
        elif request.method == 'PATCH':
            body = request.get_json()
            for key in body:
                setattr(vendor_sweets_exists, key, body[key])
                db.session.add(vendor_sweets_exists)
                db.session.commit()
                return make_response(jsonify(vendor_sweets_exists.to_dict()), 201)

if __name__ == '__main__':
    app.run(port=5555)