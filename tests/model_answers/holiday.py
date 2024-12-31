print("HOLIDAY TIME 🌴")

# Dict for destinations and their costs

destinations = {
    "london" : (20000, 5000, 2500),
    "johannesburg" : (8000, 950, 425),
    "paris" : (55000, 5000, 3500)
}

def plane_cost(city_flight):
    # Check if the destination exists in the dictionary
    if city_flight in destinations:
        # Retrieve the tuple for the given destination
        destination = destinations[city_flight]

        # Extract the flight cost from the tuple
        flight_cost = destination[0]

        return flight_cost

    else:
        return None

def hotel_cost(city_flight, num_nights):
    # Check if the  exists in the dictionary
    if city_flight in destinations:
        # Retrieve the tuple for the given destination
        destination = destinations[city_flight]

        # Extract the hotel cost from the tuple
        hotel_cost = destination[1]

        # Calculate the total hotel cost
        total_hotel = hotel_cost *num_nights

        return total_hotel

    else:
        return None

def car_rental(city_flight, rental_days):
    # Check if the  exists in the dictionary
    if city_flight in destinations:
        # Retrieve the tuple for the given destination
        destination = destinations[city_flight]

        # Extract the car rental cost from the tuple
        car_rental = destination[2]

        # Calculate the car rental cost
        rental_total = car_rental *rental_days

        return rental_total

    else:
        return None

def holiday_cost(hotel_cost, plane_cost, car_rental):
    while True:
    # Prompt user for destination

        print("Please select a destination:")
        for city in destinations.keys():
            print(city.capitalize())

        # Prompt the user to input a destination
        city_flight = input("Enter the destination >  ").strip().lower()

        # Get flight cost
        flight_cost = plane_cost(city_flight)
        
        if flight_cost:
            print(f"\nThe cost for {city_flight.capitalize()} is R{flight_cost:.2f}")

        else:
            print(f"Destination '{city_flight}' not found in the list.")
            continue

        # Hotel nights
        try:
            # Prompt the user to input a destination
            num_nights = int(input("Enter the number nights you'll be staying >  "))

            # Get flight cost
            total_hotel = hotel_cost(city_flight, num_nights)

            print(f"\nHotel cost for {num_nights} nights is R{total_hotel:.2f}")

        except Exception as ex:
            print(ex, "\nPlease Try Again!")
            continue

        # Car rental
        try:
            # Prompt the user to input a destination
            rental_days = int(input("Enter the number of days for car rental >  "))

            # Get flight cost
            total_rental = car_rental(city_flight, rental_days)

            print(f"\nCar rental cost for {rental_days} days is R{total_rental:.2f}")
            break
        except Exception as ex:
            print(ex, "\nPlease Try Again!")
            continue

    # return Holiday total
    return flight_cost + total_hotel + rental_days

# Call the function
holiday_total = holiday_cost(hotel_cost, plane_cost, car_rental)

# Update user on total holiday cost
print(f"Thank You!\nYour Total Holiday will be  R{holiday_total:.2f}\nHave Fun!")
