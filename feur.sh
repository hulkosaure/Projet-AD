#!/bin/bash

# Counter variable
counter=0

# Loop through the desired number of times
for i in {1..5}; do
  # Check if the counter is zero
  if [ $counter -eq 0 ]; then
    # Execute spd-say command
    spd-say "feur"

    # Set the counter to 1 to prevent further executions
    counter=1
  fi

  # You can add more commands or logic here if needed
  # ...

done

