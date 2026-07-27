#!/bin/bash
#
# Usage:
#   ./backup2.sh                 # Exclude ./results
#   ./backup2.sh -all            # Include ./results
#   ./backup2.sh -a test         # Archive name: cc-agent-test-YYYYMMDD-HHMM.tar.gz
#   ./backup2.sh -all -a test    # Include ./results and append "test" to the filename

EXCLUDES=(
    --exclude='./agent/venv'
    --exclude='./backup'
)

INCLUDE_RESULTS=false
SUFFIX=""

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -all)
            INCLUDE_RESULTS=true
            shift
            ;;
        -a)
            SUFFIX="-$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [-all] [-a <suffix>]"
            exit 1
            ;;
    esac
done

# Exclude ./results unless -all is specified
if ! $INCLUDE_RESULTS; then
    EXCLUDES+=(--exclude='./results')
fi

ARCHIVE="backup/cc-agent-$(date +%Y%m%d-%H%M)${SUFFIX}.tar.gz"

tar "${EXCLUDES[@]}" -czvf "$ARCHIVE" .

echo $ARCHIVE generated..