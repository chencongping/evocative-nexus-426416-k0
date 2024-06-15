from pydub import AudioSegment

# 加载两个 MP3 文件
audio1 = AudioSegment.from_mp3("path/to/first_file.mp3")
audio2 = AudioSegment.from_mp3("path/to/second_file.mp3")

# 合并音频
combined = audio1 + audio2

# 导出合并后的音频文件
combined.export("path/to/combined_file.mp3", format="mp3")

print("音频文件已成功合并并保存为 'combined_file.mp3'")
