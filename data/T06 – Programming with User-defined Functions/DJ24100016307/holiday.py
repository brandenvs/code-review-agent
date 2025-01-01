### TASK 6 ###

# Request entry of city from customer
city_flight = input("Choose a city from London, Berlin, Paris and Vienna: ")

# Request customer enters the number of nights in hotel
num_nights = int(input("Enter the number of nights you will stay in your hotel: "))

# Request customer enters the number of days they will hire a car
rental_days = int(input("Enter the number of days you will be hiring a car: "))

# Return results to customer
print("You have selected: ")
print("City:", city_flight)
print("Number of Nights:", num_nights)
print("Car Rental Days:", rental_days)


# Create function for hotel costs
"""
Calculate the hotel cost.
Parameters: sets the hotel price at 60 per night
Returns: number of nights as entered by the customer in 'num_nights', multiplied by the 
price per night
"""

def hotel_cost(num_nights):
    price_per_night = 60    # Price per night
    return num_nights * price_per_night


# Create a function for flight costs
"""
Calculate the flight cost.
Parameters: Determine the city as entered by the customer in 'city_flight'.
Returns: Set the cost by city chosen.
"""

def plane_cost(city_flight):
    if city_flight == "Vienna":
        return 250  # Cost of Berlin flight
    elif city_flight == "Berlin": 
        return 200  # Cost of Berlin flight
    elif city_flight == "Paris":
        return 150  # Cost of Paris flight
    elif city_flight == "London":
        return 100  # Cost of London flight
    

# Create a function for car rental costs:
"""
Calculate the cost of car rental.
Parameters: Set the car rental price per day.
Returns: The cost of car rental multiplied by 'rental_days' as entered by the customer
"""

def car_rental(rental_days):    # Price per rental day
    price_per_day = 25
    return rental_days * price_per_day


# Calculate the total cost of the holiday
total_cost = hotel_cost(num_nights) + plane_cost(city_flight) + car_rental(rental_days)

# Return total holiday cost

print(f"The total cost of your holiday is: £{total_cost:.2f}")
