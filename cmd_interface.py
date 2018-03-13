# Imports
import argparse
import logging, logging.config
import inspect
import yaml
import io
import os
import sys
import socket
import platform


# Load base logging information
PACKAGE_PATH = os.path.split(os.path.realpath(__file__))[0]

loggerconfig_stream = open(PACKAGE_PATH + "/logger.ini", "r")
log_config = yaml.safe_load(loggerconfig_stream)
logging.config.dictConfig(log_config)

logger = logging.getLogger(__name__)
logging.Formatter.default_msec_format = '%s.%03d'


class CmdInterface:

    def parse_args(self, args):

        parsed_args = self.arg_parser.parse_args(args)

        return parsed_args

    def load_script_settings(self, settings_path):

        with io.open(settings_path, "r") as settings_yml:
            try:
                settings_dict = yaml.safe_load(settings_yml)
                logger.debug("Loaded command interface settings")
            except:
                logger.error("Command interface settings failed to load from file: " + settings_path)

        return settings_dict

    def create_arg_parser(self):

        logger.debug("Creating argument parser")
        parser = argparse.ArgumentParser(prog=self.settings.get("prog"),
                                         description=self.settings.get("description"),
                                         epilog=self.settings.get("epilog"))

        argument_settings_list = self.settings.get("arguments")

        for argument in argument_settings_list:
            parser.add_argument(argument.get("name"), dest=argument.get("dest"), nargs=argument.get("nargs"))

        return parser

    def run(self, args):

        parsed_args = self.parse_args(args)
        parsed_args_dict = vars(parsed_args)

        self.output_function_header()

        self.func(**parsed_args_dict)

        pass

    def __init__(self, func, settings_path):

        logger.debug("Initializing command line interface class")
        self.func = func
        self.settings = self.load_script_settings(settings_path)

        self.arg_parser = self.create_arg_parser()
        pass

    def output_function_header(self):

        host = socket.gethostname()
        py_version = platform.python_version()
        plat = platform.platform(aliased=0, terse=0)

        logger.info("**************************************************")
        logger.info(self.settings.get("glyph_l1") + "\t\t" + self.settings.get("project"))
        logger.info(self.settings.get("glyph_l2") + "\t\t" + self.settings.get("prog"))
        logger.info(self.settings.get("glyph_l3") + "\t\t" + "v " + self.settings.get("version"))
        logger.info(self.settings.get("glyph_l4"))
        logger.info("**************************************************")
        logger.info("[host: " + host + ", version: Python " + py_version + "]")
        logger.info("[platform: " + str(plat) + "]")

        pass