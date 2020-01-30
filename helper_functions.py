'''
*********description*********

'''

import json

def load_JSON_key(json_str, key):
    try:
            py_dict = json.loads(json_str)
            result = py_dict[key]
    except TypeError as e:
            print "\n\t[***except***]-----Need a JSON string object-----:  %s" % e
    except ValueError as e:
            print "\n\t[***except***]-----Missing VALUE in some JSON key-value pairs-----:  %s" % e
    except KeyError as e:
            print "\n\t[***except***]-----Specified KEY doesn't exist-----:  %s" % e
    else:
            print "\n\t[***else***]-----Load JSON object successful, return VALUE associated with KEY-----"
            return result
    finally:
            print "\n\t[***finally***]-----I'll always display in ANY circumstances ^_^"
            
