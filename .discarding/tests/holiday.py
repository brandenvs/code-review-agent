# calculate a user’s total holiday cost, which includes the
# plane cost, hotel cost, and car rental cost.

# def hotel_cost(num_nights):
#     # Assume the cost per night is $100
#     price_per_night = 100
#     return num_nights * price_per_night

def flight_cost(city_flight):
# cost for flight to desired city
    if city_flight == "new york":
        return 300
    elif city_flight== "paris":
            return 400
    elif city_flight=="tokyo":
            return 500
    elif city_flight =="cape town":
            return 700
    else: 
            return 0 
                    # no valid city input
def car_rental(car_rental_days):
    # estimate car rental a day = £50
    price_per_day = 50
    return car_rental_days * price_per_day
    
def hotel_night(num_nights):
    # assuming stay per night is £70
    price_per_night = 70
    return num_nights* price_per_night
    
    
    # total cost of holiday

def holiday_cost(city_flight, car_rental_days, num_nights):
        total_flight = (city_flight)
        total_car_fare=(car_rental_days)
        total_hotel_cost = (num_nights)
        return total_flight+total_car_fare+total_hotel_cost

# User input

city_flight = input("name of city you will be flying (new york, tokyo, capetown,paris):")
car_rental_days = int(input("number of days to rent a car:"))
num = int(input("number of nights to stay at hotel"))


# total cost of booking
total_cost = holiday_cost(city_flight, car_rental_days, num_nights)


# result
print (f" the total holiday cost of trip to {city_flight}) is {total_cost}.")


