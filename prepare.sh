#!/bin/bash

# run generate_dirty_data.py
python3 generate_dirty_data.py

grep -v "#" ms_data_dirty.csv | sed -e '/^$/d' | sed -e "s/,,/,/g" | cut -d"," -f"1,2,4,5,6" > ms_data.csv

# remove comment lines
# grep -v "#" ms_data_dirty.csv > ms_data_ing.csv

# # remove empty lines
# sed -e '/^$/d' ms_data_ing.csv > ms_data_ing.csv

# # remove extra comma
# sed -e "s/,,/,/g" ms_data_ing.csv > ms_data_ing.csv

# # extract 
# cut -d"," -f"1,2,4,5,6" ms_data_ing.csv > ms_data.csv

## command in one line grep -v "#" ms_data_ing.csv | sed -e '/^$/d' > ms_data_ing.csv

# create insurance.lst
touch insurance.lst
echo Basic > insurance.lst
echo Premium >> insurance.lst
echo -n Platinum >> insurance.lst # append

# count the number of visits
echo "The total number of visits are $(tail -n+2 ms_data.csv | wc -l)"
tail -n+2 ms_data.csv | head