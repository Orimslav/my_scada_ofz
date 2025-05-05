@echo off
cd /d C:\Webapp\my_scada_ofz
call venv\Scripts\activate.bat
python manage.py readopc
