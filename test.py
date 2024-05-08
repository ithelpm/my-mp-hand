import logging

logging.basicConfig(level=logging.INFO, filename="test.log")

if __name__ == "__main__":
    logger = logging.getLogger("Main")
    logger.info("Success...")