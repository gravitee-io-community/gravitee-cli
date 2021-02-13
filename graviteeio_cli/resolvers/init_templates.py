from . import init_templates_api as tpl_api
from . import init_templates_app as tpl_app

templates_api = {
    "json": {
        "value_file": tpl_api.default_value_file_json,
        "template": tpl_api.default_template_json,
        "setting_files": {
            "Http{}": tpl_api.default_setting_http_json
        }
    },
    "yaml": {
        "value_file": tpl_api.default_value_file_yaml,
        "template": tpl_api.default_template_yaml,
        "setting_files": {
            "Http{}": tpl_api.default_setting_http_yaml
        }
    }
}

templates_app = {
    "json": {
        "value_file": tpl_app.default_value_file_json,
        "template": tpl_app.default_template_json,
        "setting_files": {}
    },
    "yaml": {
        "value_file": tpl_app.default_value_file_yaml,
        "template": tpl_app.default_template_yaml,
        "setting_files": {}
    }
}
