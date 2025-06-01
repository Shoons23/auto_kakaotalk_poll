
def toggle_hangul_key():
    """
    VK_HANGUL(0x15)을 눌렀다 떼어서 한영 모드를 전환.
    """
    user32 = ctypes.windll.user32
    VK_HANGUL = 0x15
    KEYEVENTF_KEYUP = 0x0002

    # 한영 키 누르기
    user32.keybd_event(VK_HANGUL, 0, 0, 0)
    time.sleep(0.05)
    # 한영 키 떼기
    user32.keybd_event(VK_HANGUL, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.1)

def is_english_input() -> int:
    """
    현재 포그라운드 윈도우의 키보드 레이아웃을 확인하여,
    English(US)의 LID(0x0409)이면 1, 아니면 0 반환.
    """
    user32 = ctypes.windll.user32

    # 1) 포그라운드 윈도우 핸들
    hwnd = user32.GetForegroundWindow()
    # 2) 해당 윈도우의 스레드 ID
    tid = user32.GetWindowThreadProcessId(hwnd, 0)
    # 3) 그 스레드의 키보드 레이아웃 핸들
    layout = user32.GetKeyboardLayout(tid)
    # 4) 하위 WORD(16비트)만 추출하여 Language ID(LID) 확인
    lid = layout & 0xFFFF

    # 0x0409 = English (US) → 1, 그 외(예: 0x0412 한글) → 0
    return 1 if lid == 0x0409 else 0