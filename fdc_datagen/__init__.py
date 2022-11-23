from flask import Flask
from flask_restful import Resource, Api, reqparse
from semtk3 import semtktable
import traceback
import json

from semtk3.resultset import ResultSet
from semtk3 import SemtkTable
    
        
class FdcGenerator(Resource):
   
    
    # Instructions:
    #    - override this class
    #    - set input_table_count and input_columns
    #    - override workers, and semtk_tables param will have correct number of tables with correct columns
    #    - main needs:
    #          api.add_resource(SubClassOfFdcGenerator, '/sample/fdc_endpoint_name') 
    #    - return a semtkTable
    input_table_count = 1
    input_columns = { '1': ["column1","column2"] }
    
    '''
    @param semtk_table_dict where semtk_table_dict[step_seq_num] = semtkTable
    '''
    def worker(self, semtk_table_dict):
        cls = self.__class__
        table = semtk_table_dict[1]
        
        # PEC TODO : I think this is returning a csv instead of a table
        res_tab = SemtkTable(
            SemtkTable.create_table_dict(
                ["out_col1", "out_col2"],
                ["string", "string"],
                [["one", "two"], ["oneA", "twoA"]]
                )
            )
                
        return res_tab
                                        
    def post(self):
        cls = self.__class__
        try:
            parser = reqparse.RequestParser()  # initialize
            
            parser.add_argument('tables', required=True)
            args = parser.parse_args()  
            
            # confirm we got the right number of tables
            input_tables = json.loads(args['tables']);
            dict_keys = input_tables.keys()
            if (len(dict_keys) != cls.input_table_count):
                raise Exception("Wrong number of tables sent to FDC generator.  Expected: " + cls.input_table_count + " found: " + len(dict_keys))
            
            semtk_tables = {}
            for seq_num in input_tables.keys():
                semtk_tables[seq_num] = SemtkTable(input_tables[seq_num])
            
            for seq_num in cls.input_columns.keys():
                # confirm table columns
                actual_col_names = semtk_tables[seq_num].get_column_names()
                for c in cls.input_columns[seq_num]:
                    if (not c in actual_col_names):
                        raise Exception("Input table " + str(seq_num) + " is missing column '" + c + "', found: " + ','.join(actual_col_names))
            # do work
            res_tab = self.worker(semtk_tables)
            
            # return
            res = ResultSet()
            res.set_status(True)
            res.set_table(res_tab);
            
            return res.to_dict(), 200  # return data with 200 OK
        
        except Exception as e:
            res = ResultSet()
            res.set_status(False)
            res.set_rationale(str(e))
            traceback.print_exc()
            return res.to_dict(), 200  # return data with 200 OK



#
# This endpoint provides nodegroups from the resources folder
# 
# api.add_resource(NodegroupProvider, '/YOUR_PATH/getNodegroup')
#
class NodegroupProvider(Resource):     
    def post(self):
        
        try:
            parser = reqparse.RequestParser()  # initialize
            
            parser.add_argument('id', required=True)
            args = parser.parse_args()  
            
            nodegroup_id = args['id'];
            
            # do work
            data = ""
            filename = "resources/" + nodegroup_id + ".json"
            with open (filename, "r") as myfile:
                data=myfile.read()
            
            if len(data.strip()) == 0:
                raise Exception("File is empty: " + filename)
            
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

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    
    api.add_resource(NodegroupProvider, '/sample/getNodegroup')
    api.add_resource(FdcGenerator, '/sample/generator')

    app.run(host='0.0.0.0', port=12999, debug=True) 