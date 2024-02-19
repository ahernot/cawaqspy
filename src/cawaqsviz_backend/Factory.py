
import json
from abc import ABCMeta, abstractmethod

class FactoryClass(metaclass=ABCMeta):

    @classmethod
    def fromDict(cls, a_dict):
        """
            instantiates from a dictionary, no validity tests here
        """
        return cls(a_dict)

    @classmethod
    def fromJsonString(cls, a_json_string):
        """
            instantiates from a json string, no validity tests here
        """
        try:
            a_dict = json.loads(a_json_string)
        except ValueError:
            # not a valid json string
            print('not a valid JSON string', flush=True)
            return None
        return cls(a_dict)

    @classmethod
    def fromJsonFile(cls, a_filename):
        """
            instantiates from a json file

            exceptions:
            - file not found
            - value error

        """
        try:
            with open(a_filename) as json_file:
                a_dict = json.load(json_file)

            # int(keys and values) in dict load from a jsonfile 
            for key, value in a_dict.items():
                if isinstance(a_dict[key], dict):
                    try :
                        a_dict[key] = {int(subkey): int(subvalue) \
                            if isinstance(subvalue, str) else subvalue \
                                for subkey, subvalue in a_dict[key].items()}
                    except : 
                        pass

                if isinstance(a_dict[key], dict):
                    try :
                        a_dict[key] = {int(subkey): subvalue \
                            if isinstance(subvalue, str) else subvalue \
                                for subkey, subvalue in a_dict[key].items()}
                    except : 
                        pass

        except FileNotFoundError as e:
            print(e)
            raise(e)
        except ValueError as e:
            # not a valid json string
            print(e)
            raise(e)
        return cls(a_dict)
    

    @classmethod
    def fromUnformattedDict(cls, a_dict):
        """
            instantiates from a json file

            exceptions:
            - file not found
            - value error

        """
        try:
            for key, value in a_dict.items():
                if isinstance(a_dict[key], dict):
                    try :
                        a_dict[key] = {int(subkey): int(subvalue) \
                            if isinstance(subvalue, str) else subvalue \
                                for subkey, subvalue in a_dict[key].items()}
                    except : 
                        pass

                if isinstance(a_dict[key], dict):
                    try :
                        a_dict[key] = {int(subkey): subvalue \
                            if isinstance(subvalue, str) else subvalue \
                                for subkey, subvalue in a_dict[key].items()}
                    except : 
                        pass

        except ValueError as e:
            # not a valid json string
            print(e)
            raise(e)
        return cls(a_dict)

    @abstractmethod
    def __init__(self, a_dict):
        return