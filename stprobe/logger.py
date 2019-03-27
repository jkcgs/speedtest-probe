import logging

logger = logging.getLogger('st-probe')

log_format = '%(asctime)s | %(levelname)-8s | %(message)s'
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_format, '%Y-%m-%d %H:%M:%S')
stdout_logger = logging.StreamHandler()
stdout_logger.setLevel(logging.DEBUG)
stdout_logger.setFormatter(formatter)
logger.addHandler(stdout_logger)
