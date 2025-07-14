#!/bin/bash

# Directory to monitor
MONITOR_DIR="."

# Log file
LOG_FILE="monitor.log"

# Function to log changes
log_change() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" >> $LOG_FILE
}

# Initial state
find $MONITOR_DIR -type f -exec md5sum {} + > /tmp/checksums.initial

log_change "Monitoring started for directory: $MONITOR_DIR"

# Monitor loop
while true; do
    # Current state
    find $MONITOR_DIR -type f -exec md5sum {} + > /tmp/checksums.current

    # Compare states
    diff /tmp/checksums.initial /tmp/checksums.current > /tmp/checksums.diff

    # Check for changes
    if [ -s /tmp/checksums.diff ]; then
        # Log created files
        grep "^>" /tmp/checksums.diff | while read -r line; do
            file=$(echo "$line" | awk '{print $3}')
            log_change "File created: $file"
        done

        # Log deleted files
        grep "^<" /tmp/checksums.diff | while read -r line; do
            file=$(echo "$line" | awk '{print $3}')
            log_change "File deleted: $file"
        done

        # Log modified files
        grep -v "^<" /tmp/checksums.diff | grep -v "^>" | while read -r line; do
            file=$(echo "$line" | awk '{print $3}')
            log_change "File modified: $file"
        done

        # Update initial state
        cp /tmp/checksums.current /tmp/checksums.initial
    fi

    sleep 1
done
