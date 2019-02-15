import argparse

class Reservations:
    def __init__(self, filename):
        self._reservations = []
        with open(filename) as _f:
            for res_id, reservation in enumerate(_f):
                name, number = reservation.strip().split(",")
                if not name:
                    name = "UNKNOWN"
                try:
                    int(number)
                except ValueError:
                    number = str(25)
                self._reservations.append((str(res_id), name, number))

    def calculate_chairs_per_person(self, num_chairs):
        chairs = []
        for res_id, name, number in self._reservations:
            try:
                chairs.append(num_chairs / int(number))
            except ZeroDivisionError:
                # Assume that 0 guests in reality means 1 guest
                chairs.append(num_chairs)
        
        self._chairs_per_person = chairs
        return chairs

    def dangerous_reservations(self):
        low_chair_warnings = []
        for reservation, avg_chairs in zip(self._reservations, self._chairs_per_person):
            if avg_chairs < 1.05:
                low_chair_warnings.append(reservation[0])

        self._dangerous_chairs = low_chair_warnings
        return low_chair_warnings

    def generate_chair_warnings(self):
        for (res_id, name, number), chairs in zip(self._reservations, self._chairs_per_person):
            if res_id in self._dangerous_chairs:
                print("Low-chair warning for {}, only {} chairs per person for reservation {}".format(name, chairs, res_id))

    @property
    def reservations(self):
        return self._reservations

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--warn', action='store_true')
    parser.add_argument('--average', action='store_true')
    options = parser.parse_args()

    reservations = Reservations("reservations")

    chairs_per_person = reservations.calculate_chairs_per_person(50)
    reservations.dangerous_reservations()

    if options.warn:
        reservations.generate_chair_warnings()

    if options.average:
        average = sum(chairs_per_person) / len(chairs_per_person)
        print("The average chairs per person is {}".format(average))
    if not options.warn and not options.average:
        for reservation in reservations.reservations:
            print("\t".join(reservation))

if __name__ == "__main__":
    main()
