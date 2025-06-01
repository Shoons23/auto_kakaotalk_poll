import pyautogui
import time
import datetime
import json
import os


def load_coords(json_path="coords.json"):
    if not os.path.exists(json_path):
        print(f"[ERROR] 좌표 파일을 찾을 수 없습니다: {json_path}")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    coord_dict = {}
    for key, val in raw.items():
        if isinstance(val, list) and len(val) == 2:
            coord_dict[key] = tuple(val)
        else:
            print(f"[ERROR] 좌표 형식이 잘못되었습니다: {key} → {val}")
            sys.exit(1)

    return coord_dict

# ---------------------------------------------

def click_and_type(x, y, text=None):
    # 1) click
    pyautogui.click(x, y)
    time.sleep(0.3)
    # 2) input text
    if text is not None:
        pyautogui.write(text, interval=0.05)
        time.sleep(0.3)

def click_and_type_after_clean(x, y, text):
    pyautogui.click(x, y)
    time.sleep(0.5) 

    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    time.sleep(0.2)
    pyautogui.write(text, interval=0.05)
    time.sleep(0.5)

# algorithm ---------------------------------------------

def open_kakao_chatroom(chat_name: str, coords: dict):
    x0, y0 = coords["kakao_window"]
    pyautogui.doubleClick(x0, y0)
    time.sleep(7) 

    sx, sy = coords["search_box"]
    click_and_type(sx, sy, text=chat_name)
    pyautogui.press('enter')
    time.sleep(1) 

def navigate_to_poll(coords: dict):
    bx, by = coords["more_button"]
    pyautogui.click(bx, by)
    time.sleep(1)

    tbx, tby = coords["talk_board"]
    pyautogui.click(tbx, tby)
    time.sleep(0.5)

    px_, py_ = coords["poll_tab"]
    pyautogui.click(px_, py_)
    time.sleep(0.5)

    wx, wy = coords["write_button"]
    pyautogui.click(wx, wy)
    time.sleep(1) 

def fill_poll(title: str, options: list[str], coords: dict):
    tx, ty = coords["title_box"]
    click_and_type_after_clean(tx, ty, title)

    abx, aby = coords["add_option_button"]
    for i in range(3):
        pyautogui.click(abx, aby+60*i)
        time.sleep(0.5) 

    vertical_gap = 60 
    ox, oy = coords["option1_box"]
    for idx, text in enumerate(options):
        opt_x = ox
        opt_y = oy + vertical_gap * idx
        click_and_type(opt_x, opt_y, text=text)

    mx, my = coords["multi_toggle"]
    pyautogui.click(mx, my)
    time.sleep(0.5)

    ex, ey = coords["end_time_toggle"]
    pyautogui.scroll(-330) 
    pyautogui.click(ex,ey)

    cx, cy = coords["create_button"]
    pyautogui.click(cx, cy)
    time.sleep(0.2)

    
# option --------------------------------------------- 
def get_this_week_dates_excluding_saturday(reference_date=None):
    if reference_date is None:
        reference_date = datetime.date.today() + datetime.timedelta(7)
    weekday_idx = reference_date.weekday()  # Monday=0, Sunday=6
    monday = reference_date - datetime.timedelta(days=weekday_idx)
    week_dates = []
    weekdays_en = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    for i in range(7):
        day = monday + datetime.timedelta(days=i)
        if day.weekday() in [0, 1, 2, 3, 4, 6]:
            week_dates.append((day, weekdays_en[day.weekday()]))
    return week_dates

def format_english_date(day: datetime.date, weekday_name: str) -> str:
    yymmdd = day.strftime("%y%m%d")
    return f"{yymmdd} ({weekday_name})"

# ---------------------------------------------
# ---------------------------------------------
# main
# ---------------------------------------------
def main():
    coords = load_coords("coords.json")
    week = get_this_week_dates_excluding_saturday()
    options = [format_english_date(d, wd) for (d, wd) in week]

    
    try:
        open_kakao_chatroom("회식비정산", coords)
        navigate_to_poll(coords)
        fill_poll("Exercise", options, coords)

    except KeyboardInterrupt:
        print("\n[INFO] 프로그램 실행이 Ctrl+C에 의해 중단되었습니다.")
        sys.exit(0)

if __name__ == "__main__":
    main()
