import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:     %(message)s",
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)
