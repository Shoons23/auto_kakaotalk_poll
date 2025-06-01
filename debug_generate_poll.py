import pyautogui
import time
import datetime
import json
import os
import sys
import ctypes

# ---------------------------------------------

def load_coords(json_path="coords.json"):
    if not os.path.exists(json_path):
        print(f"[ERROR] 좌표 파일을 찾을 수 없습니다: {json_path}")
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

def click_and_type(x, y, text=None):

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

def open_kakao_chatroom(chat_name: str, coords: dict):
    """
    kakao_window 위치를 더블클릭해 카카오톡 창을 활성화하고,
    검색창을 클릭 → chat_name을 입력 후 Enter → 채팅방 진입
    """

    x0, y0 = coords["kakao_window"]
    pyautogui.doubleClick(x0, y0)
    print(f"[DEBUG] kakao_window 더블클릭 → ({x0}, {y0})")
    time.sleep(7)  # 창 활성화 충분히 대기

    sx, sy = coords["search_box"]
    click_and_type(sx, sy, text=chat_name)
    pyautogui.press('enter')
    print(f"[DEBUG] Enter 키 → 채팅방 \"{chat_name}\" 열기")
    time.sleep(1)  # 채팅방이 열릴 때까지 대기

# ---------------------------------------------
# 5) 톡게시판 → 투표 만들기 화면 진입
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
    vertical_gap = 60 
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

    
    ex, ey = coords["end_time_toggle"]
    pyautogui.scroll(-330)  # 아래로 스크롤
    pyautogui.click(ex,ey)

    # (5) 등록
    cx, cy = coords["create_button"]
    # pyautogui.click(cx, cy)
    print("test end")
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
