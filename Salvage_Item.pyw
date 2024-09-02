from pynput import keyboard
from PIL import Image, ImageDraw
import pystray
import time
import threading

controller = keyboard.Controller()
running = True
action_thread = None
action_thread_lock = threading.Lock()
listener = None
icon = None

def create_image():
    """
    트레이 아이콘 이미지를 생성합니다.
    """
    # 아이콘 생성
    image = Image.new('RGB', (64, 64), color=(0, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (16, 16, 48, 48),
        fill=(255, 255, 255)
    )
    return image

def quit_action(icon, item):
    icon.stop()
    with action_thread_lock:
        global running
        running = False
    if listener:
        listener.stop()

def start_tray_icon():
    """
    트레이 시작
    """
    global icon
    icon = pystray.Icon('name', create_image(), 'Salvage_Item')
    icon.menu = pystray.Menu(
        pystray.MenuItem('Quit', quit_action)
    )
    icon.run()

def check_running():
    """
    현재 상태가 running인지 확인하고, 그렇지 않으면 함수를 종료합니다.
    """
    with action_thread_lock:
        return running

def press_and_hold(key):
     """
     특정 키를 일정 시간 동안 눌렀다 떼는 함수

     param key : 눌렀다 뗄 키
     param hold_time : 눌렀다 뗄 시간
     """
     time.sleep(0.37)
     controller.press(key)
     start_time = time.time()
     while time.time() - start_time < 1.3:
         if not check_running():
             controller.release(key)
             return
     controller.release(key)

def press_key(key):
     """
     특정 키를 누르는 함수
     """
     time.sleep(0.37)
     controller.press(key)
     time.sleep(0.37)
     controller.release(key)

def perform_f1_actions():
    global running

    # 메뉴 열기
    press_key('i')

    if not check_running():
        return

    # 무기 목록 열기s
    press_key('a')

    if not check_running():
        return
    
    # 전체 선택 shift
    press_and_hold(keyboard.Key.shift)

    if not check_running():
        return

    # 반응로 창으로 이동
    press_key('d')
    press_key('d')

    if not check_running():
        return

    # 전체 선택 shift
    press_and_hold(keyboard.Key.shift)

    if not check_running():
        return

    # 외장부품으로 이동
    press_key('s')

    if not check_running():
        return

    # 전체 선택 shift
    press_and_hold(keyboard.Key.shift)

    if not check_running():
        return

    # 갈갈이 ctrl
    press_and_hold(keyboard.Key.ctrl)

    if not check_running():
        return
    
    # 완료 누르기
    press_key(keyboard.Key.space)

    if not check_running():
        return

    # 메뉴 종료
    press_key(keyboard.Key.esc)
    press_key(keyboard.Key.esc)

def on_press(key):
    global running
    global action_thread
    try:

        # 숫자 f1 키를 눌렀을 때
        if key == keyboard.Key.f1:
            if action_thread is None or not action_thread.is_alive():
                running = True
                action_thread = threading.Thread(target=perform_f1_actions)
                action_thread.start()

        elif key == keyboard.Key.f2:
            # F2 키를 눌러서 동작을 중단
            print("Stopping...")
            running = False

    except AttributeError:
        # 예외 처리
        pass

def on_release(key):
    global icon
    if key == keyboard.Key.f3:
        if icon:
            icon.stop()
        return False  # Listener를 중지합니다.

def start_keyboard_listener():
    """
    키보드 리스너를 시작합니다.
    """
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()

def main():
    
    # 키보드 리스너 시작
    listener_thread = threading.Thread(target=start_keyboard_listener)
    listener_thread.start()
    
    # 트레이 아이콘 시작
    start_tray_icon()
if __name__ == "__main__":
    main()