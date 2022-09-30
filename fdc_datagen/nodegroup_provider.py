from flask_restful import Resource, reqparse
import traceback
import json
from semtk3.resultset import ResultSet

#
# This endpoint provides nodegroups from the resources folder
# 
# api.add_resource(NodegroupProvider, '/YOUR_PATH/getNodegroup')
#
class NodegroupProvider(Resource):     
    def post(self):
        
        try:
            parser = reqparse.RequestParser()  # initialize
            
            parser.add_argument('arg_id', required=True)
            args = parser.parse_args()  
            
            arg_id = args['arg_id'];
            
            # do work
            data = ""
            with open ("resources/" + arg_id + ".json", "r") as myfile:
                data=myfile.read()
            
            # return
            res = ResultSet()
            res.set_status(True)
            res.set_json_field("sgjson", json.loads(data));
            
            return res.to_dict(), 200  # return data with 200 OK
        
        except Exception as e:
            res = ResultSet()
            res.set_status(False)
            res.set_rationale(str(e))
            traceback.print_exc()
            return res.to_dict(), 200  # return data with 200 OK
  
