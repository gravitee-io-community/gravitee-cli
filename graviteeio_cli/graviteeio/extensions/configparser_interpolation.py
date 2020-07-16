import os
from configparser import Interpolation, BasicInterpolation
from graviteeio_cli import environments

class GioInterpolation(BasicInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        newvalue = self._get_env_value(value)
        return super().before_get(parser, section, option, newvalue, defaults)

    def before_set(self, parser, section, option, value):
        return super().before_set(parser, section, option, value)
    

    def _get_env_value(self, value):
        to_return = value
        if value.startswith("env:"):
            to_return = os.environ.get(value[4:])
            # if not to_return:
            #     raise GraviteeioError('No environement value found for [{}].'.format(value[4:]))
            #     logger.error("No environement value found for [{}].".format(to_return))

        return to_return
        
