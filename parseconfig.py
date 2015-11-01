import configparser
import webwatch

def unsafe_dict_to_resource(name, dict):
  cls = getattr(webwatch, dict.pop('class', 'Resource'))
  kwargs = {key: eval(value) for key, value in dict.items()}
  return cls(name=name, **kwargs)

def unsafe_parse_config(filename):
  cp = configparser.ConfigParser()
  cp.read(filename)
  return [unsafe_dict_to_resource(name, cp[name]) for name in cp.sections()]
