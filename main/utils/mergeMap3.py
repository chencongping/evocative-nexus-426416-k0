import os
from pydub import AudioSegment


class MergeMap3:

    def __init__(self, map3_input_folder, output):
        self.map3_input_folder = map3_input_folder
        self.output = output

    # noinspection PyUnusedLocal
    def merge(self):
        map3_input_files = self.list_files_in_directory()
        combined = None
        for mp3_path in map3_input_files:
            print(f'{mp3_path}')
            current_audio = AudioSegment.from_mp3(mp3_path)
            if combined is None:
                combined = current_audio
            else:
                combined = combined + current_audio
        combined.export(self.output, format="mp3")
        print(f"音频文件已成功合并并保存为 {self.output}")
        # self.delete_tmp()

    def list_files_in_directory(self):
        file_paths = []
        # 遍历目录中的文件和子目录
        for root, _, input_files in os.walk(self.map3_input_folder):
            for input_file in input_files:
                file_path = os.path.join(root, input_file)
                file_paths.append(file_path)
        # 按文件名排序
        file_paths.sort()
        return file_paths

    def delete_tmp(self):
        for mp3_path in self.list_files_in_directory():
            try:
                os.remove(mp3_path)
                print(f"Deleted file: {mp3_path}")
            except OSError as e:
                print(f"Error deleting file {mp3_path}: {e}")
