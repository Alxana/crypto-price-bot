import logging
import sys

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the root logger level (DEBUG shows all levels)

# Formatter for the logs
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console handler (for real-time logs)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  # Adjust level for console (INFO and above)
console_handler.setFormatter(formatter)

# File handler (for storing logs)
file_handler = logging.FileHandler("../application.log")
file_handler.setLevel(logging.DEBUG)  # Log DEBUG and above to file
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)