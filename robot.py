import sys
import os
import win32con
import win32gui
import win32ui
import win32api
import numpy as np
import time
import json
import math
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QDoubleSpinBox, QMessageBox
from PySide2.QtCore import QRegExp, QSettings, QRect, Signal
from PySide2.QtGui import QRegExpValidator
from UIView import Ui_UIView
from PIL import Image
from pynput.keyboard import Key, Listener
from inputs import get_gamepad, UnpluggedError
from threading import Thread
from qt_material import QtStyleTools, list_themes


vk_dict = {chr(x).lower(): x for x in list(range(48, 58)) + list(range(65, 91))}
vk_dict.update({'.': 190, '/': 191, 'space': 32, ';': 186, '\'': 222, ',': 188, '[': 219,
                ']': 221, '\\': 220, '-': 189, '=': 187})

pos_chop_progress_bar = (692, 346, 748, 362)
pos_dirty_dish = (628, 787, 710, 865)
pos_rpot = (828, 272, 869, 312)
pos_lpot = (767, 272, 808, 312)
pos_serving_table2 = (1227, 723, 1312, 793)
pos_serving_table1 = (1202, 668, 1287, 738)
pos_lucannon0 = (536, 483, 623, 553)
pos_lucannon = (563, 392, 640, 460)
pos_lbcannon = (530, 787, 623, 865)
pos_rucannon = (1300, 400, 1380, 466)
pos_rbcannon = (1316, 786, 1414, 870)
pos_trash_bin = (1198, 533, 1284, 608)

img_chop_progress_bar = np.array(Image.open('images/chop.png'), dtype=float)
img_dirty_dish = np.array(Image.open('images/dirty.png'), dtype=float)
img_rpot = np.array(Image.open('images/rpot.png'), dtype=float)
img_lpot = np.array(Image.open('images/lpot.png'), dtype=float)
img_lucannon = np.array(Image.open('images/lucannon.png'), dtype=float)
img_lucannon0 = np.array(Image.open('images/lucannon0.png'), dtype=float)
img_lbcannon = np.array(Image.open('images/lbcannon.png'), dtype=float)
img_rucannon = np.array(Image.open('images/rucannon.png'), dtype=float)
img_rbcannon = np.array(Image.open('images/rbcannon.png'), dtype=float)


def is_cannoned_to_lu(): return not match_img(pos_lucannon, img_lucannon, thresh=50)
def is_cannoned_to_lu0(): return not match_img(pos_lucannon0, img_lucannon0, thresh=50)
def is_cannoned_to_lb(): return not match_img(pos_lbcannon, img_lbcannon, thresh=58)
def is_cannoned_to_ru(): return not match_img(pos_rucannon, img_rucannon, thresh=55)
def is_cannoned_to_rb(): return not match_img(pos_rbcannon, img_rbcannon, thresh=58)
def is_chopped(): return not match_img(pos_chop_progress_bar, img_chop_progress_bar, thresh=70)
def is_dirty_dish_placed(): return match_img(pos_dirty_dish, img_dirty_dish, thresh=35)
def is_rpot_empty(): return not match_img(pos_rpot, img_rpot, thresh=40)
def is_lpot_empty(): return not match_img(pos_lpot, img_lpot, thresh=50)


def screenshot():
    # hwnd = win32gui.FindWindow(None, 'Overcooked! 2')
    hwnd = 0
    wdc = win32gui.GetWindowDC(hwnd)
    w = win32ui.GetDeviceCaps(wdc, win32con.DESKTOPHORZRES)
    h = win32ui.GetDeviceCaps(wdc, win32con.DESKTOPVERTRES)
    dc_obj = win32ui.CreateDCFromHandle(wdc)
    cdc = dc_obj.CreateCompatibleDC()
    data_bitmap = win32ui.CreateBitmap()
    data_bitmap.CreateCompatibleBitmap(dc_obj, w, h)
    cdc.SelectObject(data_bitmap)
    cdc.BitBlt((0, 0), (w, h), dc_obj, (0, 0), win32con.SRCCOPY)
    signed_ints_array = data_bitmap.GetBitmapBits(True)
    img = Image.frombuffer('RGBA', (w, h), signed_ints_array).convert('RGB')
    if w/h < 16/9:
        padding = int((h-w/16*9)/2)
        img = img.crop((0, padding, w, h-padding))
    elif w/h > 16/9:
        padding = int((w-h/9*16)/2)
        img = img.crop((padding, 0, w-padding, h))
    #     Free Resources
    dc_obj.DeleteDC()
    cdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, wdc)
    win32gui.DeleteObject(data_bitmap.GetHandle())
    return img


