import logging
import os

def log_file_exists() -> bool:
    """
    Determine if log file exists. If log file does not exist, create it.

    :return: bool
    """
    current_file = 'logger_config.py'
    log_name = 'server_logs.log'
    root = os.path.realpath(current_file).split('server')[0]
    dir_path = os.path.join(root, 'server', 'logs')
    file_path = os.path.join(dir_path, log_name)
    if os.path.exists(file_path):
        return True
    if not os.path.exists(dir_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, 'w') as f:
            pass
        return True
    except Exception as e:
        print(f"Logging file could not be created: {e}")
        return False


def create_logger() -> None:
    """
    Initialise all logs for the project.

    :return: None
    """
    if not log_file_exists():
        return

    logging.basicConfig(filename='logs/server_logs.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')