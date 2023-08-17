import logging as log

"""
    -The basicConfig method of the logging module is used to configure the logging system.
    -The level parameter sets the logging level to log.INFO, which means only log messages with level INFO and higher 
     will be processed.
    -The format parameter sets the message format of the log message. In this case, it's set to '%(message)s.
    -The handlers parameter is set to a list with one element, log.StreamHandler(),
    -which means log messages will be handled by the StreamHandler class and sent to the standard output stream (sys.stderr)
"""

log.basicConfig(
    level=log.INFO,
    format='%(message)s',
    handlers=[log.StreamHandler()]
)
