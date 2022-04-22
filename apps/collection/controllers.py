# Import flask dependencies
from flask import Blueprint, redirect, request, render_template, jsonify, flash, abort, session
from web3.auto import w3
from eth_account.messages import encode_defunct
from web3 import Web3
from web3.middleware import geth_poa_middleware
import sqlalchemy
import time
from decouple import config

from apps.collection.models import Collection
from apps import db

collection_bp = Blueprint('collection', __name__, url_prefix='/collections')


@collection_bp.route('/', methods=['GET'])
def collection_list():
    collections = db.session.query(Collection).order_by(Collection.date_created.desc())
    return render_template('collection/list.html', collections=collections)



@collection_bp.route('/<collection_address>', methods=['GET'])
def collection_detail(collection_address):
    collection = db.session.query(Collection).filter_by(contract_address=collection_address).first()
    if collection:
        return render_template('collection/detail.html', collection=collection)    
    else:
        return render_template('404.html')   


@collection_bp.route('/<collection_address>/<int:token_id>', methods=['GET'])
def token_detail(collection_address, token_id):
    collection = db.session.query(Collection).filter_by(contract_address=collection_address).first()
    if collection:
        return render_template('collection/token_detail.html', collection=collection, token_id=token_id)    
    else:
        return render_template('404.html')           

