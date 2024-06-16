import concurrent.futures
import time


# 定义一个示例任务函数
def task(name, duration):
    print(f"任务 {name} 开始执行")
    time.sleep(duration)
    print(f"任务 {name} 执行完毕")
    return f"任务 {name} 完成"


# 使用 ThreadPoolExecutor 来管理线程池和异步任务
def main():
    tasks = [
        ('A', 2),
        ('B', 3),
        ('C', 1),
    ]

    # 创建一个 ThreadPoolExecutor 对象
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # 提交任务并获取 future 对象
        # futures = [executor.submit(task, name, duration) for name, duration in tasks]
        executor.submit(task, 'A', 0)

        # 等待所有任务完成并获取结果
        # for future in concurrent.futures.as_completed(futures):
        #     result = future.result()
        #     print(result)


if __name__ == "__main__":
    main()
