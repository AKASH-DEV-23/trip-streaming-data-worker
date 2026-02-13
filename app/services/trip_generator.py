import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# ---------- Master Data (Extended) ----------
US_LOCATIONS = [
    ("Chicago", "IL"), ("Naperville", "IL"), ("Elgin", "IL"),
    ("Joliet", "IL"), ("Rockford", "IL"),
    ("Indianapolis", "IN"), ("Fort Wayne", "IN"),
    ("Cincinnati", "OH"), ("Columbus", "OH"), ("Cleveland", "OH"),
    ("Madison", "WI"), ("Green Bay", "WI"), ("Milwaukee", "WI"),
    ("Detroit", "MI"), ("Grand Rapids", "MI"),
    ("St. Louis", "MO"), ("Kansas City", "MO"),
    ("Minneapolis", "MN"), ("Saint Paul", "MN")
]

CUSTOMERS = [
    "Walmart", "Amazon", "Target", "Costco",
    "HomeDepot", "PepsiCo", "FedEx", "UPS",
    "CocaCola", "Nike", "Ford", "GM",
    "DHL", "BestBuy", "Kroger", "Walgreens"
]

TRIP_TYPES = [
    "Domestic", "International", "Interstate",
    "Dedicated", "Express", "Refrigerated",
    "Hazmat", "Bulk", "Container"
]

# ---------- Random Integer TripID ----------
def random_trip_id():
    return random.randint(1_000_000, 99_999_999)  # 7–8 digit integer


# ---------- Trip Generator ----------
def generate_trip():
    ship_days = random.randint(1, 12)

    ship_date = fake.date_between(start_date="-60d", end_date="today")
    delivery_date = ship_date + timedelta(days=ship_days)

    origin_city, origin_state = random.choice(US_LOCATIONS)
    dest_city, dest_state = random.choice(US_LOCATIONS)

    total_miles = random.randint(150, 1800)
    loaded_miles = int(total_miles * random.uniform(0.65, 0.98))

    shipping_cost = round(random.uniform(1500, 9500), 2)
    revenue = round(shipping_cost * random.uniform(1.15, 1.9), 2)

    capacity = random.randint(40, 100)
    checkpoints = random.randint(1, 12)

    profit = round(revenue - shipping_cost, 2)
    revenue_miles = round(revenue / total_miles, 6)
    profit_miles = round(profit / total_miles, 6)

    return {
        "TripID": random_trip_id(),
        "ShipperID": random.randint(1, 20),
        "CategoryID": random.randint(1, 12),
        "Customer": random.choice(CUSTOMERS),

        "ShipDate": ship_date.isoformat(),
        "OriginCity": origin_city,
        "OriginState": origin_state,
        "ShipDays": ship_days,

        "DestinationCity": dest_city,
        "DestinationState": dest_state,
        "DeliveryDate": delivery_date.isoformat(),

        "TotalMiles": total_miles,
        "LoadedMiles": loaded_miles,
        "ShippingCost": shipping_cost,
        "Revenue": revenue,
        "Capacity": capacity,
        "TripType": random.choice(TRIP_TYPES),
        "CheckPoints": checkpoints,
        "Profit": profit,
        "Revenue Miles": revenue_miles,
        "Profit miles": profit_miles,

        # Recommended for streaming analytics
        "EventTime": datetime.utcnow().isoformat()
    }
