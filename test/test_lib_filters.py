from jinja2 import Environment
from graviteeio_cli.graviteeio.extensions.jinja_filters import filter_loader

def test_to_yaml():
    env = Environment(autoescape=True)
    filter_loader(env)

    t = env.from_string("{{ x|toyaml }}")
    assert t.render(x={"foo": "bar"}) == '{foo: bar}'