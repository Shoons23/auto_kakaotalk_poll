# get_kakao_coords.py
#
# 사용 방법:
# 1) 관리자 권한으로 터미널(CMD/Powershell 등) 실행
# 2) python get_kakao_coords.py
# 3) 카카오톡 UI 창을 띄운 뒤, 좌표를 알고 싶은 지점에 마우스를 올려놓고
#    Ctrl+Shift+X 키를 누르면 터미널에 (x, y) 좌표가 찍힙니다.
#
#    찍힌 좌표 값을 복사해서 자동화 스크립트의 COORD 딕셔너리에 붙여넣어 사용하세요.
#
# 4) 스크립트 종료: Ctrl+C 또는 터미널 종료

import pyautogui
import keyboard
import time

def main():
    print("=== 좌표 찍기 도구 ===")
    print("카카오톡 UI 위에서 마우스를 옮긴 뒤, Ctrl+Shift+X 를 누르면 좌표가 표시됩니다.")
    print("여러 지점을 찍어서 기록하고 싶으면 원하는 만큼 Ctrl+Shift+X 를 누르세요.")
    print("종료하려면 Ctrl+C 를 누르세요.\n")

    # 잠시 대기 후 실행 (사용자가 카카오톡 창을 준비할 시간 주기)
    time.sleep(1)

    try:
        while True:
            # keyboard 모듈을 사용해 Ctrl+Shift+X 조합 입력을 감지
            if keyboard.is_pressed('ctrl+shift+x'):
                x, y = pyautogui.position()
                # 현재 시간을 같이 출력하면 나중에 기록 관리하기 편함
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"[{timestamp}] 좌표: ({x}, {y})")
                # 키가 눌렸을 때 너무 빠르게 여러 번 찍히는 것을 방지하기 위해 짧게 대기
                time.sleep(0.5)

            # 약간의 CPU 점유율을 낮추기 위한 짧은 대기
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")


if __name__ == "__main__":
    main()
