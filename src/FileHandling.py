from ApplicationLogger.logger import logger
import os
from ApplicationLogger.logger import logger
import config

Logger=logger(config.LOG_PATH)
prefix="WEBSCRAPPER"

def createFolder(folder_path):
    Logger.log("info",f"{prefix}: started create folder function")
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            Logger.log("info",f"{prefix}: Ended create folder function")
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while creating folder {e}")

    
  
def clearDirectory(folder_path):
    Logger.log("info",f"{prefix}: started clear directory function")
    try:
        if os.path.exists(folder_path):
            dir = folder_path
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
            Logger.log("info",f"{prefix}: Ended clear directory function")
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while clearing directory {e}")