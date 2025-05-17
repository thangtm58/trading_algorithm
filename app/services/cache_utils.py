import os
import pickle

def get_cached_result(symbol, key, compute_func, cache_dir="app/cache"):
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{symbol}_{key}.pkl")

    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    result = compute_func()
    with open(cache_file, "wb") as f:
        pickle.dump(result, f)
    return result
