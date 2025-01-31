import os
import glob
import importlib, importlib.util
import logging

default_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "default")
loaded = {}


def dummy_callback():
    pass


def on(event_name, *args, **kwargs):
    global loaded
    cb_name = 'on_%s' % event_name
    for plugin_name, plugin in loaded.items():
        if cb_name in plugin.__dict__:
            try:
                plugin.__dict__[cb_name](*args, **kwargs)
            except Exception as e:
                logging.error("error while running %s.%s : %s" % (plugin_name, cb_name, e))
                logging.error(e, exc_info=True)


def one(plugin_name, event_name, *args, **kwargs):
    global loaded
    if plugin_name in loaded:
        plugin = loaded[plugin_name]
        cb_name = 'on_%s' % event_name
        if cb_name in plugin.__dict__:
            try:
                plugin.__dict__[cb_name](*args, **kwargs)
            except Exception as e:
                logging.error("error while running %s.%s : %s" % (plugin_name, cb_name, e))
                logging.error(e, exc_info=True)


def load_from_file(filename):
    plugin_name = os.path.basename(filename.replace(".py", ""))
    spec = importlib.util.spec_from_file_location(plugin_name, filename)
    instance = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(instance)
    return plugin_name, instance


def load_from_path(path, enabled=()):
    global loaded
    for filename in glob.glob(os.path.join(path, "*.py")):
        try:
            name, plugin = load_from_file(filename)
            if name in loaded:
                raise Exception("plugin %s already loaded from %s" % (name, plugin.__file__))
            elif name not in enabled:
                # print("plugin %s is not enabled" % name)
                pass
            else:
                loaded[name] = plugin
        except Exception as e:
            logging.warning("error while loading %s: %s" % (filename, e))
            logging.debug(e, exc_info=True)

    return loaded


def load(config):
    enabled = [name for name, options in config['main']['plugins'].items() if
               'enabled' in options and options['enabled']]
    custom_path = config['main']['custom_plugins'] if 'custom_plugins' in config['main'] else None
    # load default plugins
    loaded = load_from_path(default_path, enabled=enabled)
    # set the options
    for name, plugin in loaded.items():
        plugin.__dict__['OPTIONS'] = config['main']['plugins'][name]
    # load custom ones
    if custom_path is not None:
        loaded = load_from_path(custom_path, enabled=enabled)
        # set the options
        for name, plugin in loaded.items():
            plugin.__dict__['OPTIONS'] = config['main']['plugins'][name]

    on('loaded')
