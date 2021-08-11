from enum import Enum
from moviepy.editor import VideoFileClip

class ConversionType(Enum):
    SMALL_SIZE = 'small_size'
    NOTE_SIZE = 'note_size'

def convert_video(file_id, conversion_type):
    conversion_type = ConversionType(conversion_type)
    if conversion_type == ConversionType.NOTE_SIZE:
        convert_to_video_note(file_id)
    elif conversion_type == ConversionType.SMALL_SIZE:
        compress_video(file_id)

def convert_to_video_note(file_id):
    clip = VideoFileClip(f'videos/{file_id}.mp4')

    if clip.duration >= 60:
        clip = clip.subclip(0,59)

    clip = clip.resize(height=640)
    clip = clip.crop(x_center=clip.size[0]//2, width=640)

    clip.write_videofile(f"videos/converted/{file_id}.mp4", codec="mpeg4")

def compress_video(file_id):
    pass