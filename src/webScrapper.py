
import re
from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from src.FileHandling import createFolder,clearDirectory
from src.MovieMaker import MakeMovieFromImage,addAudio
import config
import time
from ApplicationLogger.logger import logger

Logger=logger(config.LOG_PATH)
prefix="WEBSCRAPPER"


    
def striphtml(data):
    Logger.log("info",f"{prefix}: starting the strip html function")
    result=""
    try:
        p = re.compile(r'<.*?>')
        result=p.sub('', data)
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while strip html from text {e}")
    Logger.log("info",f"{prefix}: Ending the strip html function")
    return result

def getScreenShot(driver,element,name,pathToSavePhoto,pathToEditPhoto):
    Logger.log("info",f"{prefix}: starting taking screenshots ")
    try:
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        location = element.location
        x = location['x']
        y = location['y']
        driver.execute_script(f"window.scrollTo({int(x)}, {int(y)-100});")
        location = element.location
        x = location['x']
        y = location['y']
        size = element.size

        driver.save_screenshot(f"{pathToEditPhoto}/{name}.png")
        
        width = 330+size['width']
        height = 110+size['height']
        #print(x,y)
        im = Image.open(f'{pathToEditPhoto}/{name}.png')
        im = im.crop((330,110, int(width), int(height)-100))
        im.save(f'{pathToSavePhoto}/{name}.png')
        Logger.log("info",f"{prefix}: Ending the get screenshot function successfully")
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while taking screenshot function {e}")


def getTop5HashTags(driver):
    #//span[contains(text(),'#')]
    Logger.log("info",f"{prefix}: started getting top 5 hashtags function")
    tag_list=[]
    try:
        tags=driver.find_elements_by_xpath("//span[contains(text(),'#')]")
        for i in tags:
            tag=striphtml(i.get_attribute("innerHTML"))
            tag_list.append(tag)
            Logger.log("info",f"{prefix}: Ended getting top 5 hashtags function")
        return tag_list
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while getting top 5 hashtags {e}")
        return tag_list

def filterEmojis(url):
    Logger.log("info",f"{prefix}: started filtering image URLs function")
    try:
        result=True
        skip_url_words=["svg","profile_images","hashflags"]
        for skip in skip_url_words:
            if skip in url:
                result= False
                break
        Logger.log("info",f"{prefix}: Ended filtering image URLs function")
        return result
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while filtering image URLs ")
        return False

def getPosts(driver,post_tag,pathToSavePhoto,pathToEditPhoto):
    img_urls=[]
    number_of_posts=0
    Logger.log("info",f"{prefix}: started get posts function")
    try:
        PostResults = driver.find_elements_by_tag_name("article")
        number_of_posts=len(PostResults)
        pCount=0
        for i in PostResults:
            getScreenShot(driver,i,f"Post{pCount}",pathToSavePhoto,pathToEditPhoto)
            pCount+=1
            # image_urls=i.find_elements_by_tag_name("img")
            # for img in image_urls:
            #     img_url=img.get_attribute("src")
            #     if filterEmojis(img_url):
            #         img_urls.append(img_url)
        video_path=MakeMovieFromImage(pathToSavePhoto,post_tag)
        addAudio(video_path,config.AUDIO_PATH,post_tag)
        Logger.log("info",f"{prefix}: Ended get posts function")
    except Exception as e:
        Logger.log("error",f"{prefix}: Error whil getting posts {e}")
    return img_urls,number_of_posts

def GetChromeDriver():
    Logger.log("info",f"{prefix}: started creating chrome driver")
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.set_window_size(1024, 600)
        driver.maximize_window() 
        Logger.log("info",f"{prefix}: Ended creating chrome driver")
        return driver
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while creating chrome driver {e}")
        return None

def closeChromeDriver(driver):
    Logger.log("info",f"{prefix}: started closing chrome driver")
    try:
        driver.quit()
        Logger.log("info",f"{prefix}: Ended closing chrome driver successfully")
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while closing chrome driver {e}")

def Get_top_Trending_Videos(driver):
    Logger.log("info",f"{prefix}: started getting Trending Videos")
    try:
        driver.get(config.TREND_URL)
        time.sleep(5)#sleep_between_interactions
        tags=getTop5HashTags(driver)
        print(tags)
        if len(tags)==0:
            time.sleep(5)
            tags=getTop5HashTags(driver)
        if len(tags)>0:
            createFolder(config.FINAL_VIDEO_PATH)    
            createFolder(config.EDIT_VIDEO_PATH)
            clearDirectory(config.FINAL_VIDEO_PATH)
            clearDirectory(config.EDIT_VIDEO_PATH)
            tcount=1
            for i in tags:
                i=i.replace("#","")
                url_search=config.SEARCH_URL.replace("QUERY",i)
                driver.get(url_search)
                time.sleep(5)
                pathToSavePhoto=f"{config.FINAL_PHOTO_PATH}/trending{tcount}"
                pathToEditPhoto=f"{config.EDIT_PHOTO_PATH}/trending{tcount}"
                clearDirectory(pathToSavePhoto)
                clearDirectory(pathToEditPhoto)
                createFolder(pathToSavePhoto)
                createFolder(pathToEditPhoto)
                img_urls,NoOfPosts=getPosts(driver,f"trending{tcount}",pathToSavePhoto,pathToEditPhoto)
                tcount+=1
        #Locate the images to be scraped from the current page 
        Logger.log("info",f"{prefix}: Ended getting Trending Videos")
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while getting Trending Videos {e}")


def Load_and_save_TrendingVideos():
    try:
        Logger.log("info",f"{prefix}: started Load_and_save_TrendingVideos function")
        driver= GetChromeDriver()
        Get_top_Trending_Videos(driver)
        closeChromeDriver(driver)
        Logger.log("info",f"{prefix}: Ended Load_and_save_TrendingVideos function")
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while loading Trending Videos {e}")