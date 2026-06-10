import csv

def is_admin(user_id) -> bool:
    admin_ids=[]
    with open("data/admins.csv",encoding="utf8") as file:
        for row in csv.DictReader(file,fieldnames=("Name","ID")):
            admin_ids.append(int(row["ID"]))
    return (user_id in admin_ids)