# --> HOLIDAY COST TASK (LATEST VERSION) <--



# TASK -- USER INPUT

# dictionary of destination options & fligth cost: key = city, value = price
user_options = {"Paris": 140, "Amsterdam": 172, "Berlin": 189}
print(f"Your destination options & the price (£): {user_options}")
print()

# user input of chosen destination
# .capitalise() to match the dictionary keys
city_flight = str(input("Enter a destination: ")).capitalize()

# user input for duration of stay
num_nights = int(input("How many nights will you be away? "))

# user input for days renting a car
rental_days = int(input("How many days will you rent a car? "))
print()



# DESTINATION -- CITY & PRICE

# user chosen destination
print(f"Your chosen destination is {city_flight}.")

# user defined function   plane_cost()
# if/else statement to return the cost of the flight
def plane_cost():
    if city_flight in user_options:
        print(f"The cost of your flight is £{user_options[city_flight]}.")
    else:
        print("Holiday destination not avaibale.")

plane_cost()
result_city = int(user_options[city_flight])     # convert the returned cost as an integer
print()



# HOTEL -- NUMBER OF NIGHTS

# users chosen number of nights stay
print(f"You will be away for {num_nights} nights.")

# price per night
price_per_night = 89
print("The hotel price per night is £89.")

# user defined function   hotel_cost()
# multiply the number of nights with the price per night
def hotel_cost(num_nights, price_per_night):
    """ Multiply the price per night & number of nights """
    total_hotel_cost = num_nights * price_per_night
    return total_hotel_cost

#output of total cost of hotel
result_hotel = hotel_cost(num_nights, price_per_night)
print(f"The total cost of your hotel during your stay is £{result_hotel}.")
print()



# CAR -- NUMBER OF DAYS

# user chosen numbers of days renting a car
print(f"You will rent a car for {rental_days} days.")

# price per day
price_per_day = 42
print("The price per day for car rental is £42.")

# user defined function   car_rental()
# multiply the number of days renting with the price per day to rent
def car_rental(rental_days, price_per_day):
    """ Multiply the price per day & number of days """
    total_rental_cost = rental_days * price_per_day
    return total_rental_cost

#output of total cost of car rental
result_rental = car_rental(rental_days, price_per_day)
print(f"The total cost for renting a car is £{result_rental}.")
print()



# TOTAL -- PRICE OF HOLIDAY

# variable of three result variable combined

# user defined function   holiday_cost()
# using the three result variables made adding the total together
def holiday_cost():
    combined_results = (result_city + result_hotel + result_rental)
    return(combined_results)

total_price = holiday_cost()

# output of total cost of holiday
print(f"The total cost of your holiday is £{total_price}.")
print("HAVE A FUN HOLIDAY, ENJOY!")




