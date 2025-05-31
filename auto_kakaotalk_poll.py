import pyautogui
import time
import datetime
import json
import os
import sys
import ctypes

# ---------------------------------------------
# PyAutoGUI 안전 설정
# ---------------------------------------------
pyautogui.FAILSAFE = True   # 마우스를 좌측 상단(0,0)으로 옮기면 즉시 예외 발생
pyautogui.PAUSE = 0.2       # 클릭/타이핑 사이에 0.2초 자동 대기


# ---------------------------------------------
# 1) 날짜 계산: 이번 주 월요일 ~ 일요일 중 월~금 + 일요일만 리스트 생성
# ---------------------------------------------
def get_this_week_dates_excluding_saturday(reference_date=None):
    if reference_date is None:
        reference_date = datetime.date.today() + datetime.timedelta(7)
    weekday_idx = reference_date.weekday()  # Monday=0, Sunday=6
    monday = reference_date - datetime.timedelta(days=weekday_idx)
    week_dates = []
    weekdays_en = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    for i in range(7):
        day = monday + datetime.timedelta(days=i)
        # 월(0)~금(4), 일(6)만 포함
        if day.weekday() in [0, 1, 2, 3, 4, 6]:
            week_dates.append((day, weekdays_en[day.weekday()]))
    return week_dates

def format_english_date(day: datetime.date, weekday_name: str) -> str:
    # 두 자리 연도(YY), 월(MM), 일(DD)
    yymmdd = day.strftime("%y%m%d")
    return f"{yymmdd} ({weekday_name})"

# ---------------------------------------------
# 2) coords.json 파일에서 COORD 불러오기
# ---------------------------------------------
def load_coords(json_path="coords.json"):
    if not os.path.exists(json_path):
        print(f"[ERROR] 좌표 파일을 찾을 수 없습니다: {json_path}")
        sys.exit(1)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        print(f"[ERROR] 좌표 파일 로드 중 오류: {e}")
        sys.exit(1)

    coord_dict = {}
    for key, val in raw.items():
        if isinstance(val, list) and len(val) == 2:
            coord_dict[key] = tuple(val)
        else:
            print(f"[ERROR] 좌표 형식이 잘못되었습니다: {key} → {val}")
            sys.exit(1)

    return coord_dict

# ---------------------------------------------
# 3) 클릭 & 타이핑 헬퍼: 단순 클릭 → 입력
# ---------------------------------------------
def click_and_type(x, y, text=None):
    """
    (x, y) 위치를 클릭한 뒤,
    text가 주어지면 문자열 작성 (영문/숫자용)
    """
    # 1) 클릭
    pyautogui.click(x, y)
    print(f"[DEBUG] 클릭 → ({x}, {y})")
    time.sleep(0.3)

    # 2) 텍스트 입력
    if text is not None:
        print(f"[DEBUG] 입력 → \"{text}\"")
        pyautogui.write(text, interval=0.05)
        time.sleep(0.3)

def click_and_type_after_clean(x, y, text):

    # 1) 제목란 클릭
    pyautogui.click(x, y)
    print(f"[DEBUG] (제목) 클릭 → ({x}, {y})")
    time.sleep(0.5)  # 클릭 후 충분히 기다려야 입력란이 활성화됨

    # 2) 전체 선택 (Ctrl+A) → 플레이스홀더 포함 모든 텍스트 선택
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    print("[DEBUG] (제목) Ctrl+A → 전체 선택")
    time.sleep(0.2)

    # 3) 덮어쓰기할 텍스트 입력
    print(f"[DEBUG] (제목) 입력 → \"{text}\"")
    pyautogui.write(text, interval=0.05)
    time.sleep(0.5)  # 입력 후에도 충분히 기다려야 UI가 업데이트됨

# ---------------------------------------------
# 4) 채팅방 열기 (처음에 kakao_window 더블클릭 → 이후 대기)
# ---------------------------------------------
def open_kakao_chatroom(chat_name: str, coords: dict):
    """
    kakao_window 위치를 더블클릭해 카카오톡 창을 활성화하고,
    검색창을 클릭 → chat_name을 입력 후 Enter → 채팅방 진입
    """
    # (1) kakao_window 위치를 더블클릭
    x0, y0 = coords["kakao_window"]
    pyautogui.doubleClick(x0, y0)
    print(f"[DEBUG] kakao_window 더블클릭 → ({x0}, {y0})")
    time.sleep(5)  # 창 활성화 충분히 대기

    # (2) 검색창 클릭 → 채팅방 이름 입력 → Enter → 대기
    sx, sy = coords["search_box"]
    click_and_type(sx, sy, text=chat_name)
    pyautogui.press('enter')
    print(f"[DEBUG] Enter 키 → 채팅방 \"{chat_name}\" 열기")
    time.sleep(1)  # 채팅방이 열릴 때까지 대기

