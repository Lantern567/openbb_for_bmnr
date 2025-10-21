@echo off
REM Set API keys as environment variables before starting backend
SET OPENBB_FMP_API_KEY=aMygwSPUSv1KUf1OxlVPvk12JrJnIGpi
SET OPENBB_POLYGON_API_KEY=hzQYA0NSR15nlAT3Bym3nFCsTuF05inq

REM Activate conda and start backend
call conda activate bmnr_analysis
cd /d "E:\code\openbb_for_finance\backend"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
