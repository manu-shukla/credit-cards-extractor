"""
Pydantic Models for Credit Card Data
-------------------------------------
Matches the TypeScript interface for seamless frontend integration.
"""

from typing import List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class RewardCategory(BaseModel):
    """Reward multipliers by spending category"""
    dining: float = 0
    travel: float = 0
    fuel: float = 0
    grocery: float = 0
    shopping: float = 0
    utilities: float = 0
    entertainment: float = 0
    international: float = 0
    
    @field_validator('*', mode='before')
    @classmethod
    def coerce_to_float(cls, v):
        if v is None or v == "" or v == "N/A":
            return 0.0
        try:
            return float(v)
        except (ValueError, TypeError):
            return 0.0


class Benefit(BaseModel):
    """Individual card benefit"""
    icon: str = Field(..., description="Icon identifier (e.g., 'shield', 'plane', 'gift')")
    title: str = Field(..., description="Benefit title")
    description: str = Field(..., description="Detailed benefit description")


class Milestone(BaseModel):
    """Milestone benefit structure"""
    spend: int = 0
    benefit: str = ""
    value: int = 0
    
    @field_validator('spend', 'value', mode='before')
    @classmethod
    def coerce_to_int(cls, v):
        if v is None or v == "" or v == "N/A":
            return 0
        try:
            return int(float(v))  # Handle "1000.0" strings
        except (ValueError, TypeError):
            return 0


class BestMerchant(BaseModel):
    """Best merchant partner for the card"""
    name: str = Field(..., description="Merchant name")
    logo: str = Field("", description="Logo URL or identifier")
    multiplier: str = Field(..., description="Reward multiplier description")


class CreditCard(BaseModel):
    """
    Comprehensive credit card data model.
    Matches TypeScript interface for frontend integration.
    """
    # Basic Information
    id: str = Field(..., description="Unique identifier for the card")
    name: str = Field(..., description="Official card name")
    bank: str = Field(..., description="Issuing bank name")
    network: str = Field("Unknown", description="Card network: Visa, Mastercard, Amex, Rupay, Diners")
    
    # Fees
    annualFee: int = Field(0, description="Annual maintenance fee in INR")
    joiningFee: int = Field(0, description="One-time joining fee in INR")
    
    # Rewards
    rewardRate: float = Field(0, description="Base reward points per Rs 100")
    rewards: RewardCategory = Field(default_factory=RewardCategory)
    
    # Visual Styling
    color: str = Field("#1a1a1a", description="Primary gradient color (hex)")
    accentColor: str = Field("#00ff00", description="Neon accent for glow effects (hex)")
    gradient: str = Field("", description="CSS gradient string")
    
    # Benefits & Milestones
    benefits: List[Benefit] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    
    # Merchant Partners
    bestMerchants: List[BestMerchant] = Field(default_factory=list)
    
    # Reward Points Details
    rewardPointValue: float = Field(0.25, description="Value of 1 reward point in INR")
    rewardPointsName: Optional[str] = Field(None, description="Custom name for points")
    mostlyUsedFor: List[str] = Field(default_factory=list)
    
    # Optional Card Visual Details
    cardNumber: Optional[str] = Field(None)
    expiryDate: Optional[str] = Field(None)
    cardholderName: Optional[str] = Field(None)
    
    @field_validator('annualFee', 'joiningFee', mode='before')
    @classmethod
    def coerce_fees_to_int(cls, v):
        if v is None or v == "" or v == "N/A":
            return 0
        try:
            return int(float(v))
        except (ValueError, TypeError):
            return 0
    
    @field_validator('rewardRate', 'rewardPointValue', mode='before')
    @classmethod
    def coerce_to_float(cls, v):
        if v is None or v == "" or v == "N/A":
            return 0.0
        try:
            return float(v)
        except (ValueError, TypeError):
            return 0.0


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    GEMINI = "gemini"
    OPENAI = "openai"
