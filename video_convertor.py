from enum import Enum

class ConversionType(Enum):
    SMALL_SIZE = 'small_size'
    NOTE_SIZE = 'note_size'

def convert_video(file_data, conversion_type):
    return file_data