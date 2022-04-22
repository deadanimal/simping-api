# Import flask dependencies
from flask import Blueprint, redirect, request, render_template, jsonify, flash, abort, session
from web3.auto import w3
from eth_account.messages import encode_defunct
from web3 import Web3
from web3.middleware import geth_poa_middleware
import sqlalchemy
import time
from decouple import config

from apps.item.models import Item
from apps import db

item_bp = Blueprint('item', __name__, url_prefix='/item')


@item_bp.route('/', methods=['GET'])
def item_list():
    item = db.session.query(Item).order_by(Item.date_created.desc())
    return render_template('item/list.html', items=item)



@item_bp.route('/<int:item_id>', methods=['GET'])
def item_detail(item_id):
    item = db.session.query(Item).filter_by(id=item_id).first()
    return render_template('item/detail.html', item=item)    
    # if item:
    #     return render_template('item/detail.html', item=item)    
    # else:
    #     return render_template('404.html')   


