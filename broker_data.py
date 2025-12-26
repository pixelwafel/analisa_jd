# broker_data.py
# Referensi 34 Broker Kurasi berdasarkan target_broker.txt 

BROKER_CATEGORIES = [
    {
        "name": "The Foreign Whales 🌊",
        "desc": "Broker asing utama penentu arah Smart Money & Foreign Flow[cite: 1, 10, 12].",
        "codes": ["AK", "BK", "BQ", "DP", "DR", "KZ", "RX", "TP", "YU", "ZP", "AG"] # [cite: 9, 10, 12, 13, 14, 18, 22, 23, 24, 25]
    },
    {
        "name": "The Local Giants 🚀",
        "desc": "Market movers lokal dan penggerak saham lapis dua/tiga[cite: 3, 18].",
        "codes": ["MG", "CP", "AZ", "GR", "LG", "KI", "YB", "YJ"] # [cite: 10, 13, 15, 17, 18, 24]
    },
    {
        "name": "Institutional Support 🛡️",
        "desc": "Investor jangka panjang, institusi pemerintah, dan penjaga grup[cite: 6, 19].",
        "codes": ["CC", "DX", "NI", "OD", "SQ", "DH", "IF"] # [cite: 12, 13, 14, 16, 19, 22]
    },
    {
        "name": "The Retail Crowd 👥",
        "desc": "Indikator partisipasi investor ritel massal[cite: 5, 20, 24].",
        "codes": ["YP", "PD", "XC", "XL", "KK", "EP", "HP", "BB"] # [cite: 11, 14, 16, 17, 20, 23, 24]
    }
]