from function import func
import numpy as np
import logging

def setLogger():
    logger = logging.getLogger("main")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('log_file.log', mode='w')
    file_handler.setLevel(logging.INFO)

    errors = logging.FileHandler('log_file.log')
    errors.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    file_handler.setFormatter(formatter)
    errors.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(errors)
    return logger


if __name__ == "__main__":


    logger = setLogger()
    n = 10000
    ar = [float(i) for i in np.random.randint(1, n, n)]
    logger.info(f"Program started with ar: {ar}")
    func(ar)
    logger.info("Done!")
