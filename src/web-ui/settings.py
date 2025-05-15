from strictyaml import load, Map, Str, Int
import os

# Load application settings according to schema

# Schema for Subscribie application settings
# See also https://hitchdev.com/strictyaml/
schema = Map(
    {
        "IDRAC_HOST": Str(),
        "IDRAC_USERNAME": Str(),
        "IDRAC_PASSWORD": Str(),
        "HOST_HEALTHCHECK_POLL_IP": Str(),
        "DEFAULT_HTTP_REQ_TIMEOUT": Int(),
        "IDRAC_SLEEP_AFTER_RESET_REQUEST_REQ": Int(),
        "PSONO_CI_API_KEY_ID": Str(),
        "PSONO_CI_API_SECRET_KEY_HEX": Str(),
        "PSONO_CI_SERVER_URL": Str(),
        "PSONO_CI_VPN_SECRET_NOTE_ID": Str(),
    }
)


def load_settings():
    with open("settings.yaml") as fp:
        settings_string = fp.read()
        settings = load(settings_string, schema)
        for key in schema._required_keys:
            if key in os.environ:
                print(
                    f"Overriding setting {key} with environ value: {os.getenv(key)}"  # noqa: E501
                )
                settings[key] = os.getenv(key)
        return settings


# Load app setttings via strictyaml & schema
settings = load_settings().data
