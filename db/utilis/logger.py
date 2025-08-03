import logging
from colorlog import ColoredFormatter

# Configure logging with color
def setup_logging(filename='seeding.log'):
    # Create a logger object
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Define log format for color logging
    log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s%(reset)s"
    date_format = '%Y-%m-%d %H:%M:%S'
    cformatter = ColoredFormatter(log_format, date_format,
                                  log_colors={
                                      'DEBUG': 'cyan',
                                      'INFO': 'green',
                                      'WARNING': 'yellow',
                                      'ERROR': 'red',
                                      'CRITICAL': 'red,bg_white',
                                  })

    # Create console handler and add the colored formatter to it
    ch = logging.StreamHandler()
    ch.setFormatter(cformatter)
    logger.addHandler(ch)

    # Optionally add a file handler
    fh = logging.FileHandler(filename)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', date_format))
    logger.addHandler(fh)

    return logger

# Usage example
if __name__ == "__main__":
    logger = setup_logging()
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")