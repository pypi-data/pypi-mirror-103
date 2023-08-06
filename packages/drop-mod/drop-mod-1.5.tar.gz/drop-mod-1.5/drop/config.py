import json
import os

from drop.errors import ConfigParameterNotFound, ConfigNotFound

bot_config = {}


def load_config(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8", newline="\n") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise ConfigNotFound(f"Config file {filepath} doesn't exist.")
    global bot_config
    global config_filepath
    bot_config = config
    config_filepath = filepath


config_filepath = "data/config.json"
try:
    load_config("data/config.json")
except ConfigNotFound:
    bot_config = {}
    if not os.path.isdir("data/"):
        os.mkdir("data/")
    json.dump(bot_config, open(config_filepath, "w+", encoding="utf-8", newline="\n"), indent=2)


def save_config(new_config=None):
    if new_config is None:
        new_config = bot_config
    json.dump(new_config, open(config_filepath, "w+", encoding="utf-8", newline="\n"), indent=2)


def get_config_parameter(parameter, parameter_type=None):
    config_param = bot_config.get(parameter)
    if config_param is None:
        raise ConfigParameterNotFound(f"Config file doesn't have key {parameter}")
    if not parameter_type:
        parameter_type = type(config_param)
    return parameter_type(config_param)


def get_config():
    return bot_config


def write_config_parameter(parameter, new_value, parameter_type=None):
    if not parameter_type:
        parameter_type = type(new_value)
    bot_config[parameter] = parameter_type(new_value)
    save_config()
    return

# server config time
# ----------------------------------------------------------------------------------------------------------------------


def get_server_config(guild_id, parameter, parameter_type=None):
    try:
        config_parameter = get_entire_server_config(guild_id).get(parameter)
        if not config_parameter:
            raise ConfigParameterNotFound(f"Config file for guild {guild_id} doesn't have key {parameter}")
        if not parameter_type:
            parameter_type = type(config_parameter)
        return parameter_type(config_parameter)
    except FileNotFoundError:
        # No config exists for this server.
        raise ConfigNotFound(f"Config file not found for guild {guild_id}")


def get_entire_server_config(guild_id):
    try:
        with open(f"data/servers/{guild_id}/config.json", "r", encoding="utf-8", newline="\n") as file:
            server_config = json.load(file)
            return server_config
    except FileNotFoundError:
        touch_server_config(guild_id)
        return {}


def touch_server_config(guild_id):
    if not os.path.exists('data/'):
        os.mkdir('data/')
    if not os.path.exists('data/servers/'):
        os.mkdir('data/servers/')
    if not os.path.exists(f'data/servers/{guild_id}/'):
        os.mkdir(f'data/servers/{guild_id}/')
    json.dump({}, open(f'data/servers/{guild_id}/', 'w+'))
    return


def write_server_config(guild_id, param, value):
    filepath = f"data/servers/{guild_id}/config.json"
    server_config = get_entire_server_config(guild_id)
    server_config[param] = value
    json.dump(server_config, open(filepath, 'w+', encoding="utf-8", newline='\n'))
    return


def write_entire_server_config(guild_id, config: dict):
    filepath = f"data/servers/{guild_id}/config.json"
    json.dump(config, open(filepath, 'w+', encoding="utf-8", newline='\n'))
    return
