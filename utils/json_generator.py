import random
import string
import uuid
import copy
from datetime import datetime
from random import randint

class JSONGenerator(object):

    def set_seed(self, seed = 0):
        random.seed(seed)

    def generate_random_range(self, list):
        val = randrange(0,len(list))
        if val == 0:
            val = len(list)
        return list[0:val]

    def random_alphanumeric(self, limit = 10):
        #ascii alphabet of all alphanumerals
        r = (range(48, 58) + range(65, 91) + range(97, 123))
        random.shuffle(r)
        return reduce(lambda i, s: i + chr(s), r[:random.randint(0, len(r))], "")

    def random_uuid(self):
        return str(uuid.uuid4()).replace("-","")

    def random_char(self):
        return random.choice(string.ascii_uppercase)

    def random_tiny_int(self):
        return randint(0,1)

    def random_int(self, max_int = 10000):
        return randint(0, max_int)

    def random_float(self):
        return round(10000*random.random(),0)

    def random_double(self):
        return round(10000*random.random(),0)

    def random_boolean(self):
        return random.choice([True, False])

    def random_datetime(self, start = 1999, end = 2015):
        year = random.choice(range(start, end))
        month = random.choice(range(1, 13))
        day = random.choice(range(1, 29))
        return datetime(year, month, day)

    def random_alphabet_string(self, limit =10):
        uppercase = sorted(string.ascii_uppercase)
        lowercase = sorted(string.ascii_lowercase)
        value = []
        for x in range(0,limit/2):
            value.append(random.choice(uppercase))
            value.append(random.choice(lowercase))
        random.shuffle(value)
        return "".join(value)

    def random_array(self, max_dimension_size = 2, max_array_size = 10):
        dimension_size = randint(1, max_dimension_size)
        array_size = randint(1, max_array_size)
        return self.random_multi_dimension_array(level = dimension_size, max_array_size = array_size)

    def random_multi_dimension_array(self, level = 2, max_array_size = 10):
        if level == 1:
            array_size = randint(0, max_array_size)
            array = []
            for x in range(0,array_size):
                k, d = self.gen_data_no_json()
                array.append(d )
            return array
        else:
        	array_size = randint(1, max_array_size)
        	array = []
        	for x in range(array_size):
        		array_element = self.random_multi_dimension_array(level = level-1, max_array_size = max_array_size)
        		array.append(array_element)
        	return array

    def random_single_dimension_array(self, max_array_size = 1):
        array_size = randint(0, max_array_size)
        array = []
        for x in range(array_size):
            array.append(self.random_int())
        return array

    def gen_data(self):
    	function_list = ["random_int", "random_float", "random_alphanumeric", "random_float","random_boolean", "random_multi_dimension_array", "random_char", "random_json"]
    	function_name = random.choice(function_list)
        return (self.random_uuid() + "_" + function_name), getattr(self, function_name)()

    def gen_data_no_json(self):
        function_list = ["random_int", "random_float", "random_alphanumeric", "random_float",]
        function_name = random.choice(function_list)
        return (self.random_uuid() + "_" + function_name), getattr(self, function_name)()

    def nested_random_json(self, random_fields = False, random_array_count = 4, nested_level = 1, source_json=None):
        if source_json is None:
            source_json=self.random_json(random_fields=random_fields, random_array_count=random_array_count)
        json_ptr=copy.deepcopy(source_json)
        base_json=json_ptr
        for index in range(nested_level):
            json_ptr["level_{0}".format(index)]=copy.deepcopy(source_json)
            json_ptr=json_ptr["level_{0}".format(index)]
        return base_json

    def random_json(self, random_fields = False, random_array_count = 4):
    	json_body = {}
    	function_list = ["random_int", "random_float", "random_alphanumeric", "random_float","random_boolean", "random_multi_dimension_array", "random_char"]
        for function in function_list:
            if random_fields and self.isChoice():
                json_body[(self.random_uuid() + "_" + function.replace("random_", ""))] = getattr(self, function)()
            else:
                if function == "random_multi_dimension_array":
                    for x in range(random_array_count):
                        json_body[(self.random_uuid() + "_" + function.replace("random_", ""))] = getattr(self, function)()
                else:
                    json_body[(self.random_uuid() + "_" + function.replace("random_", ""))] = getattr(self, function)()
        return json_body

    def gen_json_from_template(self, source={}):
        if isinstance(source, dict):
            new_json={}
            for key, val in source.iteritems():
                new_json[key] = self.gen_json_from_template(val)
            return new_json
        elif isinstance(source, list):
            new_list=[]
            for index in range(len(source)):
                new_list.append(self.gen_json_from_template(source[index]))
            return new_list
        elif isinstance(source, int):
            return self.random_int()
        elif isinstance(source, str):
            return self.random_alphanumeric()
        elif isinstance(source, float):
            return self.random_float()
        elif source is None:
            return None

    def isChoice(self):
        return random.choice([True, False])