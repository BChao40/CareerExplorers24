questions = [
    {
        "level": 1,
        "type": "stock_price",
        "ticker": "MSFT",
        "question": "What is the current price of {ticker}'s stock?",
        "explanation": "Choice 1",
        "answers": [
            {"text": "${price} (correct)", "correct": True},
            {"text": "${price} + some operations", "correct": False},
            {"text": "${price} + other operations", "correct": False}
        ]
    },
    {
        "level": 2,
        "type": "true_false",
        "question": "True or False?",
        "explanation": "True",
        "answers": [
            {"text": "True", "correct": True},
            {"text": "False", "correct": False}
        ]
    },
    {
        "level": 3,
        "type": "multiple_choice",
        "question": "Which number is less than 2?",
        "explanation": "1 is less than 2.",
        "answers": [
            {"text": "1", "correct": True},
            {"text": "2", "correct": False},
            {"text": "3", "correct": False},
            {"text": "4", "correct": False}
        ]
    },
    {
        "level": 4,
        "type": "text",
        "explanation": "The quick brown fox jumps over the lazy dog",
        "question": "Type an answer!",
        "answers": []
    }
]