class Offset:
    offset = (0, 0)

    @classmethod
    def update(cls, img_screen):
        scale = img_screen.size[1] / 1080
        pos_new = tuple(round(x * scale) for x in pos_trash_bin)
        w = pos_trash_bin[2] - pos_trash_bin[0]
        h = pos_trash_bin[3] - pos_trash_bin[1]
        tile = img_screen.crop(pos_new).resize((w, h))
        tile = np.array(tile, dtype=float)
        try:
            black = tile.sum(axis=2) < 30
            if black.sum() > 500:
                left = np.argwhere(black.sum(axis=0) > 15)[1, 0]
                right = np.argwhere(black.sum(axis=0) > 15)[-2, 0]
                upper = np.argwhere(black.sum(axis=1) > 15)[1, 0]
                bottom = np.argwhere(black.sum(axis=1) > 15)[-2, 0]
            else:  # near trash bin
                black = tile.sum(axis=2) < 100
                left = np.argwhere(black.sum(axis=0) > 8)[1, 0]
                right = np.argwhere(black.sum(axis=0) > 8)[-2, 0] + 3
                upper = np.argwhere(black.sum(axis=1) > 8)[1, 0]
                bottom = np.argwhere(black.sum(axis=1) > 8)[-2, 0] + 8
            cls.offset = ((left + right - tile.shape[1]) // 2, (upper + bottom - tile.shape[0]) // 2)
        except (ValueError, IndexError):
            pass
        return cls.offset


def get_tile(img_screen, pos, offset):
    pos_new = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[0], pos[3] + offset[1])
    scale = img_screen.size[1] / 1080
    pos_new = tuple(round(x * scale) for x in pos_new)
    w = pos[2] - pos[0]
    h = pos[3] - pos[1]
    tile = img_screen.crop(pos_new).resize((w, h))
    tile = np.array(tile, dtype=float)
    tile = tile[..., [2, 1, 0]]
    return tile


def match_img(pos, img_src, thresh, debug=0):
    img_screen = screenshot()
    offset = Offset.update(img_screen)
    tile = get_tile(img_screen, pos, offset)
    diff = np.mean(np.abs(tile - img_src))
    if debug == 1:
        print(diff)
    return diff < thresh


def match_serving_table(debug=0):
    img_screen = screenshot()
    offset = Offset.update(img_screen)
    tile1 = get_tile(img_screen, pos_serving_table1, offset)
    tile2 = get_tile(img_screen, pos_serving_table2, offset)
    covered1 = np.sum((tile1[..., 2] - tile1[..., 0]) > 30) < 3000
    covered2 = np.sum((tile2[..., 2] - tile2[..., 0]) > 30) < 3000
    if debug == 1:
        print(covered1, covered2)
    if covered1 and covered2:
        return 2
    elif covered1:
        return 1
    else:
        return 0


