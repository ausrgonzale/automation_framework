#!/bin/bash

# E2E Test Runner Script for Django Application
# This script helps run Playwright E2E tests with various options

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ ${NC}$1"
}

print_success() {
    echo -e "${GREEN}✓ ${NC}$1"
}

print_warning() {
    echo -e "${YELLOW}⚠ ${NC}$1"
}

print_error() {
    echo -e "${RED}✗ ${NC}$1"
}

# Function to check if Django server is running
check_django_server() {
    print_info "Checking if Django server is running on localhost:8000..."
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        print_success "Django server is running"
        return 0
    else
        print_error "Django server is not running on localhost:8000"
        print_warning "Please start the Django server with: python manage.py runserver"
        return 1
    fi
}

# Function to display usage
show_usage() {
    cat << EOF
${GREEN}E2E Test Runner for Django Application${NC}

Usage: ./run_tests.sh [OPTIONS]

${YELLOW}Options:${NC}
    -a, --all           Run all E2E tests
    -r, --registration  Run only registration tests
    -h, --headed        Run tests in headed mode (visible browser)
    -s, --slow          Run tests in slow motion (for debugging)
    -f, --fast          Run only fast tests (skip slow tests)
    -v, --verbose       Run with verbose output
    -d, --debug         Run with debug output (verbose + print statements)
    -k PATTERN          Run tests matching PATTERN
    -m MARKER           Run tests with specific MARKER
    --help              Show this help message

${YELLOW}Examples:${NC}
    ./run_tests.sh -a                    # Run all E2E tests
    ./run_tests.sh -r                    # Run registration tests
    ./run_tests.sh -r -h                 # Run registration tests in headed mode
    ./run_tests.sh -a -f                 # Run all fast tests
    ./run_tests.sh -k password           # Run tests matching 'password'
    ./run_tests.sh -m "registration"     # Run tests marked as registration
    ./run_tests.sh -d -s                 # Run in debug mode with slow motion

${YELLOW}Markers:${NC}
    registration    - User registration tests
    login           - Login functionality tests
    auth            - Authentication required tests
    slow            - Tests that run slowly
    fast            - Quick-running tests
    e2e             - End-to-end tests

EOF
}

# Check for help flag first
if [[ "$1" == "--help" ]]; then
    show_usage
    exit 0
fi

# Check if Django server is running
if ! check_django_server; then
    exit 1
fi

# Default values
VERBOSE=""
TEST_PATTERN=""
MARKER=""
HEADED=""
SLOWMO=""
EXTRA_ARGS=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--all)
            TEST_PATTERN="tests/e2e/"
            shift
            ;;
        -r|--registration)
            TEST_PATTERN="tests/e2e/test_user_registration.py"
            shift
            ;;
        -h|--headed)
            HEADED="--headed"
            shift
            ;;
        -s|--slow)
            SLOWMO="--slowmo 500"
            shift
            ;;
        -f|--fast)
            MARKER="-m \"not slow\""
            shift
            ;;
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        -d|--debug)
            VERBOSE="-v -s"
            shift
            ;;
        -k)
            EXTRA_ARGS="$EXTRA_ARGS -k $2"
            shift 2
            ;;
        -m)
            MARKER="-m $2"
            shift 2
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# If no test pattern specified, default to all e2e tests
if [[ -z "$TEST_PATTERN" ]]; then
    TEST_PATTERN="tests/e2e/"
fi

# Build the pytest command
CMD="pytest $TEST_PATTERN $VERBOSE $HEADED $SLOWMO $MARKER $EXTRA_ARGS"

# Print the command being run
print_info "Running command: $CMD"
echo ""

# Run the tests
eval $CMD
TEST_EXIT_CODE=$?

# Print summary
echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    print_success "All tests passed!"
else
    print_error "Some tests failed. Exit code: $TEST_EXIT_CODE"
fi

exit $TEST_EXIT_CODE
