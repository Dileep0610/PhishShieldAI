import joblib

def inspect():
    rt_mappings = joblib.load("models/verified_rt_lookup_mappings.pkl")
    sub_map = rt_mappings["mappings"]["SubdomainLevelRT"]
    print("Number of keys:", len(sub_map.keys()))
    for k in list(sub_map.keys())[:5]:
        print(type(k), k)

if __name__ == '__main__':
    inspect()
