
default_value_file_yaml = \
 'version: "1.0"\n' + \
 'name: My first api\n' +\
 'description: api generated with gio cli\n' +\
 'context_path: /test\n' +\
 'endpoints:\n' +\
 '   - https://api.gravitee.io/echo\n' +\
 'plans:\n' +\
 '   - name: Plan keyless\n' +\
 '     description: plan keyless\n' +\
 '     security: key_less'

default_value_file_json = \
 '{\n' + \
 '  "version": "1.0",\n' + \
 '  "name": "My first api",\n' + \
 '  "description": "api generated with gio cli",\n' + \
 '  "context_path": "/test",\n' + \
 '  "endpoints": [\n' + \
 '    "https://api.gravitee.io/echo"\n' + \
 '  ],\n' + \
 '  "plans": [\n' + \
 '    {\n' + \
 '      "name": "Plan keyless",\n' + \
 '      "description": "plan keyless",\n' + \
 '      "security": "key_less"\n' + \
 '    }\n' + \
 '  ]\n' + \
 '}'

default_setting_http_yaml = \
 'connectTimeout: 5000\n' +\
 'idleTimeout: 60000\n' +\
 'keepAlive: true\n' +\
 'readTimeout: 10000\n' +\
 'pipelining: false\n' +\
 'maxConcurrentConnections: 100\n' +\
 'useCompression: true\n' +\
 'followRedirects: false\n' +\
 'encodeURI: false'

default_setting_http_json = \
 '{\n' +\
 '  "connectTimeout": 5000,\n' +\
 '  "idleTimeout": 60000,\n' +\
 '  "keepAlive": true,\n' +\
 '  "readTimeout": 10000,\n' +\
 '  "pipelining": false,\n' +\
 '  "maxConcurrentConnections": 100,\n' +\
 '  "useCompression": true,\n' +\
 '  "followRedirects": false,\n' +\
 '  "encodeURI": false\n' +\
 '}'

default_template_yaml = \
 'version: {{ Values.version}}\n' +\
 'name: {{ Values.name}}\n' +\
 'description: {{ Values.description}}\n' +\
 'visibility: private\n' +\
 'proxy:\n' +\
 '  strip_context_path: false\n' +\
 '  preserve_host: false\n' +\
 '  virtual_hosts:\n' +\
 '    - path: {{ Values.context_path}}\n' +\
 '  groups:\n' +\
 '    - name: default-group\n' +\
 '      endpoints:\n' +\
 '      {%- for endpoint in Values.endpoints %}\n' +\
 '        - name: default-{{ loop.index }}\n' +\
 '          target: {{ endpoint}}\n' +\
 '          weight: 1\n' +\
 '          backup: false\n' +\
 '          type: HTTP\n' +\
 '          inherit: true\n' +\
 '      {% endfor -%}\n' +\
 '      load_balancing:\n' +\
 '        type: round_robin\n' +\
 '      http: {{ Http | toyaml}}\n' +\
 'paths:\n' +\
 '  "/": []\n' +\
 'resources: []\n' +\
 'path_mappings: []\n' +\
 'response_templates: {}\n' +\
 'plans:\n' +\
 '{%- for plan in Values.plans %}\n' +\
 '  - name: {{ plan.name}}\n' +\
 '    description: {{ plan.description}}\n' +\
 '    validation: {{ plan.validation | default("auto")}}\n' +\
 '    security: {{ plan.security}}\n' +\
 '    type: api\n' +\
 '    status: {{ plan.status | default("published")}}\n' +\
 '    order: {{loop.index - 1}}\n' +\
 '    paths:\n' +\
 '      "/": []\n' +\
 '    comment_required: False\n' +\
 '    characteristics: []\n' +\
 '{% endfor -%}'

default_template_json = \
 '{\n' +\
 '    "version": "{{ Values.version}}",\n' +\
 '    "name": "{{ Values.name}}",\n' +\
 '    "description": "{{ Values.description}}",\n' +\
 '    "visibility": "private",\n' +\
 '    "proxy": {\n' +\
 '        "strip_context_path": false,\n' +\
 '        "preserve_host": false,\n' +\
 '        "virtual_hosts": [{\n' +\
 '            "path": "{{ Values.context_path}}"\n' +\
 '        }],\n' +\
 '        "groups": [\n' +\
 '            {\n' +\
 '                "name": "default-group",\n' +\
 '                "endpoints": [\n' +\
 '                {%- for endpoint in Values.endpoints %}\n' +\
 '                    {\n' +\
 '                        "name": "default-{{ loop.index }}",\n' +\
 '                        "target": "{{ endpoint}}",\n' +\
 '                        "weight": 1,\n' +\
 '                        "backup": false,\n' +\
 '                        "type": "HTTP",\n' +\
 '                        "inherit": true\n' +\
 '                    }{%- if not loop.last -%},{%- endif -%}\n' +\
 '                {% endfor -%}\n' +\
 '                ],\n' +\
 '                "load_balancing": {"type": "round_robin"},\n' +\
 '                "http": {{ Http | tojson}}\n' +\
 '            }\n' +\
 '        ]\n' +\
 '    },\n' +\
 '    "paths": {"/": []},\n' +\
 '    "resources": [],\n' +\
 '    "path_mappings": [],\n' +\
 '    "response_templates": {},\n' +\
 '    "plans": [\n' +\
 '    {%- for plan in Values.plans %}\n' +\
 '        {\n' +\
 '            "name": "{{ plan.name}}",\n' +\
 '            "description": "{{ plan.description}}",\n' +\
 '            "validation": "{{ plan.validation | default("auto")}}",\n' +\
 '            "security": "{{ plan.security}}",\n' +\
 '            "type": "api",\n' +\
 '            "status": "{{ plan.status | default("published")}}",\n' +\
 '            "order": {{loop.index - 1}},\n' +\
 '            "paths": {"/": []},\n' +\
 '            "comment_required": false,\n' +\
 '            "characteristics": []\n' +\
 '        }{%- if not loop.last -%},{%- endif -%}\n' +\
 '    {% endfor -%}\n' +\
 '    ]\n' +\
 '}'

templates = {
    "json": {
        "value_file": default_value_file_json,
        "setting_http": default_setting_http_json,
        "template": default_template_json
    },
    "yaml": {
        "value_file": default_value_file_yaml,
        "setting_http": default_setting_http_yaml,
        "template": default_template_yaml
    }
}
