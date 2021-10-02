import moviepy.editor as mp
import os
from moviepy import *
from moviepy.editor import ImageClip,concatenate_videoclips,VideoFileClip,AudioFileClip,CompositeAudioClip
import config
from ApplicationLogger.logger import logger

Logger=logger(config.LOG_PATH)
prefix="WEBSCRAPPER"


def MakeMovieFromImage(folderPath,videoName):
    Logger.log("info",f"{prefix}: started making movie from images")
    try:
        image_folder=folderPath
        image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".png")]
        #print(image_files)
        #clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
        clips = [ImageClip(m).set_duration(2)
          for m in image_files]
        video_save_path=f'{config.EDIT_VIDEO_PATH}/{videoName}.mp4'
        concat_clip = concatenate_videoclips(clips, method="compose")
        concat_clip.write_videofile(video_save_path, fps=24,codec='mpeg4',audio_codec='aac')
        Logger.log("info",f"{prefix}: Ended making movie from images")
        return video_save_path
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while making movie from images{e}")
        return None

def addAudio(video_path,audio_path,video_name):
    Logger.log("info",f"{prefix}: started adding audio to video")
    try:
        videoclip = VideoFileClip(video_path)
        audioclip = AudioFileClip(audio_path)
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        videoclip.write_videofile(f"{config.FINAL_VIDEO_PATH}/{video_name}.mp4")
        Logger.log("info",f"{prefix}: Ended adding audio to video")
    except Exception as e:
        Logger.log("error",f"{prefix}: Error while adding audio to video {e}")