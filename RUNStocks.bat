@echo off
C:
CD\
CD  C:\git\stocks

REM Activate the virtual environment 
call C:\git\stocks\venv\Scripts\activate.bat

REM Start MonoDB
REM call C:\Program Files\MongoDB\Server\6.0\bin>mongod
REM call mongod --port 27017 --dbpath C:\git\hackathon2023\db
REM Open in new cli window
call START C:\"Program Files"\MongoDB\Server\6.0\bin\mongod --port 27017 --dbpath C:\git\stocks\db

REM Launcho MongoDB Compass
call C:\Users\OMFG\AppData\Local\MongoDBCompass\MongoDBCompass.exe

REM Start tika server
REM Open in new window
call cd \
call cd c:\tika
call START /B java -jar tika-server-standard-2.8.0.jar --port 9998

REM Run python command  
REM call python docproc.py
REM call streamlit run ingest_app_test.py
REM call streamlit run test-chat.py

REM Working code to import PDF file
REM call streamlit run doc-proc-pdf-upload.py

REM Testing code to search and summarize PDF file
REM call streamlit run doc-proc-pdf-summarize.py

REM Deactivate the virtual environment
call C:\git\hackathon2023\venv\Scripts\deactivate.bat

REM Check PDF File
REM call python show_pdf.py