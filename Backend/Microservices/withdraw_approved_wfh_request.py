from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)

employee_URL = "http://127.0.0.1:5000/userAccounts/hp_num/"
bank_accounts_URL = "http://127.0.0.1:5001/bankAccounts/transferral/"
transaction_history_URL = "http://127.0.0.1:5002/transaction_history"