"""Models package: Pydantic schemas for request/response validation."""
from __future__ import annotations

from models.accommodation import (
    AccommodationCreate,
    AccommodationResponse,
)
from models.activity import ActivityCreate, ActivityResponse
from models.budget import BudgetPlanCreate, BudgetPlanResponse
from models.category import CategoryBase, CategoryResponse
from models.destination import (
    DestinationCreate,
    DestinationResponse,
    DestinationUpdate,
)
from models.festival import FestivalCreate, FestivalResponse
from models.itinerary import ItineraryCreate, ItineraryResponse
from models.itinerary_stop import ItineraryStopCreate, ItineraryStopResponse
from models.restaurant import RestaurantCreate, RestaurantResponse
from models.review import ReviewCreate, ReviewResponse
from models.season import SeasonBase, SeasonResponse
from models.tag import TagBase, TagResponse
from models.transport import TransportCreate, TransportResponse
from models.user import UserCreate, UserResponse, UserUpdate

__all__ = [
    # accommodation
    "AccommodationCreate",
    "AccommodationResponse",
    # activity
    "ActivityCreate",
    "ActivityResponse",
    # budget
    "BudgetPlanCreate",
    "BudgetPlanResponse",
    # category
    "CategoryBase",
    "CategoryResponse",
    # destination
    "DestinationCreate",
    "DestinationResponse",
    "DestinationUpdate",
    # festival
    "FestivalCreate",
    "FestivalResponse",
    # itinerary
    "ItineraryCreate",
    "ItineraryResponse",
    # itinerary stop
    "ItineraryStopCreate",
    "ItineraryStopResponse",
    # restaurant
    "RestaurantCreate",
    "RestaurantResponse",
    # review
    "ReviewCreate",
    "ReviewResponse",
    # season
    "SeasonBase",
    "SeasonResponse",
    # tag
    "TagBase",
    "TagResponse",
    # transport
    "TransportCreate",
    "TransportResponse",
    # user
    "UserCreate",
    "UserResponse",
    "UserUpdate",
]
