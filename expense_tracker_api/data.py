expenses = [
    {
        "id": 1,
        "title": "Lunch",
        "amount": 250,
        "category": "food"
    },
    {
        "id": 2,
        "title": "Uber",
        "amount": 180,
        "category": "transport"
    }
]

ids = [1, 2]

def d(array):
    for ele in array:
        for expense in expenses:
            if expense["id"] == ele:
                print(expense)

d(ids)
