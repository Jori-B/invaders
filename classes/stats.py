class Stats:
    def __init__(self, ship):
        self.ship = ship
        if ship == "lord_nelson":
            self.laser_width = 2
            self.laser_speed = 2
            self.ship_speed = 3
        if ship == "commander_cosmonaut":
            self.laser_width = 4
            self.laser_speed = 1
            self.ship_speed = 2
        if ship == "pointy_boy":
            self.laser_width = 2
            self.laser_speed = 3
            self.ship_speed = 2
        if ship == "donut_warrior":
            self.laser_width = 4
            self.laser_speed = 3
            self.ship_speed = 3