class UIFunc(QMainWindow, Ui_UIView, QtStyleTools):
    msg_signal = Signal()

    def __init__(self, app):
        super(UIFunc, self).__init__()
        self.app = app
        self.setupUi(self)
        reg_exp = QRegExp(r"[0-9a-zA-Z,/;'=\.\[\]\\\-]")
        self.lineEdit_dict = {
            'Up': self.lineEdit_1,
            'Down': self.lineEdit_2,
            'Left': self.lineEdit_3,
            'Right': self.lineEdit_4,
            'Operate': self.lineEdit_5,
            'PickUp': self.lineEdit_6,
            'Dash': self.lineEdit_7
        }
        for lineEdit in self.lineEdit_dict.values():
            lineEdit.setValidator(QRegExpValidator(reg_exp))

        self.config = QSettings('config.ini', QSettings.IniFormat)
        self.choice_num_order.setCurrentText(self.config.value('Config/Orders'))
        self.choice_start.setCurrentIndex(int(self.config.value('Config/Start')))
        self.choice_stop.setCurrentIndex(int(self.config.value('Config/Stop')))
        self.doubleSpinBox_2.setValue(float(self.config.value('Config/PlateDelay2')))
        self.doubleSpinBox_3.setValue(float(self.config.value('Config/PlateDelay3')))
        self.doubleSpinBox_31.setValue(float(self.config.value('Config/PlateDelay31')))
        self.doubleSpinBox_top.setValue(float(self.config.value('Config/LandingDelayTop')))
        self.doubleSpinBox_lbottom.setValue(float(self.config.value('Config/LandingDelayLBottom')))
        self.doubleSpinBox_rbottom.setValue(float(self.config.value('Config/LandingDelayRBottom')))
        self.checkBox_onion.setChecked(self.config.value('Config/Onion') == 'true')
        self.choice_donut.setCurrentIndex(int(self.config.value('Config/Donut')))
        self.choice_theme.addItems(list_themes())
        self.choice_theme.setCurrentText(self.config.value('Config/Theme'))

        self.set_keymap_text()

        self.choice_num_order.currentIndexChanged.connect(self.on_config_change)
        self.choice_start.currentIndexChanged.connect(self.on_config_change)
        self.choice_stop.currentIndexChanged.connect(self.on_config_change)
        self.doubleSpinBox_2.valueChanged.connect(self.on_config_change)
        self.doubleSpinBox_3.valueChanged.connect(self.on_config_change)
        self.doubleSpinBox_31.valueChanged.connect(self.on_config_change)
        self.doubleSpinBox_top.valueChanged.connect(self.on_config_change)
        self.doubleSpinBox_lbottom.valueChanged.connect(self.on_config_change)
        self.doubleSpinBox_rbottom.valueChanged.connect(self.on_config_change)
        self.checkBox_onion.stateChanged.connect(self.on_config_change)
        self.choice_donut.currentIndexChanged.connect(self.on_config_change)
        self.start_key = self.stop_key = None
        self.on_config_change()
        for lineEdit in self.lineEdit_dict.values():
            lineEdit.textEdited.connect(self.on_keymap_change)
        self.keymap_dict = dict()
        self.on_keymap_change()
        self.choice_theme.currentTextChanged.connect(self.on_theme_change)
        self.on_theme_change()

        self.playing = False
        self.msg_signal.connect(lambda: QMessageBox.critical(self, 'Error', '请设置键位'))

        def on_press(key):
            if key == self.start_key and not self.playing:
                if len(''.join(set(self.keymap_dict.values()))) < 7:
                    self.msg_signal.emit()
                else:
                    self.playing = True
                    self.robot_thread = RobotThread(self)
                    self.robot_thread.start()
            elif key == self.stop_key and self.playing:
                self.robot_thread.playing = False
                self.playing = False

        self.keyboard_listener = Listener(on_press=on_press)
        self.keyboard_listener.start()

        def monitor_gamepad():
            while True:
                try:
                    events = get_gamepad()
                    for event in events:
                        if event.state == 1:
                            on_press(event.code)
                except UnpluggedError:
                    time.sleep(0.1)
                    pass
        self.gamepad_listener = Thread(target=monitor_gamepad)
        self.gamepad_listener.daemon = True
        self.gamepad_listener.start()

    def set_keymap_text(self):
        for name, lineEdit in self.lineEdit_dict.items():
            v = self.config.value('Config/'+name)
            if v == ':':
                v = ';'
            lineEdit.setText(v)

    def on_config_change(self):
        self.config.setValue('Config/Orders', self.choice_num_order.currentText())
        self.config.setValue('Config/Start', self.choice_start.currentIndex())
        self.config.setValue('Config/Stop', self.choice_stop.currentIndex())
        self.config.setValue('Config/PlateDelay2', self.doubleSpinBox_2.value())
        self.config.setValue('Config/PlateDelay3', self.doubleSpinBox_3.value())
        self.config.setValue('Config/PlateDelay31', self.doubleSpinBox_31.value())
        self.config.setValue('Config/LandingDelayTop', self.doubleSpinBox_top.value())
        self.config.setValue('Config/LandingDelayLBottom', self.doubleSpinBox_lbottom.value())
        self.config.setValue('Config/LandingDelayRBottom', self.doubleSpinBox_rbottom.value())
        self.config.setValue('Config/Onion', self.checkBox_onion.isChecked())
        self.config.setValue('Config/Donut', self.choice_donut.currentIndex())
        start_dict = {0: Key.f1, 1: Key.shift_r, 2: "BTN_START"}
        stop_dict = {0: Key.esc, 1: "BTN_SELECT"}
        self.start_key = start_dict[self.choice_start.currentIndex()]
        self.stop_key = stop_dict[self.choice_stop.currentIndex()]

    def on_keymap_change(self):
        dict0 = {
            'Up': 'W',
            'Down': 'S',
            'Left': 'A',
            'Right': 'D',
            'Operate': 'Oem_2',
            'PickUp': 'Space',
            'Dash': 'Oem_Period'
        }
        new_keymap_dict = {dict0[name]: lineEdit.text().lower() for name, lineEdit in self.lineEdit_dict.items()}
        # 有键位冲突
        if len(''.join(new_keymap_dict.values())) > len(''.join(set(new_keymap_dict.values()))):
            self.set_keymap_text()
        else:
            self.keymap_dict = new_keymap_dict
            for name, lineEdit in self.lineEdit_dict.items():
                v = lineEdit.text().lower()
                if v == ';':
                    v = ':'
                self.config.setValue('Config/'+name, v)

    def on_theme_change(self):
        self.apply_stylesheet(self.app, theme=self.choice_theme.currentText())
        self.config.setValue("Config/Theme", self.choice_theme.currentText())


