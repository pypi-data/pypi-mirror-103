from inspect import getmembers

import yaml
from robot.libraries.BuiltIn import BuiltIn
from robotframework_reportportal import listener, variables


class ReportPortalWrapper:

    __doc__ = """
    Report portal listener allow execution as 
    robot  --listener ReportPortalWrapper; \
                RP_UUID=<user token>; \
                RP_ENDPOINT:http://<your portal URI>:8080; \
                RP_LAUNCH:<Lunch name>; \
                RP_PROJECT:<Portal project name in lower case>; \
                ENV:TIRAMISU; \
                PLATFORM:CUSTOM_REMOTE_CHROME;
                x_api_version:1.4.0 
    """

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, **kwargs):
        self.ROBOT_LIBRARY_LISTENER = self
        yaml_file = kwargs.get('yaml', None)

        if yaml_file:
            with open(yaml_file, 'r') as yam:
                kwargs = yaml.load_all(yam)

        for var_name, var_value in kwargs.items():
            BuiltIn().set_global_variable(var_name, var_value)

        variables.Variables().check_variables()

        for (name, method) in getmembers(listener):
            if not name.startswith('_'):
                setattr(self, name, method)



