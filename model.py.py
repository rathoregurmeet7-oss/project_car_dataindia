import os

def predict_car_model(image_path):
    fname = os.path.basename(image_path).lower()
    keywords = {
        "civic": "Civic",
        "swift": "Swift",
        "corolla": "Corolla",
        "city": "City",
        "creta": "Creta",
        "thar": "Thar",
        "fortuner": "Fortuner",
        "harrier": "Harrier",
        "model3": "Model 3", "model_3": "Model 3",
        "amaze": "Amaze",
        "baleno": "Baleno",
        "i10": "Grand i10", "grand_i10": "Grand i10", "grand-i10": "Grand i10",
        "altroz": "Altroz",
        "wagonr": "Wagon R", "wagon_r": "Wagon R", "wagon-r": "Wagon R",
        "verna": "Verna",
        "dzire": "Dzire",
        "venue": "Venue",
        "seltos": "Seltos",
        "innova": "Innova",
        "brezza": "Brezza",
        "magnite": "Magnite",
        "tiago": "Tiago",
        "alto": "Alto",
        "scorpio": "Scorpio N", "scorpio_n": "Scorpio N",
        "xuv700": "XUV700",
        "nexon": "Nexon",
        "punch": "Punch",
        "fronx": "FRONX", "fronz": "FRONX",
        "ertiga": "Ertiga",
        "defender": "Defender",
        "sonet": "Sonet",
        "jimny": "Jimny",
        "hector": "Hector",
        "elevate": "Elevate",
        "comet": "Comet EV", "comet_ev": "Comet EV",
        "e2o": "Mahindra e2o", "mahindra_e2o": "Mahindra e2o",
        "tigor": "Tigor",
        "bolero": "Bolero",
        "glanza": "Glanza",
        "ignis": "Ignis",
        "redigo": "Redi-GO", "redi_go": "Redi-GO", "redi-go": "Redi-GO",
        "kwid": "Kwid",
        "zest": "Zest"
    }

    for key, model in keywords.items():
        if key in fname:
            return model
    return None
