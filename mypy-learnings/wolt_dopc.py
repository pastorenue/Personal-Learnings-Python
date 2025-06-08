##################
# model.py
##################
from dataclasses import dataclass


@dataclass
class DeliveryModel:
    fee: int
    distance: int


@dataclass
class DOPCResponseModel:
    total_price: int
    small_order_surcharge: int
    cart_value: int
    delivery: DeliveryModel

    def serialize(self):
        """
        Returns a dictionary representation of the model.
        """
        return {
            "total_price": self.total_price,
            "small_order_surcharge": self.small_order_surcharge,
            "cart_value": self.cart_value,
            "delivery": {
                "fee": self.delivery.fee,
                "distance": self.delivery.distance
            }
        }


##################
# client.py
##################
import requests


class HomeAPIClient:
    def __init__(self, base_url: str, venue_slug: str):
        self.venue_slug = venue_slug
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_static(self):
        url = f"{self.base_url}/{self.venue_slug}/static"
        response = self.session.get(url)
        return response.json()
    
    def get_dynamic(self):
        url = f"{self.base_url}/{self.venue_slug}/dynamic"
        response = self.session.get(url)
        return response.json()


##################
# service.py
##################

import math
from functools import cached_property

class InvalidQueryParamsError(Exception):
    pass


class ImpossibleDeliveryError(Exception):
    pass


BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"


class DOPCService:
    """
    Delivery Order Price Calculator Service
    """
    def __init__(self, hapi_client: HomeAPIClient, query_params: dict) -> None:
        """
        Initialize the service with the HomeAPIClient and the query parameters
        
        Args:
            hapi_client: HomeAPIClient
            query_params: dict
        """
        self.__query_params = query_params # This is private
        self.hapi_client = hapi_client
    
    @property
    def venue_slug(self) -> str:
        try:
            return self.__query_params["venue_slug"]
        except KeyError:
            raise InvalidQueryParamsError("venue_slug is required")

    @property
    def cart_value(self) -> int:
        try:
            return int(self.__query_params["cart_value"])
        except KeyError:
            raise InvalidQueryParamsError("cart_value is required")
    
    @property
    def user_lon(self) -> float:
        try:
            return float(self.__query_params["user_lon"])
        except KeyError:
            raise InvalidQueryParamsError("user_lon is required")
    
    @property
    def user_lat(self) -> float:
        try:
            return float(self.__query_params["user_lat"])
        except KeyError:
            raise InvalidQueryParamsError("user_lat is required")

    @cached_property
    def _get_home_api_data(self):
        """
        Returns the relevant data needed from the Home API
        """
        static = self.hapi_client.get_static()
        dynamic = self.hapi_client.get_dynamic()

        res: dict = {}
        static_raw = static["venue_raw"]
        dynamic_raw = dynamic["venue_raw"]
        res["coord"] = static_raw["location"]["coordinates"] # I am 100% that this will always be present
        res["min_surcharge"] = dynamic_raw["delivery_specs"]["order_minimum_no_surcharge"]
        res["base_price"] = dynamic_raw["delivery_specs"]["delivery_pricing"]["base_price"]
        res["distance_ranges"] = dynamic_raw["delivery_specs"]["delivery_pricing"]["distance_ranges"]

        return res
    
    def params_is_valid(self) -> bool:
        return all([
            self.cart_value,
            self.venue_slug,
            self.user_lat,
            self.user_lon
        ])
    
    def get_delivery_distance(self) -> int:
        """
        Returns the coordinate difference between the user and the venue
        Using distance of two points formula
        d = √((x2 – x1)² + (y2 – y1)²)
        """
        user_lon = self.user_lon
        user_lat = self.user_lat
        venue_lon, venue_lat = self._get_home_api_data["coord"]
       
        d = math.sqrt((venue_lon - user_lon)**2 + (venue_lat - user_lat)**2)
        return math.floor(d)
    
    def get_small_order_surcharge(self) -> int:
        return abs(self.cart_value - self._get_home_api_data["min_surcharge"])
    
    def get_delivery_fee(self) -> int:
        """Get the delivery price"""
        distance_ranges = self._get_home_api_data["distance_ranges"]
        distance = self.get_delivery_distance()
        actual_range = list(filter(lambda x: x["min"] <= distance and x["max"] > distance, distance_ranges))
        if not actual_range:
            raise ImpossibleDeliveryError("Distance too long.")
        
        # Expecting the actual range to be len of 1
        d_range = actual_range[0]
        base_price = self._get_home_api_data["base_price"]
        return (base_price + int(d_range["a"])) + math.floor(int(d_range["b"]) * distance / 10)
    
    def get_total_price(self) -> int:
        return self.cart_value + self.get_delivery_fee() + self.get_small_order_surcharge()
    
    def serialize_model(self) -> dict:
        return DOPCResponseModel(
            total_price=self.get_total_price(),
            small_order_surcharge=self.get_small_order_surcharge(),
            cart_value=self.cart_value,
            delivery=DeliveryModel(
                fee=self.get_delivery_fee(),
                distance=self.get_delivery_distance()
            )
        ).serialize()


###################
# v1/routes.py
###################

from flask import Blueprint, request, jsonify

# delivery_bp
delivery_bp = Blueprint("deliver_bp", __name__)

@delivery_bp.route("/delivery-order-price", methods=["GET"])
def delivery_order_price():
    query_params = request.args
    try:
        home_api = HomeAPIClient(BASE_URL, query_params["venue_slug"])
        dopc = DOPCService(hapi_client=home_api, query_params=query_params)
        dopc_model = dopc.serialize_model()
    except ImpossibleDeliveryError as e:
        return {"error": str(e)}, 400
    
    return jsonify(dopc_model), 200


##################
# v1/__init__.py
##################

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api_v1.register_blueprint(delivery_bp)


##################
# app.py
##################

from flask import Flask, Blueprint
# from v1.routes import api_v1

bp = Blueprint("api", __name__, url_prefix="/api/v1/")

app = Flask(__name__)

app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=False)


# Sample requests:
# curl http://localhost:5000/api/v1/delivery-order-price\?venue_slug\=home-assignment-venue-berlin\&cart_value\=1000\&user_lat\=60.17094\&user_lon\=24.93087
# http://localhost:5000/api/v1/delivery-order-price\?venue_slug\=home-assignment-venue-tokyo\&cart_value\=1000\&user_lat\=67094\&user_lon\=93087