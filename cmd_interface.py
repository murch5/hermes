# Imports

import logging, logging.config

import argparse

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

logging.disable(logging.INFO)



class CmdInterface:

    def parse_args(self, args):

        parsed_args = self.arg_parser.parse_args(args)

        return parsed_args

    def load_script_settings(self, settings_path):

        with io.open(settings_path, "r") as settings_yml:
            try:
                settings_dict = yaml.safe_load(settings_yml)
            except:
                logger.error("Command interface settings failed to load from file: " + settings_path)

        return settings_dict

    def create_arg_parser(self):


        parser = argparse.ArgumentParser(prog=self.settings.get("prog"),
                                         description=self.settings.get("description"),
                                         epilog=self.settings.get("epilog"),
                                         allow_abbrev=False)

        argument_settings_list = self.settings.get("arguments")

        self.add_args(parser, argument_settings_list)

        return parser

    def add_args(self, parser, arg_list):

        for argument in arg_list:
            args = argument.get("name")
            kwargs = argument
            del kwargs["name"]

            if isinstance(args, list):
                parser.add_argument(*args, **kwargs)
            else:
                parser.add_argument(args, **kwargs)

        return parser

    def run(self, args):

        parsed_args = self.parse_args(args)
        self.parsed_args_dict = vars(parsed_args)

        self.process_common_args(**self.parsed_args_dict)

        if self.show_header:
            self.output_function_header()

        self.func(**self.parsed_args_dict)

        pass

    def __init__(self, func, settings_path):

        self.func = func
        self.settings = self.load_script_settings(settings_path)

        self.arg_parser = self.create_arg_parser()
        self.parsed_args_dict = {}
        self.show_header = True

        self.add_common_cmd_args()

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
        logger.info("[args: " + str(self.parsed_args_dict) + "]")

        pass

    def add_common_cmd_args(self):

        common_args = self.load_script_settings(os.path.split(__file__)[0] + "/settings.yml")

        self.add_args(self.arg_parser, common_args.get("arguments"))

        pass

    def process_common_args(self, **kwargs):

        silent_flag = kwargs.get("silent_flag")

        if silent_flag:
            logging.disable(logging.CRITICAL)
            self.show_header = False
        else:
            logging.disable(logging.NOTSET)

        if kwargs.get("hide_header"):
            self.show_header = False


        pass