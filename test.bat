@echo off
call ./.venv/Scripts/activate.bat

coverage run -m unittest discover
coverage html

echo ==============
echo �������к���
echo ��������Ͽ�������������
echo Ҳ���Դ� .\htmlcov\index.html �鿴Ŀǰ�Ĳ��Ը�����
echo ==============

pause