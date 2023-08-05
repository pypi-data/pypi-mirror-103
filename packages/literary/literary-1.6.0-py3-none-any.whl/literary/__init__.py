import os
import logging

LOGLEVEL = os.environ.get("LITERARY_LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)
