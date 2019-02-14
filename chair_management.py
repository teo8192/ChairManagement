import argparse

def calculate_chairs_per_person(num_chairs, reservations):
    chairs = []
    for res_id, name, number in reservations:
        try:
            chairs.append(num_chairs / int(number))
        except ZeroDivisionError:
            # Assume that 0 guests in reality means 1 guest
            chairs.append(num_chairs)
    return chairs

def read_reservations(filename):
    reservations = []
    with open(filename) as f:
        for res_id, reservation in enumerate(f):
            name, number = reservation.strip().split(",")
            if not name:
                name = "UNKNOWN"
            try:
                int(number)
            except ValueError:
                number = str(25)
            reservations.append((str(res_id),name,number))
    return reservations

def get_dangerous_reservations(reservations, chairs):
    low_chair_warnings = []
    for reservation, avg_chairs in zip(reservations, chairs):
        if avg_chairs < 1.05:
            low_chair_warnings.append(reservation[0])
    return low_chair_warnings

def generate_chair_warnings(reservations, low_chairs, chairs):
    for (res_id, name, number), chairs in zip(reservations, chairs):
        if res_id in low_chairs:
            print("Low-chair warning for {}, only {} chairs per person for reservation {}".format(name, chairs, res_id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--warn', action='store_true')
    parser.add_argument('--average', action='store_true')
    options = parser.parse_args()

    reservations = read_reservations("reservations")
    chairs_per_person = calculate_chairs_per_person(50, reservations)
    low_chairs = get_dangerous_reservations(reservations, chairs_per_person)
    if options.warn:
        generate_chair_warnings(reservations, low_chairs, chairs_per_person)
    if options.average:
        average = sum(chairs_per_person) / len(chairs_per_person)
        print("The average chairs per person is {}".format(average))
    if not options.warn and not options.average:
        for reservation in reservations:
            print("\t".join(reservation))
