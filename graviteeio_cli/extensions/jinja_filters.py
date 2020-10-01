import yaml


def to_yaml(a, *args, **kw):
    return yaml.safe_dump(a, default_flow_style=True).rstrip()


def filter_loader(environment):
    environment.filters['toyaml'] = to_yaml
