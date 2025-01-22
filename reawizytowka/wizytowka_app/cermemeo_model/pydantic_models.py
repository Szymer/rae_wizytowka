from typing import List, Optional
from pydantic import BaseModel

from pydantic import BaseModel, EmailStr, Field, field_validator

"""_summary_
    Klasa zawierająca modele danych dla aplikacji cermemeo.
    mozna wykorzystac do walidacji danych wejsciowych do API 
    w tym projrkcie troche na wyrost ale mozna to wykorzystac
"""
class Comment(BaseModel):
    text: str


class LeadModel(BaseModel):
    campaign_token: str = Field(..., description="Wymagany token kampanii")
    phone: str = Field(..., pattern=r"^\+\d{11}$", description="Numer telefonu w formacie +48500100100")
    email: Optional[EmailStr] = Field(None, description="Adres email użytkownika")
    external_id: Optional[str] = Field(None, description="ID w systemie partnera")
    ip: Optional[str] = Field(None, description="Adres IP")
    creator_id: Optional[str] = Field(None, description="ID użytkownika, który tworzy leada")
    trader_id: Optional[str] = Field(None, description="ID użytkownika, do którego będzie przypisany lead")
    name: Optional[str] = Field(None, description="Imię")
    surname: Optional[str] = Field(None, description="Nazwisko")
    pesel: Optional[str] = Field(None, pattern=r"^\d{11}$", description="Numer PESEL")
    id_card: Optional[str] = Field(None, description="Numer dowodu osobistego")
    account: Optional[str] = Field(None, pattern=r"^\d{26}$", description="Numer konta bankowego")
    address_region: Optional[str] = Field(None, check_fields=False, description="Nazwa województwa zgodna ze słownikiem")
    address_city: Optional[str] = Field(None, description="Miejsce zamieszkania")
    address_street: Optional[str] = Field(None, description="Ulica")
    address_building: Optional[str] = Field(None, description="Numer budynku")
    address_flat: Optional[str] = Field(None, description="Numer mieszkania")
    address_postcode: Optional[str] = Field(None, pattern=r"^\d{2}-\d{3}$", description="Kod pocztowy")
    correspondence_region: Optional[str] = Field(None, description="Nazwa województwa zgodna ze słownikiem")
    correspondence_city: Optional[str] = Field(None, description="Miejsce zamieszkania do korespondencji")
    correspondence_street: Optional[str] = Field(None, description="Ulica do korespondencji")
    correspondence_building: Optional[str] = Field(None, description="Numer budynku do korespondencji")
    correspondence_flat: Optional[str] = Field(None, description="Numer mieszkania do korespondencji")
    correspondence_postcode: Optional[str] = Field(None, pattern=r"^\d{2}-\d{3}$", description="Korespondencyjny kod pocztowy")
    comments: Optional[List[Comment]] = Field(None, description="Lista komentarzy")

    @field_validator("adress_region", check_fields=False)
    def validate_adress_region(cls, value) :
        if value not in ["dolnośląskie", "kujawsko-pomorskie", "lubelskie", "lubuskie", "łódzkie", "małopolskie", "mazowieckie", "opolskie", "podkarpackie", "podlaskie", "pomorskie", "śląskie", "świętokrzyskie", "warmińsko-mazurskie", "wielkopolskie", "zachodniopomorskie"]:
            raise ValueError("Niepoprawna nazwa województwa")
        return value
    
    @field_validator("phone")
    def validate_phone(cls, value):
        if value[:3] != "+48":
            raise ValueError("Numer telefonu powinien zaczynać się od +48")
        
        return value