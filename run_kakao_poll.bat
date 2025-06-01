@echo off

REM 1) 가상환경(venv) 활성화
CALL "%~dp0dongbu_venv\Scripts\activate.bat"

REM 2) 스크립트가 있는 디렉터리로 이동 
CD /D "%~dp0"

REM 3) 파이썬 스크립트 실행
python auto_kakaotalk_poll.py

REM 4) 가상환경 비활성화
CALL deactivate
