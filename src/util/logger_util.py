import logging

def get_logger_statements(logger_name, logging_level=logging.INFO):
    """
    This is a helper method defined to add logger statements for debugging

    Returns:
    logger statements that are formatted by time
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)

    stream_handler = logging.StreamHandler()
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    return logger