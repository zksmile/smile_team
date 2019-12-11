# coding=utf-8
import os

from flask import Flask


def create_app(test_config = None):
	#create and configure the app
	app = Flask(__name__,instance_relative_config = True)
	app.config.from_mapping(
		SECRET_KEY = '\x1b\xcbC?B\x84e\xb6rX?\xae4\xe0\x9f\xf0+\x87\xfe}k\xcf\x91\xb3'
		)