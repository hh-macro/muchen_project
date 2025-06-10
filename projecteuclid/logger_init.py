# -- coding: utf-8 --
# @Author: 胡H
# @File: logger_init.py
# @Created: 2025/6/10 15:31
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import sys
from pathlib import Path

from loguru import logger

current_file = Path(__file__).parent  #
project_rootpath = current_file.parent  #
# ================================= 日志配置 =====================================
log_dir = Path(project_rootpath)
log_dir.mkdir(parents=True, exist_ok=True)

# 清除默认配置
logger.remove()

# 控制台输出配置
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{file}:{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# 文件输出配置（自动轮转）
logger.add(
    log_dir / "init.log",
    rotation="10 MB",  # 每个日志文件最大10MB
    retention="30 days",  # 保留30天日志
    compression="zip",  # 旧日志压缩为zip
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {file}:{line} - {message}",
    level="DEBUG"
)

