
from ebay import app, db
from ebay.models import items as mitems
from flask import Flask, Response, request, json
from flask import Blueprint
from ebay.utils import seasoned_response


mod = Blueprint('ebay', __name__, url_prefix='/ebay')

#ebay/add
@mod.route('/add', methods=['POST'])
#@ma.login_required
#@authtest()
def ebay_add():
    r = request.get_json()
    result = []
    for i in r:
        item = mitems.items()
        item.from_json(i)
        item['title'] = item['title'].decode('unicode_escape').encode('ascii', 'ignore')
        db.session.add(item)
        result.append(item.to_json())
    db.session.commit()
    if result:
        app.logger.info('%s %r', "Successfully added new records to database:", result)
    else:
        app.logger.info("No new records added to database")
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

    item = mitems.items.query.filter_by(**rebuiltjson).all()
    result = [mitems.items.to_json(x) for x in item]

    app.logger.info('%s', "Call to get succeeded.")
    return "200"


#ebay/list
@mod.route('/list')
#@ma.login_required
#@authtest()
def ebay_list():
    item = mitems.items.query.all()
    result = [mitems.items.to_json(x) for x in item]

    app.logger.info('%s', "Call to list succeeded.")
    return seasoned_response(result, "200")


#ebay/listids
@mod.route('/listids')
#@ma.login_required
#@authtest()
def ebay_list_ids():
    item = mitems.items.query.all()
    result = [mitems.items.to_json(x)['id'] for x in item]

    app.logger.info('%s', "Call to list succeeded.")
    return seasoned_response(result, "200")


#ebay/listitemids
@mod.route('/listitemids')
#@ma.login_required
#@authtest()
def ebay_list_item_ids():
    item = mitems.items.query.all()
    result = [mitems.items.to_json(x)['item_id'] for x in item]

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
