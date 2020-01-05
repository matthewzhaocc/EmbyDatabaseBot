import json

class Config:
    required_fields = ["database_uri", "token"]
    fields = ["database_uri", "token", "log_channel"]

    database_uri: str
    bot_token: str
    log_channel: str

    def __init__(self, database_uri: str, token: str, log_channel: str = None):
        self.database_uri = database_uri
        self.token = token
        self.log_channel = log_channel

    @staticmethod
    def from_file(filename: str) -> "Config":
        try:
            with open(filename, "r") as f:
                config = json.load(f)
        except IOError as e:
            # If all the required fields are specified as environment variables, it's OK to 
            # not raise the IOError, we can just construct the dict from these
            if all([rf.upper() in os.environ for rf in Config.required_fields]):
                config = {}
            else:
                # If they aren't, though, then rethrow
                raise e

        # If we currently don't have all the required fields, then raise
        if not all([rf in config for rf in Config.required_fields]):
            raise RuntimeError("Some config fields were missing! Please check your config file.")

        return Config(**config)
