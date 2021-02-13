default_value_file_yaml = \
 'name_app: My first app'

default_value_file_json = \
 '{\n' + \
 '  "name_app": "My first app",\n' + \
 '}'

default_template_yaml = \
 'name: {{ Values.name_app}}\n' +\
 'description: my first app\n' +\
 'settings:\n' +\
 '  app: {}\n'

default_template_json = \
 '{\n' +\
 '    "name": "{{ Values.name_app}}",\n' +\
 '    "description": "my first app",\n' +\
 '    "settings": {\n' +\
 '       "app": {}\n' +\
 '     }\n' +\
 '}'
