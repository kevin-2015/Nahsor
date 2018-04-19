# -*- coding:utf-8 -*-
import pytest


def pytest_collect_file(parent, path):
    print(path)
    if path.ext == ".json" and path.basename.startswith("test"):
        return JsonFile(path, parent)

class JsonFile(pytest.File):
    def collect(self):
        import json
        raws = json.load(self.fspath.open())
        # print(raws)
        for raw in raws:
            for name, spec in sorted(raw.items()):
                yield JsonItem(name, self, spec)

class JsonItem(pytest.Item):
    def __init__(self, name, parent, spec):
        super(JsonItem, self).__init__(name, parent)
        self.spec = spec

    def runtest(self):
        for name, value in sorted(self.spec.items()):
            # some custom test execution (dumb example follows)
            # print(name, value)
            if name != value:
                raise JsonException(self, name, value)

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        if isinstance(excinfo.value, JsonException):
            return "\n".join([
                "usecase execution failed",
                "   spec failed: %r: %r" % excinfo.value.args[1:3],
                "   no further details known at this point."
            ])

    def reportinfo(self):
        return self.fspath, 0, "usecase: %s" % self.name

class JsonException(Exception):
    """ custom exception for error reporting. """