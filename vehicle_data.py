# Vehicle dimensions (length, width) in meters
vehicle_dimensions = {
    # Cars
    "Honda City": (4.55, 1.75),
    "Maruti Swift": (3.86, 1.73),
    "Hyundai i20": (3.99, 1.77),
    "Hyundai Creta": (4.30, 1.79),
    "Kia Seltos": (4.31, 1.80),
    "Toyota Innova": (4.73, 1.83),
    "Toyota Fortuner": (4.79, 1.85),
    "Maruti Baleno": (3.99, 1.74),
    "Tata Nexon": (3.99, 1.81),
    "Mahindra XUV700": (4.70, 1.89),

    # Bikes / Scooters
    "Honda Activa": (1.85, 0.70),
    "TVS Jupiter": (1.84, 0.68),
    "Suzuki Access 125": (1.87, 0.69),
    "Royal Enfield Classic 350": (2.14, 0.84),
    "Royal Enfield Bullet": (2.20, 0.81),
    "Bajaj Pulsar 150": (2.05, 0.79),
    "Yamaha R15": (1.99, 0.72),
    "TVS Apache RTR": (2.08, 0.79),
    "Hero Splendor": (2.00, 0.72),
    "KTM Duke 200": (2.02, 0.83)
}

# Map each model to its vehicle category (used by templates)
vehicle_type_map = {}
_cars = [
    "Honda City", "Maruti Swift", "Hyundai i20", "Hyundai Creta",
    "Kia Seltos", "Toyota Innova", "Toyota Fortuner", "Maruti Baleno",
    "Tata Nexon", "Mahindra XUV700"
]
_bikes = [
    "Honda Activa", "TVS Jupiter", "Suzuki Access 125", "Royal Enfield Classic 350",
    "Royal Enfield Bullet", "Bajaj Pulsar 150", "Yamaha R15", "TVS Apache RTR",
    "Hero Splendor", "KTM Duke 200"
]
for m in _cars:
    vehicle_type_map[m] = 'car'
for m in _bikes:
    vehicle_type_map[m] = 'bike'

