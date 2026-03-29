@echo off
REM E2E Test Runner Script for Django Application (Windows)
REM This script helps run Playwright E2E tests with various options

setlocal enabledelayedexpansion

REM Function to check if Django server is running
echo [INFO] Checking if Django server is running on localhost:8000...
curl -s http://localhost:8000 >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Django server is not running on localhost:8000
    echo [WARNING] Please start the Django server with: python manage.py runserver
    exit /b 1
)
echo [SUCCESS] Django server is running

REM Default values
set "TEST_PATTERN=tests/e2e/"
set "VERBOSE="
set "HEADED="
set "SLOWMO="
set "MARKER="
set "EXTRA_ARGS="

REM Parse command line arguments
:parse_args
if "%~1"=="" goto run_tests
if /i "%~1"=="-a" (
    set "TEST_PATTERN=tests/e2e/"
    shift
    goto parse_args
)
if /i "%~1"=="--all" (
    set "TEST_PATTERN=tests/e2e/"
    shift
    goto parse_args
)
if /i "%~1"=="-r" (
    set "TEST_PATTERN=tests/e2e/test_user_registration.py"
    shift
    goto parse_args
)
if /i "%~1"=="--registration" (
    set "TEST_PATTERN=tests/e2e/test_user_registration.py"
    shift
    goto parse_args
)
if /i "%~1"=="-h" (
    set "HEADED=--headed"
    shift
    goto parse_args
)
if /i "%~1"=="--headed" (
    set "HEADED=--headed"
    shift
    goto parse_args
)
if /i "%~1"=="-s" (
    set "SLOWMO=--slowmo 500"
    shift
    goto parse_args
)
if /i "%~1"=="--slow" (
    set "SLOWMO=--slowmo 500"
    shift
    goto parse_args
)
if /i "%~1"=="-v" (
    set "VERBOSE=-v"
    shift
    goto parse_args
)
if /i "%~1"=="--verbose" (
    set "VERBOSE=-v"
    shift
    goto parse_args
)
if /i "%~1"=="-d" (
    set "VERBOSE=-v -s"
    shift
    goto parse_args
)
if /i "%~1"=="--debug" (
    set "VERBOSE=-v -s"
    shift
    goto parse_args
)
if /i "%~1"=="-f" (
    set "MARKER=-m \"not slow\""
    shift
    goto parse_args
)
if /i "%~1"=="--fast" (
    set "MARKER=-m \"not slow\""
    shift
    goto parse_args
)
if /i "%~1"=="--help" (
    goto show_usage
)
echo [ERROR] Unknown option: %~1
goto show_usage

:run_tests
REM Build and run the pytest command
set "CMD=pytest %TEST_PATTERN% %VERBOSE% %HEADED% %SLOWMO% %MARKER% %EXTRA_ARGS%"
echo [INFO] Running command: %CMD%
echo.

%CMD%
set TEST_EXIT_CODE=%errorlevel%

echo.
if %TEST_EXIT_CODE% equ 0 (
    echo [SUCCESS] All tests passed!
) else (
    echo [ERROR] Some tests failed. Exit code: %TEST_EXIT_CODE%
)

exit /b %TEST_EXIT_CODE%

:show_usage
echo.
echo E2E Test Runner for Django Application
echo.
echo Usage: run_tests.bat [OPTIONS]
echo.
echo Options:
echo     -a, --all           Run all E2E tests
echo     -r, --registration  Run only registration tests
echo     -h, --headed        Run tests in headed mode (visible browser)
echo     -s, --slow          Run tests in slow motion (for debugging)
echo     -f, --fast          Run only fast tests (skip slow tests)
echo     -v, --verbose       Run with verbose output
echo     -d, --debug         Run with debug output (verbose + print statements)
echo     --help              Show this help message
echo.
echo Examples:
echo     run_tests.bat -a              # Run all E2E tests
echo     run_tests.bat -r              # Run registration tests
echo     run_tests.bat -r -h           # Run registration tests in headed mode
echo     run_tests.bat -a -f           # Run all fast tests
echo.
exit /b 0
