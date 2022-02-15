import re
import time

import pyautogui
import pyperclip as pyclip

global class_name
class_name = ""
global method_body
method_body = ""

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = False

PIC_PATH = 'resource/leecode_tool/'
CONFIG_PATH = 'conf/leecode_tool.tt'


def execute():
    with open(CONFIG_PATH) as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        line = line.strip('\n')
        # print("@command line", line)
        array = line.split(" ")
        action = array[0]
        if "click" == action:
            print("#action -> click...")
            pyautogui.click()
        elif "doubleClick" == action:
            print("#action -> doubleClick...")
            pyautogui.doubleClick()
        elif "rightClick" == action:
            print("#action -> rightClick...")
            pyautogui.rightClick()
        elif "locate" == action:
            print("#action -> locate...")
            sign = locate_pic(array[1])
            if not sign:
                print("can't locate[", array[1], "]")
                break
        elif "write" == action:
            print("#action -> write...")
            pyautogui.write(array[1])
        elif "press" == action:
            print("#action -> press...")
            pyautogui.press(array[1])
        elif "hotkey" == action:
            print("#action -> hotkey...")
            pyautogui.hotkey(array[1], array[2])  # pyautogui.hotkey('command', 'f')
        elif "hotkey3" == action:
            print("#action -> hotkey3...")
            pyautogui.hotkey(array[1], array[2], array[3])
        elif "move" == action:
            print("#action -> move...")
            pyautogui.move(int(array[1]), int(array[2]))
        elif "build" == action:
            print("#action -> build_class...")
            build_class()
        elif "pasteclass" == action:
            print("#action -> pasteclass...")
            clip_paste_class()
        elif "pastemethod" == action:
            print("#action -> pastemethod...")
            clip_paste_method()
        elif "sleep" == action:
            time.sleep(int(array[1]))
        else:
            time.sleep(0.5)
            print("i don't know [", line, "], learning...")
    f.close()
    print("---end---")


def locate_pic(line):
    # 在当前屏幕中查找指定图片(图片需要由系统截图功能截取的图)
    line = PIC_PATH + line
    location = pyautogui.locateOnScreen(line, confidence=0.6)
    if location is not None:
        # 截图大小为3584 * 2240，pyautogui.size()大小为1792 * 1120
        # 原因：retina屏*2渲染，https://www.macx.cn/thread-2228242-1-1.html
        print("location:", location)
        x = location[0] / 2
        y = location[1] / 2
        x += location[2] / 4
        y += location[3] / 4
        print(x, y)
        # 移动到该坐标点n
        pyautogui.moveTo(x, y)
        return True
    else:
        return False


def debug_pyautogui():
    # 屏幕分辨率：宽*高
    screen_width, screen_width = pyautogui.size()
    print(screen_width, screen_width)
    # 鼠标当前位置
    print(pyautogui.position())


def build_class():
    content = pyclip.paste()
    pattern = re.compile(r"(public|private|protected)+\s(static)?\s?(\S+)\s(\S+)(\s*)\((\w+.*\w*)?\)")
    print(content)
    method_info = pattern.findall(content)

    # 类名
    print(method_info)
    global class_name
    class_name = method_info[0][3]
    class_name = class_name.title()

    # 方法体
    global method_body
    method_body += content
    method_body += "\n}"
    method_body += "\n\npublic static void main(String[] args) {\n\n}"


def clip_paste_class():
    global class_name
    pyclip.copy(class_name)


def clip_paste_method():
    global method_body
    pyclip.copy(method_body)


if __name__ == '__main__':
    execute()
