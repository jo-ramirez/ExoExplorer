import numpy  as np
import pandas as pd
import lightkurve as lk

def fast_kepler_lc(kic, quarter=None, exptime="long"):
    search_result = lk.search_lightcurve(
        f"KIC {kic}",
        mission="Kepler",
        author="Kepler",
        exptime=exptime,
        quarter=10,
        cadence="long", 
    )

    try:
        lc_collection = search_result.download_all()
        lc = lc_collection.stitch().flatten(window_length=901).remove_outliers()
        return lc
    except:
        return None

def download_light_curve (kic):
    lc = fast_kepler_lc(kic)

    if lc == None:
        return None
    
    period = np.linspace(1, 20, 10000)
    bls = lc.to_periodogram(method='bls', period=period, frequency_factor=500)

    planet_b_period = bls.period_at_max_power
    planet_b_t0     = bls.transit_time_at_max_power

    fold_lc = lc.fold(period=planet_b_period, epoch_time=planet_b_t0)
    return fold_lc


if __name__ == "__main__":
    df = pd.read_csv("data/predicted_results.csv")
    for kepid in df["kepid"]:
        lc = download_light_curve(kepid)
        lc.to_fits(f"data/light_curves/KIC-{kepid}.fits", overwrite=True)