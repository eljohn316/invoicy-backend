from datetime import datetime

invoices: list[dict] = [
    {
        "id": "5a0879b259664193bd0a2d1bdbc31cba",
        "created_at": datetime(2021, 8, 18, 7, 48, 32),
        "payment_due": datetime(2021, 8, 19),
        "description": "Re-branding",
        "payment_terms": 1,
        "client_name": "Jensen Huang",
        "client_email": "jensenh@mail.com",
        "status": "paid",
        "sender_address": {
            "street": "19 Union Terrace",
            "city": "London",
            "post_code": "E1 3EZ",
            "country": "United Kingdom",
        },
        "client_address": {
            "street": "106 Kendell Street",
            "city": "Sharrington",
            "post_code": "NR24 5WQ",
            "country": "United Kingdom",
        },
        "items": [
            {
                "name": "Brand Guidelines",
                "quantity": 1,
                "price": 1800.90,
            }
        ],
    },
    {
        "id": "7e94ca039c0046c78192a96b74329d23",
        "created_at": datetime(2021, 8, 21),
        "payment_due": datetime(2021, 9, 20),
        "description": "Graphic Design",
        "payment_terms": 30,
        "client_name": "Alex Grim",
        "client_email": "alexgrim@mail.com",
        "status": "pending",
        "sender_address": {
            "street": "19 Union Terrace",
            "city": "London",
            "post_code": "E1 3EZ",
            "country": "United Kingdom",
        },
        "client_address": {
            "street": "84 Church Way",
            "city": "Bradford",
            "post_code": "BD1 9PB",
            "country": "United Kingdom",
        },
        "items": [
            {"name": "Banner Design", "quantity": 1, "price": 156.00, "total": 156.00},
            {"name": "Email Design", "quantity": 2, "price": 200.00, "total": 400.00},
        ],
        "total": 556.00,
    },
]
