import json
from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

def pretty_print_json_to_log(json_data, keyword):
    """
    Pretty print JSON data to the log.

    Parameters:
    - json_data: A Python dictionary or list to be pretty-printed as JSON.
    """
    try:
        pretty_json = json.dumps(json_data, indent=4, sort_keys=True)
        _logger.info(f"{keyword}: {pretty_json}")
    except TypeError as e:
        _logger.error("Error pretty printing JSON: " + str(e))