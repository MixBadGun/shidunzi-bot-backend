:: ---------------------------------------------------------------- ::
::  **Notice**:                                                     ::
::      This file is under the decoding of GB2312. If you cannot    ::
::      view the content in this file correctly in VSCode, you can  ::
::      enable "files.autoGuessEncoding" setting in VSCode.         ::
::                                                                  ::
::      I'm not going to make *this* file able to work in other     ::
::      non-Chinese computers. If you have any solution, you can    ::
::      edit this file directly or just write a Python-based script ::
::      to run tests automatically and generate the `coverage`      ::
::      reports. Thank you!                                         ::
:: ---------------------------------------------------------------- ::

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