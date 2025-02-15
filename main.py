#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pynput.keyboard import Key
from pynput import keyboard
import time
import struct


# 定义按键事件的数据结构
# 使用 struct 模块将数据打包为二进制格式
# 格式：按键（1字节），行为（1字节），时间戳（8字节，毫秒级）
EVENT_FORMAT = '!BBQ'  # ! 表示网络字节序（大端序），B 是无符号字节，Q 是无符号长整型（8字节）

# 用于追踪已按下的键
pressed_keys = set()

# 用于存储数据的二进制文件
file = None

# 插入按键信息到数据库
def insert_key_event(action: int, virtual_key_code: int):
    global file
    if file:
        # 获取当前时间戳
        timestamp = int(time.time())
        packed_data = struct.pack(EVENT_FORMAT, virtual_key_code, action, timestamp)
        print(virtual_key_code, action, timestamp)
        file.write(packed_data)
        file.flush()


# 键盘按下事件处理函数
def on_press(key):
    try:
        if isinstance(key, Key):
            vk = key.value.vk
        else:
            vk = key.vk
        # 只在按键没有被记录时记录它
        if vk not in pressed_keys:
            action = 1 
            # 记录按下的按键
            pressed_keys.add(vk)  
            insert_key_event(action, vk)
    except Exception as e:
        print(f"Error: {e}")


# 键盘释放事件处理函数
def on_release(key):
    try:
        if isinstance(key, Key):
            vk = key.value.vk
        else:
            vk = key.vk
        # 按键释放时移除按键
        if vk in pressed_keys:
            action = 0
            pressed_keys.remove(vk)
            insert_key_event(action, vk)
    except Exception as e:
        print(f"Error: {e}")


def start_listener():
    global file
    file = open('key_events.bin', 'wb')
    try:
        # 设置信号捕获
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    finally:
        if file:
            file.close()
            file = None


if __name__ == '__main__':
    start_listener()
