class SmartTrafficLight:
    def __init__(self, *streets):
        self.streets = {street: car_count for car_count, street in streets}
        self.road_traffic_equal = False

    def turngreen(self):
        if self.road_traffic_equal:
            return None

        priority = max(self.streets, key=lambda k: self.streets[k])
        traffic = self.streets[priority]

        if all(traffic == count for count in self.streets.values()):
            self.road_traffic_equal = True
            return None
        else:
            self.streets[priority] = 0
            return priority
