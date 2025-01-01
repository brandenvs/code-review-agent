# Determining the Triathlon award winner

# input of times
swimming = float(input("Enter the minutes of swimming: "))
cycling = float(input("Enter the minutes of cycling: "))
running = float(input("Enter the minutes of running: "))

# Calculating the total time
total_time = swimming + cycling + running
print("Total time:", total_time)

if total_time <= 100:
    print("Received Honorary colours")
elif 101 <= total_time <= 105:
    print("Received Honorary half colours")
elif 106 <= total_time <= 110:
    print("Received Honorary scroll")
else:
    print("Received No award")
