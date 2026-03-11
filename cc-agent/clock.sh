#!/usr/bin/env bash

function start_clock() {
	start_time=$(date +%s.%N)
	echo -n $start_time > CLOCK_START
}

function get_clock() {
	if [ ! -f CLOCK_START ]; then
		start_clock
	fi
	start_time=$(<CLOCK_START)
	current_time=$(date +%s.%N)
	elapsed_time=$(echo "$current_time - $start_time" | bc)
	printf "%.6f" $elapsed_time
}

function clear_clock() {
	if [ -f CLOCK_START ]; then
		rm -r CLOCK_START
		echo "Clock cleared."
	else
		echo "No clock to clear."
	fi
}

# Check argument and call appropriate function
if [ "$1" == "start" ]; then
	start_clock
elif [ "$1" == "get" ]; then
	get_clock
elif [ "$1" == "clear" ]; then
	clear_clock
else
    echo "Please specify a valid arg (start, get)."
fi


# start_time=$(date +%s.%N)
# while true; do
#    current_time=$(date +%s.%N)
#    elapsed_time=$(echo "$current_time - $start_time" | bc)
#    printf "\r%.6f seconds" $elapsed_time
#     echo -n $elapsed_time > clock
#     sleep 0.1  # Adjust sleep time as needed
# done
