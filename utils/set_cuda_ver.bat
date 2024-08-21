@echo off
REM Set the desired CUDA version
set CUDA_VERSION=11.7

REM Set the CUDA paths based on the version
set CUDA_PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v%CUDA_VERSION%
set PATH=%CUDA_PATH%\bin;%CUDA_PATH%\libnvvp;%PATH%
set CUDA_HOME=%CUDA_PATH%

REM Activate the virtual environment
call E:\dev\audiocraft\.venv\Scripts\activate

REM Confirm the CUDA version being used
nvcc --version