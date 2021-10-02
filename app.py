from ApplicationLogger.logger import logger
import config
from src.webScrapper import Load_and_save_TrendingVideos



Logger=logger(config.LOG_PATH)
prefix="APP"
if __name__=="__main__":
    Logger.log("info",f"{prefix} :Starting the main app")
    try:
        Load_and_save_TrendingVideos()
        Logger.log("info",f"{prefix} :Ending the main app")
    except Exception as e:
        Logger.log("error",f"{prefix} :Error while running the main app {e}")

    