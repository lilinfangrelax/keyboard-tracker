#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import struct


"""从二进制文件中读取按键事件"""

# 定义按键事件的数据结构
# 使用 struct 模块将数据打包为二进制格式
# 格式：按键（1字节），行为（1字节），时间戳（8字节，毫秒级）
EVENT_FORMAT = '!BBQ'  # ! 表示网络字节序（大端序），B 是无符号字节，Q 是无符号长整型（8字节）


def load_events(file):
    """
    从二进制文件中读取按键事件
    :param file: 文件对象
    :return: 返回按键事件列表
    """
    events = []
    while True:
        # 每次读取 10 字节（1 + 1 + 8）
        packed_data = file.read(10)
        if not packed_data:
            break
        # 解包二进制数据
        key, action, timestamp = struct.unpack(EVENT_FORMAT, packed_data)
        events.append((key, action, timestamp))
    return events


if __name__ == "__main__":
    # 使用 'rb' 模式以二进制读取方式打开文件
    with open('key_events.bin', 'rb') as f:
        events = load_events(f)
        for key, action, timestamp in events:
            # 将时间戳转换为可读格式
            dt = datetime.fromtimestamp(timestamp)
            print(f"Key: {chr(key)}, Action: {'Pressed' if action == 1 else 'Released'}, Timestamp: {dt}")