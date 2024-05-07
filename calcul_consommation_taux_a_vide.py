class Camion:
    def __init__(self, type_camion, consommation_par_km):
        self.type_camion = type_camion
        self.consommation_par_km = consommation_par_km
        self.distance_parcourue_vide = 0
        self.distance_totale_parcourue = 0

    def realiser_prestation(self, distance):
        self.distance_totale_parcourue += distance
        return distance * self.consommation_par_km  # Retourne la consommation de carburant pour cette prestation

    def retourner_base(self, distance):
        self.distance_parcourue_vide += distance
        self.distance_totale_parcourue += distance
        return distance * self.consommation_par_km  # Retourne la consommation de carburant pour le retour

    def calcul_taux_voyage_a_vide(self):
        # Calcule le taux de voyage à vide par rapport à la distance totale parcourue
        if self.distance_totale_parcourue == 0:
            return 0
        return (self.distance_parcourue_vide / self.distance_totale_parcourue) * 100


def simulation_prestations(prestations, consommation_par_km, capacite_carburant):
    camions = [Camion('Type A', consommation_par_km) for _ in range(prestations[0]['nombre_camions'])]
    carburant_total = capacite_carburant * len(camions)
    consommation_totale = 0

    for prestation in prestations:
        if prestation['type_camion'] == 'Type A':
            for camion in camions:
                # Réaliser la prestation si assez de carburant
                if carburant_total >= camion.realiser_prestation(prestation['distance']):
                    consommation = camion.realiser_prestation(prestation['distance'])
                    consommation_totale += consommation
                    carburant_total -= consommation
                else:
                    # Retourner à la base si pas assez de carburant
                    consommation = camion.retourner_base(prestation['distance'])
                    consommation_totale += consommation
                    carburant_total -= consommation
                    carburant_total += capacite_carburant  # Simuler le ravitaillement
        else:
            print("Type de camion non disponible pour la prestation")

    taux_voyage_a_vide = sum(camion.calcul_taux_voyage_a_vide() for camion in camions) / len(camions)
    return consommation_totale, taux_voyage_a_vide


# Exemple de simulation avec des prestations
prestations = [
    {'type_camion': 'Type A', 'distance': 100, 'nombre_camions': 2},
    {'type_camion': 'Type A', 'distance': 150, 'nombre_camions': 2},
    {'type_camion': 'Type A', 'distance': 50, 'nombre_camions': 2}
]

consommation_par_km = 0.3  # Litres par km pour le Type A
capacite_carburant = 300   # Capacité en carburant pour chaque camion de Type A

consommation, taux_vide = simulation_prestations(prestations, consommation_par_km, capacite_carburant)
print(f"Consommation totale de carburant : {consommation} litres.")
print(f"Taux de voyage à vide : {taux_vide:.2f}%.")
