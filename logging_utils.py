import logging
import json
import os


def set_default_logging(parent_dir, level=logging.INFO):
    os.makedirs(_get_log_dir(parent_dir), exist_ok=True)
    log_file = f"{_get_log_dir(parent_dir)}/wm_logs.log"
    all_log_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    logging.basicConfig(format="%(asctime)s;%(levelname)s;%(message)s",
                        datefmt='%Y-%m-%d,%H:%M:%S',
                        level=level,
                        handlers=[all_log_handler, console_handler])


def get_error_logger(action_type, object_type, log_dir):
    """
    Failures are written to object specific log file.
    """
    logger = logging.getLogger("workspace_migration")

    failed_log_file = get_error_log_file(action_type, object_type, log_dir)
    error_handler = logging.FileHandler(failed_log_file, 'w+')
    error_handler.setLevel(logging.ERROR)

    logger.addHandler(error_handler)
    return logger


def get_error_log_file(action_type, object_type, parent_dir):
    return f"{_get_log_dir(parent_dir)}/failed_{action_type}_{object_type}.log"


def _get_log_dir(parent_dir):
    return parent_dir + "/app_logs"

default_ignore_error_list=[
    'RESOURCE_ALREADY_EXISTS'
]
def log_reponse_error(error_logger,
                      response,
                      error_msg=None,
                      ignore_error_list=default_ignore_error_list):
    if check_error(response, ignore_error_list):
        if error_msg:
            error_logger.error(error_msg)
        else:
            error_logger.error(json.dumps(response))
        return True
    else:
        return False

def check_error(response, ignore_error_list=default_ignore_error_list):
    return ('error_code' in response and response['error_code'] not in ignore_error_list) \
            or ('error' in response and response['error'] not in ignore_error_list) \
            or (response.get('resultType', None) == 'error' and 'already exists' not in response.get('summary', None))
