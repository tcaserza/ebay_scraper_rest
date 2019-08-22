
from ebay import app, db
from ebay.models import items as mitems
from flask import Flask, Response, request, json, jsonify, url_for, g, _request_ctx_stack, abort, has_request_context, session, make_response, send_file
from flask import Blueprint
from ebay.utils import seasoned_response


mod = Blueprint('ebay', __name__, url_prefix='/ebay')

#ebay/add
@mod.route('/add', methods=['POST'])
#@ma.login_required
#@authtest()
def ebay_add():
    r = request.get_json()
    item = mitems.items()
    item.from_json(r)
    db.session.add(item)
    db.session.commit()
    result = item.to_json()
    app.logger.info('%s %r', "Successfully added new record to database:", result)
    return seasoned_response(result, "200")


#ebay/delete
@mod.route('/deletebyid', methods=['GET', 'PUT'])
@mod.route('/delete', methods=['GET', 'PUT'])
#@ma.login_required
#@authtest()
def ebay_delete():
    r = request.get_json()
    if "id" in r:
        item = mitems.items.query.filter_by(id=r['id'])
    else:
        app.logger.info('%s', "Exited, need rackunit to delete.")
        return "409"
    if item.first() is None:
        app.logger.info('%s', "Exited, record not found in database.")
        return "404"

    # Display the record to be deleted
    deleted_record = item.first().to_json()

    item.delete()
    db.session.commit()
    app.logger.info('%s %r', "Successfully deleted record from database:", deleted_record)
    return "200"


#ebay/get
@mod.route('/get', methods=['GET', 'PUT'])
#@ma.login_required
#@authtest()
def ebay_get():
    rebuiltjson = {}
    for key, value in request.get_json().iteritems():
        for keyname in ["id", "item_id", "name", "end_date", "price"]:
            if key == keyname:
                rebuiltjson[keyname] = value

    if len(rebuiltjson) == 0:
        app.logger.info('%s', "Exited, user provides no search data.")
        return "400"

    stat = mitems.items.query.filter_by(**rebuiltjson).all()
    result = [mitems.items.to_json(x) for x in stat]

    app.logger.info('%s', "Call to get succeeded.")
    return "200"


#ebay/list
@mod.route('/list')
#@ma.login_required
#@authtest()
def ebay_list():
    stat = mitems.items.query.all()
    result = [mitems.items.to_json(x) for x in stat]

    app.logger.info('%s', "Call to list succeeded.")
    return seasoned_response(result, "200")


#ebay/update
@mod.route('/updatebyid', methods=['PUT'])
@mod.route('/update', methods=['PUT'])
#@ma.login_required
#@authtest()
def ebay_update():
    r = request.get_json()
    if "id" in r:
        item = mitems.items.query.filter_by(id=r['id']).first()
    else:
        app.logger.info('%s', "Exited, need id to update.")
        return "400"

    if item is None:
        app.logger.info('%s', "Exited, record not found in database.")
        return "404"

    for key, value in r.iteritems():
        item[key] = value

    db.session.commit()
    app.logger.info('%s %r', "Successfully updated record in database:",item.to_json())
    return "200"
