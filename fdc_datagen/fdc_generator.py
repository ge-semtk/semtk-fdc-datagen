
from flask_restful import Resource, reqparse
from semtk3 import SemtkTable
from semtk3.resultset import ResultSet
import json
import traceback
        
class FdcGenerator(Resource):
    # input table:  x x 
    #
    #    sorted by x
    #    where the 
    #
    # Output:     y y 
    #    
    #
    # api.add_resource(SubClassOfFdcGenerator, '/sample/fdc_endpoint_name') 

    def sample_worker(self, table):
        # confirm table columns
        col_names = table.get_column_names()
        for c in ["column1","column2"]:
            if (not c in col_names):
                raise Exception("Input table is missing column '" + c + "', found: " + ','.join(col_names))
        
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
        
        try:
            parser = reqparse.RequestParser()  # initialize
            
            parser.add_argument('tables', required=True)
            args = parser.parse_args()  
            
            # confirm we got the right number of tables
            input_tables = json.loads(args['tables']);
            dict_keys = input_tables.keys()
            if (not "1" in dict_keys or len(dict_keys) != 1):
                raise Exception("Expected tables to have key '1', found: " + ",".join(dict_keys))
            
            # get input table
            table1 = SemtkTable(input_tables['1'])
            
            # do work
            res_tab = self.sample_worker(table1)
            
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





    
    
    
 

        
