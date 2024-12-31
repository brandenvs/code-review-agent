def hotel_cost(num_nights):
    """Multiplies the number of nights by 1000

    Params:
        num_nights Int: The number of nights 

    Returns:
        Int: The hotel cost
    """
    cost = num_nights * 1000
    return cost


# This is the function plane_cost, multiplying city_flight by cost per flight
def plane_cost(city_flight):
    if city_flight.lower() == "cape town":
        return 1000
    
    elif city_flight.lower() == "johannesburg":
        return 2000
   
    elif city_flight.lower() == "durban":
        return 3000
    
    elif city_flight.lower() == "east london":
        return 4000
    
    elif city_flight.lower() == "pietermaritzburg":
        return 5000

# This is the function of car rental, multiplying rental days by cost for a day to rent a car.
def car_cost(rental_days):
    cost2 = rental_days * 500
    return cost2


# This is the function of holiday cost including the three arguments hotel cost, plane cost and rental cost and returning cost
def holiday_cost(city, nights, rental):
    # Get the required costs 
    nights = hotel_cost(nights)
    city = plane_cost(city)
    rental = car_cost(rental)

    total = nights + city + rental
    return total


# Asking the user to enter amount that they are paying for the city they're selected 
city = input("Enter the city you wish to fly to.\n"
             "(Select one of the following options):\n"
             "Cape Town,\n"
             "Johannesburg,\n"
             "East London,\n"
             "Durban,\n"
             "Pietermaritzburg\n"
             ": ")


# Asking the user to enter the number of nights they'll be staying at the hotel
nights = int(input("Enter the number of nights" 
                   " you'll be staying at the hotel: "))  

# Asking the user to enter the number of days renting a car
rental = int(input("Enter the number of days renting a car: "))


# Getting the total cost
total_cost = holiday_cost(city, nights, rental)
print(f"Total holiday cost: R{total_cost}")

