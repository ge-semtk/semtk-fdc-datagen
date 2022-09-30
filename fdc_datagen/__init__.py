from flask import Flask
from flask_restful import Resource, Api, reqparse
from semtk3 import semtktable
import traceback
import json
from fdc_datagen import nodegroup_provider
from fdc_datagen import fdc_generator


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    
    api.add_resource(nodegroup_provider.NodegroupProvider, '/sample/getNodegroup')
    api.add_resource(fdc_generator.FdcGenerator, '/sample/generator')

    app.run(host='0.0.0.0', port=12999, debug=True) 