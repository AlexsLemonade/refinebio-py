import click
import json

@click.group()
def cli():
    pass


class DictParamType(click.ParamType):
    name = "dict"

    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except:
            self.fail(
                "expected valid string in a dict form, "
                "got: {0}".format(value),
                param,
                ctx
            )


class ListParamType(click.ParamType):
    name = "list"

    def convert(self, value, param, ctx):
        try:
            return value.split()
        except:
            self.fail(
                "expected valid string in list form, "
                "got: {0}".format(value),
                param,
                ctx
            )