# ---------------------------------------------
# 5) 톡게시판 → 투표 만들기 화면 진입
# ---------------------------------------------
def navigate_to_poll(coords: dict):
    # (1) 더보기(⋯) 클릭
    bx, by = coords["more_button"]
    pyautogui.click(bx, by)
    print(f"[DEBUG] 더보기 클릭 → ({bx}, {by})")
    time.sleep(1)

    # (2) 톡게시판 클릭
    tbx, tby = coords["talk_board"]
    pyautogui.click(tbx, tby)
    print(f"[DEBUG] 톡게시판 클릭 → ({tbx}, {tby})")
    time.sleep(0.5)

    # (3) 투표 탭 클릭
    px, py_ = coords["poll_tab"]
    pyautogui.click(px, py_)
    print(f"[DEBUG] 투표 탭 클릭 → ({px}, {py_})")
    time.sleep(0.5)

    # (4) 글쓰기 버튼 클릭 → 투표 만들기 화면 진입
    wx, wy = coords["write_button"]
    pyautogui.click(wx, wy)
    print(f"[DEBUG] 글쓰기 버튼 클릭 → ({wx}, {wy})")
    time.sleep(1)  # 투표 만들기 화면이 로드될 대기

# ---------------------------------------------
# 6) 투표 만들기: 제목 “exercise” 입력 → 슬롯 확장 → 순서대로 옵션 입력 → 토글 클릭 → 등록 좌표 출력
# ---------------------------------------------

def fill_poll(title: str, options: list[str], coords: dict):
    # (1) 제목 “exercise” 입력
    tx, ty = coords["title_box"]
    click_and_type_after_clean(tx, ty, title)

    # (2) 기본 3개 슬롯 → 총 6개 슬롯이 필요하므로 옵션 추가 버튼 3회 클릭
    abx, aby = coords["add_option_button"]
    for i in range(3):
        pyautogui.click(abx, aby+60*i)
        print(f"[DEBUG] 옵션 추가 버튼 클릭 ({i+1}/3) → ({abx}, {aby+60*i})")
        time.sleep(0.5)  # 슬롯 생기는 시간 확보

    # (3) 총 6개 슬롯에 순서대로 날짜/요일(영어) 입력
    vertical_gap = 60  # 옵션칸 간격(px)
    ox, oy = coords["option1_box"]
    for idx, text in enumerate(options):
        opt_x = ox
        opt_y = oy + vertical_gap * idx
        click_and_type(opt_x, opt_y, text=text)
        print(f"[DEBUG] 옵션 {idx+1} 입력 → \"{text}\" (좌표: {opt_x}, {opt_y})")

    # (4) 중복 참여 허용 토글 클릭
    mx, my = coords["multi_toggle"]
    pyautogui.click(mx, my)
    print(f"[DEBUG] 중복 참여 허용 토글 클릭 → ({mx}, {my})")
    time.sleep(0.5)

    # (5) 등록
    cx, cy = coords["create_button"]
    # print(f"[TEST MODE] '등록' 버튼 좌표: ({cx}, {cy}) (클릭하면 실제 등록됩니다.)")
    # pyautogui.click(cx, cy)
    time.sleep(0.2)

# ---------------------------------------------
# 7) 메인 흐름
# ---------------------------------------------
def main():
    coords = load_coords("coords.json")
    week = get_this_week_dates_excluding_saturday()
    options = [format_english_date(d, wd) for (d, wd) in week]

    # if is_english_input() != 1:
    #     print("[INFO] 현재 한글 모드 감지 → 한영 키로 English 모드로 전환합니다.")
    #     toggle_hangul_key()
    #     time.sleep(0.5)
    
    try:
        # 3) 채팅방 열기
        print("[INFO] 채팅방 열기 시작")
        open_kakao_chatroom("회식비정산", coords)

        # 4) 톡게시판 → 투표 만들기 화면 진입
        print("[INFO] 톡게시판 → 투표 만들기 화면 진입")
        navigate_to_poll(coords)

        # 5) 투표 생성: 제목="exercise", 옵션=options
        print("[INFO] 투표 입력 시작: 제목 및 옵션 자동 입력")
        fill_poll("Exercise", options, coords)

    except KeyboardInterrupt:
        print("\n[INFO] 프로그램 실행이 Ctrl+C에 의해 중단되었습니다.")
        sys.exit(0)

if __name__ == "__main__":
    main()
