import os

from dotenv import load_dotenv
load_dotenv()


class InvalidTasklistNameException(Exception):
    pass

class Settings(dict):
    def __getattribute__(self, key):
        return self[key]


class Setting:
    def __init__(self, name, constructor, default=None, optional=False, mutator=None):
        self.name = name
        self.constructor = constructor
        self.default = default
        self.optional = optional
        self.mutator = mutator

    def get_from_env(self):
        if not self.optional and self.default is None:
            value = os.environ[self.name]
        else:
            value = os.environ.get(self.name, self.default)

        if value is None:
            return value
        else:
            return self.mutate(self.constructor(value))

    def mutate(self, constructed_value):
        if self.mutator is None:
            return constructed_value
        else:
            return self.mutator(constructed_value)


__setting_manifest = [
    Setting("SLACK_WEBHOOK", str),
    #Setting("REDIS_PORT", int, default=6379),
]


SETTINGS = Settings({
    setting.name: setting.get_from_env()
    for setting in __setting_manifest
})
