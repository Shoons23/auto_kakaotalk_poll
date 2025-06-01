# auto_kakaotalk_poll
temporal program for badminton our club


* **다음 주 날짜 계산**: 오늘 기준 +7일을 기준으로 해당 주의 월\~금 및 일요일만 추출
* **PyAutoGUI 자동화**: 저장된 좌표( coords.json )를 불러와 카카오톡 열기 → 톡게시판 → 투표화면 이동 → 입력 순서 수행
* **IME(입력기) 전환**: 현재 입력 언어가 한글이면 한영 키 토글 후 영문 모드에서 “Exercise” 입력 (추가 예정)
* **투표 생성 흐름**:
  1. 지정 채팅방 열기
  2. 톡게시판 → 투표 탭 → 글쓰기 클릭
  3. 제목에 “Exercise” 입력
  4. 옵션 슬롯 확장 후 계산된 날짜(“YYMMDD (Day)”) 6개 입력
  5. 중복 참여 허용 토글 클릭

**실행 방법**

1. 작업 폴더에 auto_kakaotalk_poll.py 와 coords.json 생성(수작업 ㅠ)
2. PyAutoGUI 설치(`pip install pyautogui`)
3. 터미널에서 `python auto_kakaotalk_poll.py` 실행

4. (선택) Windows 작업 스케줄러에 배치 파일 등록 → 매주 일요일 17:00에 실행되도록 설정

## test 1 

window 작업 스케쥴러에 .bat 파일을 등록 후 250601 11:59:59에 실행 -> 작동완료