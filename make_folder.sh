# make a folder for the year and day

year=$1
day=$2

mkdir -p $year/day_$day
touch $year/day_$day/day$day.py
touch $year/day_$day/input.txt
touch $year/day_$day/test_input.txt