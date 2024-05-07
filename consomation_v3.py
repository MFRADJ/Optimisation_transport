# Mise à jour de la simulation pour gérer des prestations consécutives et calculer les trajets à vide et la consommation de carburant

class Camion:
    def __init__(self, type_camion, consommation_par_km, capacite_carburant):
        self.type_camion = type_camion
        self.consommation_par_km = consommation_par_km
        self.carburant_restant = capacite_carburant
        self.distance_parcourue_vide = 0
        self.distance_parcourue_charge = 0

    def effectuer_prestation(self, distance):
        consommation = distance * self.consommation_par_km
        if consommation <= self.carburant_restant:
            self.carburant_restant -= consommation
            self.distance_parcourue_charge += distance
            return consommation
        else:
            return None  # Carburant insuffisant pour la prestation

    def retourner_a_base(self, distance_base):
        consommation = distance_base * self.consommation_par_km
        if consommation <= self.carburant_restant:
            # Retour à la base pour le ravitaillement
            self.carburant_restant -= consommation
            self.distance_parcourue_vide += distance_base
            return distance_base  # Enregistre la distance de voyage à vide
        else:
            return None  # Carburant insuffisant pour retourner à la base

    def ravitailler(self):
        self.carburant_restant = self.capacite_carburant  # Ravitaillement du camion

    def taux_voyage_vide(self):
        total_distance = self.distance_parcourue_vide + self.distance_parcourue_charge
        return (self.distance_parcourue_vide / total_distance) * 100 if total_distance > 0 else 0


# Fonction pour simuler les prestations et calculer les voyages à vide et la consommation de carburant
def simulation_prestations(prestations, consommation_par_km, capacite_carburant, distance_base):
    camion = Camion('Type A', consommation_par_km, capacite_carburant)
    consommation_prestations = []
    kilometrage_vide_prestations = []

    for prestation in prestations:
        consommation = camion.effectuer_prestation(prestation['distance'])
        if consommation is not None:
            consommation_prestations.append(consommation)
        else:
            distance_vide = camion.retourner_a_base(distance_base)
            if distance_vide is not None:
                camion.ravitailler()
                consommation = camion.effectuer_prestation(prestation['distance'])
                consommation_prestations.append(consommation)
                kilometrage_vide_prestations.append(distance_vide)
            else:
                print("Le camion n'a pas assez de carburant pour retourner à la base ou réaliser la prestation.")
                break

    consommation_totale = sum(consommation_prestations)
    distance_totale_parcourue = sum(kilometrage_vide_prestations) + camion.distance_parcourue_charge
    taux_voyage_vide = camion.taux_voyage_vide()

    return consommation_prestations, kilometrage_vide_prestations, consommation_totale, taux_voyage_vide, distance_totale_parcourue


# Exemple de prestations
prestations = [
    {'type_camion': 'Type A', 'distance': 100},
    {'type_camion': 'Type A', 'distance': 150},
    {'type_camion': 'Type A', 'distance': 50}
]

# Constantes
CONSUMPTION_PER_KM = 0.3  # Consommation de carburant par km
FUEL_CAPACITY = 300  # Capacité de carburant du camion
DISTANCE_TO_BASE = 100  # Distance de la prestation à la base pour le ravitaillement

# Exécution de la simulation
fuel_consumption_per_prestation, empty_travel_per_prestation, total_fuel_consumption, empty_travel_rate, total_distance_travelled = simulation_prestations(prestations, CONSUMPTION_PER_KM, FUEL_CAPACITY, DISTANCE_TO_BASE)
print(simulation_prestations(prestations, CONSUMPTION_PER_KM, FUEL_CAPACITY, DISTANCE_TO_BASE))