class RobotThread(Thread):
    def __init__(self, frame: UIFunc):
        super().__init__(name='robot')
        self.frame = frame
        self.playing = True

    def sleep(self, sec: float):
        if not self.playing:
            return
        t0 = time.time()
        if sec > 0.02:
            time.sleep(sec-0.02)
        while True:
            t = time.time() - t0
            if t > sec:
                break

    def wait_for(self, is_func):
        while self.playing:
            if is_func():
                return True
        return False

    def run(self):
        num_order = self.frame.choice_num_order.currentText()
        plate_delay2 = self.frame.doubleSpinBox_2.value()
        plate_delay3 = self.frame.doubleSpinBox_3.value()
        plate_delay31 = self.frame.doubleSpinBox_31.value()
        landing_delay_top = self.frame.doubleSpinBox_top.value()
        landing_delay_lb = self.frame.doubleSpinBox_lbottom.value()
        landing_delay_rb = self.frame.doubleSpinBox_rbottom.value()
        onion = self.frame.checkBox_onion.isChecked()
        donut = self.frame.choice_donut.currentIndex()
        script_dir = 'scripts/'
        script_dict = {}
        for filename in os.listdir(script_dir):
            path = os.path.join(script_dir, filename)
            name = filename[:filename.find('.txt')]
            script_dict[name] = self.parse_script(path)

        lu_stay_list = [
            'lu-fw1', is_chopped,
            'lu-fw2', is_chopped,
            'lu-fw3', is_lpot_empty,
            'lu-fw4'
        ]
        serve_list = ['rb', 'wait_4th', 'rb-4th']
        all_list = [
            'ru-start', is_cannoned_to_lu0,
            'lu-start1', is_chopped,
            *['lu-start2', is_chopped] * 6,
            'lu-start3', is_rpot_empty,
            'lu-start4', is_cannoned_to_rb,
            'rb-start', 'wait_4th_2',
            'rb-4th',
            'lu-fw-b1', is_cannoned_to_ru,
            'ru-fw1', is_cannoned_to_lb,
            'wash2',
            'ru-bw1', is_cannoned_to_lu,
            'lu-bw0', is_cannoned_to_rb,
            *serve_list,
            *lu_stay_list, is_cannoned_to_ru,
            'ru-fw2', is_cannoned_to_lb,
            'wash',
            'ru-bw0', is_cannoned_to_lu,
            'lu-bw1', is_cannoned_to_rb,
            *serve_list,
            *lu_stay_list, is_cannoned_to_ru,
            'ru-fw3', is_cannoned_to_lb,
            'wash',
            'ru-bw0', is_cannoned_to_lu,
            'lu-bw1', is_cannoned_to_rb,
            *serve_list,
            'lu-fw-b2', is_cannoned_to_ru,
            'ru-fw3', is_cannoned_to_lb,
            'wash',
            'ru-bw0', is_cannoned_to_lu,
            'lu-bw1', is_cannoned_to_rb,
            *serve_list,
            *lu_stay_list, is_cannoned_to_ru,
            'ru-fw4-choco', is_cannoned_to_lb,
            'wash',
            'ru-bw0', is_cannoned_to_lu,
            'lu-bw1', is_cannoned_to_rb,
            *serve_list,
            'lu-fw-b2', is_cannoned_to_ru,
            'ru-fw3', is_cannoned_to_lb,
            'wash',
            'ru-bw0', is_cannoned_to_lu,
            'lu-bw2', is_cannoned_to_rb,
            *serve_list,
            'lu-fw5', is_cannoned_to_ru,
            'ru-fw5', is_cannoned_to_lb,
            'wash',
            'ru-bw0', is_cannoned_to_lu,
            'lu-bw3', is_cannoned_to_rb,
            *serve_list
        ]
        if num_order != '29' and donut == 1:
            all_list[91] = 'ru-fw4-berry'
        if num_order != '29' and donut == 2:
            all_list[91] = 'ru-fw4-both'
            if num_order != '32X':
                all_list[94] = 'ru-bw1'
            else:
                all_list[115] = 'ru-fw3'
        if num_order == '29':
            all_list[91] = 'ru-fw5'
            all_list[103] = 'ru-fw5'
            all_list[117] = 'wash3'
        elif num_order == '31':
            all_list[23] = 'lu-fw-b2'
            all_list[30] = 'lu-bw0-31'
            all_list[27] = 'wash3'
            all_list.insert(21, 'wait_4th_2')
            all_list.insert(22, 'rb-start-31')
        elif num_order in ['32', '32X']:
            all_list[16] = 'lu-start3-32'
            all_list[23] = 'lu-fw-b3'
            all_list[30] = 'lu-bw0-31'
            all_list[27] = 'wash'
            all_list.insert(21, 'wait_4th_2')
            all_list.insert(22, 'rb-start-31')
            all_list.insert(21, 'wait_4th_2')
            all_list.insert(22, 'rb-start-31')
            if num_order == '32X':
                all_list[70] = 'lu-bw1-32'
                all_list[82] = 'lu-bw1-32'
                all_list[100] = 'lu-bw1-32'
                all_list[112] = 'lu-bw1-32' if onion else 'lu-bw0-31'
                all_list[117] = 'lu-fw-b3'
                all_list[75] = 'lu-fw-b3'
                all_list[105] = 'lu-fw-b3'
                del all_list[57:64]
                all_list.insert(57, 'lu-fw-b3')
                del all_list[81:88]
                all_list.insert(81, 'lu-fw-b3')
        if num_order != '32X' and onion:
            all_list[-38] = 'lu-fw3-1'
            all_list[-36] = 'lu-fw4-1'

        #####
        # all_list = [is_cannoned_to_rb, 'rb-start',
        #             is_4th_dish_placed, 'rb-start-31', is_4th_dish_placed, 'rb-4th', 'lu-fw5']
        # all_list = [is_cannoned_to_rb, 'rb']
        #####
        steps = len(all_list)
        i = 0
        while i < steps:
            task = all_list[i]
            if isinstance(task, str):
                if task == 'wait_4th':
                    table = 0
                    while self.playing and table == 0:
                        table = match_serving_table()
                    if table == 2:
                        self.run_script_once(script_dict[all_list[i+1]], thd=self)
                    else:
                        self.run_script_once(script_dict[all_list[i+1]+'-1'], thd=self)
                    i += 1
                elif task == 'wait_4th_2':
                    while self.playing:
                        if match_serving_table() == 2:
                            break
                elif task == 'wash2':
                    self.sleep(0.75)
                    self.wait_for(is_dirty_dish_placed)
                    self.run_script_once(script_dict['lb-take1'], thd=self)
                    self.sleep(2.95)
                    self.run_script_once(script_dict['lb-put1'], thd=self)
                    self.sleep(2.8)
                    self.run_script_once(script_dict['lb-put2'], thd=self)
                elif task == 'wash3':
                    self.sleep(0.75)
                    self.wait_for(is_dirty_dish_placed)
                    self.run_script_once(script_dict['lb-take1'], thd=self)
                    self.sleep(2.95)
                    self.run_script_once(script_dict['lb-put1'], thd=self)
                    self.sleep(2.8 + plate_delay31)
                    self.run_script_once(script_dict['lb-put1'], thd=self)
                    self.sleep(2.8 - plate_delay31)
                    self.run_script_once(script_dict['lb-put2'], thd=self)
                elif task == 'wash':
                    self.sleep(0.75)
                    self.wait_for(is_dirty_dish_placed)
                    self.run_script_once(script_dict['lb-take1'], thd=self)
                    self.sleep(2.35)
                    if self.playing:
                        if is_dirty_dish_placed():
                            self.run_script_once(script_dict['lb-take2'], thd=self)
                            self.sleep(0.45)
                        else:
                            self.sleep(0.6)
                    self.run_script_once(script_dict['lb-put1'], thd=self)
                    self.sleep(2.8 + plate_delay2)
                    self.run_script_once(script_dict['lb-put1'], thd=self)
                    self.sleep(2.8 - plate_delay2 + plate_delay3)
                    self.run_script_once(script_dict['lb-put1'], thd=self)
                    self.sleep(2.8 - plate_delay3)
                    self.run_script_once(script_dict['lb-put2'], thd=self)
                else:
                    self.run_script_once(script_dict[task], thd=self)
            else:
                self.wait_for(task)
                if task is is_cannoned_to_rb and landing_delay_rb > 0:
                    self.sleep(landing_delay_rb)
                elif task is is_cannoned_to_lb and landing_delay_lb > 0:
                    self.sleep(landing_delay_lb)
                elif task in [is_cannoned_to_ru, is_cannoned_to_lu, is_cannoned_to_lu0] and landing_delay_top > 0:
                    self.sleep(landing_delay_top)
            i += 1
            if not self.playing:
                return

        self.playing = False
        self.frame.playing = False

    def parse_script(self, script_path):
        content = ''
        with open(script_path, 'r', encoding='utf8') as f:
            lines = f.readlines()
        for line in lines:
            if '//' in line:
                index = line.find('//')
                line = line[:index]
            line = line.strip()
            content += line

        content = content.replace('],\n]', ']\n]').replace('],]', ']]')
        s = json.loads(content)
        steps = len(s)
        events = []
        for i in range(steps):
            delay = s[i][0]
            message = s[i][2].lower()
            action = s[i][3]
            vk = vk_dict[self.frame.keymap_dict[action[1]].lower()]
            events.append({'delay': delay, 'message': message, 'vk': vk})
        return events

    def run_script_once(self, events, thd):
        steps = len(events)
        i = 0
        if not self.playing:
            return False
        while i < steps:
            event = events[i]
            delay, message, vk = event['delay'], event['message'], event['vk']
            thd.sleep(delay / 1000)
            if not self.playing:
                for key in self.frame.keymap_dict.values():
                    vk = vk_dict[key.lower()]
                    win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
                return False
            if message == 'key down':
                win32api.keybd_event(vk, 0, 0, 0)
            elif message == 'key up':
                win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
            i += 1
        return True


def resize_layout(ui, ratio_h):
    ui.resize(ui.width() * ratio_h, ui.height() * ratio_h)
    for q_widget in ui.findChildren(QWidget):
        q_widget.setGeometry(QRect(
            q_widget.x() * ratio_h,
            q_widget.y() * ratio_h,
            q_widget.width() * ratio_h,
            q_widget.height() * ratio_h
        ))
        q_widget.setStyleSheet('font-size: ' + str(math.ceil(9 * min(ratio_h, ratio_h))) + 'px')
        if isinstance(q_widget, QDoubleSpinBox):
            q_widget.setStyleSheet('padding-left: 7px')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UIFunc(app)
    hwnd = 0
    # hwnd = win32gui.FindWindow(None, 'Overcooked! 2')
    wdc = win32gui.GetWindowDC(hwnd)
    h = win32ui.GetDeviceCaps(wdc, win32con.DESKTOPVERTRES)
    ratio_h = h / 1080
    win32gui.ReleaseDC(hwnd, wdc)
    if ratio_h > 1:
        resize_layout(ui, ratio_h)

    ui.setFixedSize(ui.width(), ui.height())

    ui.show()
    sys.exit(app.exec_())
