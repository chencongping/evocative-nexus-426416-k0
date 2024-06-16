import logging
import os

# 创建日志目录
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# 配置日志
log_file = os.path.join(log_directory, "app.log")
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),  # 将日志写入文件
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

# 获取日志记录器
logger = logging.getLogger(__name__)

# 日志示例
logger.debug("这是调试信息")
logger.info("这是普通信息")
logger.warning("这是警告信息")
logger.error("这是错误信息")
logger.critical("这是严重错误信息")
