import os

# 假设单词表存储在一个名为'word_list.txt'的文件中
topic_name = '5500-words-and-explain.txt'
word_list_file = f'../../resource/txt/{topic_name}'

# 读取单词表文件
with open(word_list_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 遍历每一行，并写入单独的文件
for line in lines:
    # 分割每一行，找到"----"的位置
    parts = line.strip().split('----')
    if len(parts) == 2:  # 确保每一行都有"----"并且两边都有内容
        filename = parts[0].strip()  # 文件名
        content = parts[1].strip()  # 文件内容

        output_folder = f'../../output/{topic_name}'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 写入文件
        with open(f'{output_folder}/{filename}' + '.txt', 'w', encoding='utf-8') as outfile:
            outfile.write(content)
    else:
        print(f"Skipping line: {line.strip()}, as it does not contain '----' correctly.")

print("Files have been written successfully.")
