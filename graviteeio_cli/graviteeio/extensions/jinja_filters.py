import yaml

def to_yaml(a, *args, **kw):
    # transformed = yaml.dump(a, allow_unicode=True, default_flow_style=True, **kw)
    return yaml.safe_dump(a, default_flow_style=True).rstrip()


def filter_loader(environment):
    environment.filters['toyaml'] = to_yaml