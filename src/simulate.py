import pandas as pd
import numpy as np
from faker import Faker
import random
import os

# set up a fake friend to help us with daes and randomness
fake = Faker()

# generate a bunch of users with all the vibes (region, device, and age)
def generate_users(n=1000):
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
    devices = ['Mobile', 'Desktop', 'Tablet']

    users = []
    for i in range(n):
        users.append({
            'user_id': i + 1,
            'age': random.randint(18,65), # because most adds don't care about toddlers and your grandma - sad
            'region': random.choice(regions),
            'device': random.choice(devices)
        })

    return pd.DataFrame(users)

# genarate fake ad campaigns with some strategy and cash to burn
def generate_campaigns():
    return pd.DataFrame([
        {'campaign_id': i + 1,
         'campaign_name': f'Campaign_{i + 1}',
         'bid_strategy': random.choice(['Maximize Clicks', 'Target CPA', 'Manual CPC']),
         'daily_budget': random.randint(100, 1000) # not Google-level budgets, but enough to pretend
        }
        for i in range(5) # let's not get carried away - 5 campaigns should do it
    ])

# this is where the magic happens - simulating ad impressions with a sprinkle of click + conversion spice
def generate_interactions(users_df, campaigns_df, n= 10000):
    interactions = []
    for _ in range(n):
        user = users_df.sample(1).iloc[0] # spin the wheel, pick a user 
        campaign = campaigns_df.sample(1).iloc[0] # spin again, now with ads
        clicked = np.random.binomial(1, 0.1) #10% base CTR - not bad, not unrealistic
        converted = np.random.binomial(1, 0.05 if clicked else 0.005) # if they click, they are more likely to buy(obviously)

        interactions.append({
            'user_id': user['user_id'],
            'campaign_id': campaign['campaign_id'],
            'timestamp': fake.date_time_between(start_date='-7d', end_date='now'),
            'clicked': clicked,
            'converted': converted,
            'region': user['region'],
            'device': user['device']
        })
    return pd.DataFrame(interactions)


# save all the chaos into clean CSVs for later analysis
def stimulate_all():
    users = generate_users()
    campaigns = generate_campaigns()
    interactions = generate_interactions(users, campaigns)

    # make sure the folder exists (tried debuging for minutes because the folder didn't exist( spelled processed as pressed smh) - don't be like me)
    os.makedirs('data/processed', exist_ok=True)

    # save it like a responsible data human
    users.to_csv('data/processed/users.csv', index=False)
    campaigns.to_csv('data/processed/campaigns.csv', index=False)
    interactions.to_csv('data/processed/interactions.csv', index=False)

    print("Simulation Complete. Files saved in data/processed/")

# let it all come together now 
if __name__ == "__main__":
    stimulate_all()
