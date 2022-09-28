#!/usr/bin/env python3

#
#  Copyright (C) 2019-2020  XC Software (Shenzhen) Ltd.
#

import argparse
import logging
import os
import json
import sys
import time

_PY_ERROR_FILE_NAME = "error.py"
_EXTERNAL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "xcal-common")
_EXTERNAL_PY_PATH = os.path.join(_EXTERNAL_PATH, "py")
_PY_ERROR_FILE = os.path.join(_EXTERNAL_PY_PATH, _PY_ERROR_FILE_NAME)

# test case:
# not specify error message file param
# error message file has no read permission
# error message file is empty
# error message file is invalid
# error message file is ok
# output file is valid?


def get_parser():
    parser = argparse.ArgumentParser(description='read error message json file, generate python exception class file')
    parser.add_argument('--error-message-file', '-emf', dest='error_message_file',
                        metavar='errorMessage.json', required=True, help='error message file which contains.\
                         error name, error code, English/Chinese error messages.')
    parser.add_argument('--debug', '-d', dest='debug', action='store_true',
                        help='enable debug mode')
    return parser


def check_arguments(arguments: dict):
    logging.info("begin to check input")
    if not os.path.isfile(arguments.error_message_file):
        raise FileNotFoundError("File not found: %s" % arguments.error_message_file)
    if not os.access(arguments.error_message_file, os.R_OK):
        raise PermissionError("Cannot read file: %s" % arguments.error_message_file)
    if os.path.getsize(arguments.error_message_file) == 0:
        raise ValueError("File is empty: %s" % arguments.error_message_file)
    logging.info("input is ok")


def generate_exception_class_file(file_path: str):
    logging.info("begin to generate exception class file")
    with open(file_path) as json_file:
        error_message = json.load(json_file)
        error_keys = list(error_message.get("errors").keys())
        error_keys = list(filter(None, error_keys))     # filter empty key
    logging.debug(error_keys)

    with open(_PY_ERROR_FILE, "w") as error_file:
        # write base class
        error_file.write("class XcalError(Exception):\n")
        error_file.write("    \"\"\"Base class for exceptions in this module.\"\"\"\n")
        error_file.write("    pass\n\n\n")
        # write error code class
        for error in error_keys:
            norm_error = error.title().replace('_', '')
            error_file.write("class %s(XcalError):\n" % norm_error)
            error_file.write("    # %s\n" % error)
            error_file.write("    pass\n\n\n")
    logging.info("complete generate exception class file")
    return os.path.abspath(_PY_ERROR_FILE)


def main():
    start = time.time()

    parser = get_parser()
    arguments = parser.parse_args()
    if arguments.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        check_arguments(arguments)
    except Exception as e:
        logging.error(e)
        sys.exit(1)

    file_path = arguments.error_message_file
    result = generate_exception_class_file(file_path)

    end = time.time()
    logging.info("------------------------------------------------------------------------")
    logging.info("EXECUTION SUCCESS")
    logging.info("------------------------------------------------------------------------")
    logging.info("Total time: %ss" % (end - start))
    logging.info("------------------------------------------------------------------------")
    logging.info("artifact file path: %s" % result)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)20s - %(levelname)-8s - %(message)s', level=logging.INFO)
    main()
