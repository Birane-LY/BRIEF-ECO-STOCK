from django.db import models

class WareHouseStatus(str, models.Choices):
    ACTIVE = "active", "Actif"
    INACTIVE = "inactive", "Inactif"
    SUSPENDED = "suspended", "Suspendu"

class ProductStatus(str, models.Choices):
    DISPONIBLE = "disponible", "Disponible"
    RESERVED = "reserved", "Réservé"
    EXPIRATION = "expiration", "Périmée / Date de Durabilité Minimale en approche"
    INDISPONIBLE = "indisponible", "Indisponible" 

class OrderStatus(str, models.Choices):
    IN_PROGRESS = "IN_PROGRESS", "En cours / Réservé"
    COMPLETED = "COMPLETED", "Terminé / Livré"
    CANCELLED = "CANCELLED", "Annulé"
