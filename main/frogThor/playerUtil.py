from mutagen.mp3 import MP3


def get_mp3_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length


class PlayerUtil:
    pass
