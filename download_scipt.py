import numpy  as np
import pandas as pd
import lightkurve as lk
import csv
from pathlib import Path
from scipy.stats import kurtosis

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

def _select_windows(phase, flux, width):
    in_tr = np.abs(phase) <= width
    oot   = np.abs(phase) >= 3*width
    return in_tr, oot

def _baseline_depth(phase, flux, width):
    in_tr, oot = _select_windows(phase, flux, width)
    if np.sum(oot) < 10:  # fallback si no hay suficiente OOT
        baseline = np.median(flux)
    else:
        baseline = np.median(flux[oot])
    depth = baseline - np.min(flux[in_tr]) if np.any(in_tr) else 0.0
    if depth <= 0:
        depth = np.ptp(flux) * 0.05 + 1e-9  # evita divisiones por cero
    return baseline, depth

def symmetry_index(phase, flux, width=0.05, nbins=100):
    phase = np.asarray(phase)
    flux  = np.asarray(flux)

    sel = np.abs(phase) <= width
    if np.sum(sel) < 20:
        return np.nan

    abs_phi = np.abs(phase[sel])
    f_sel   = flux[sel]

    bins = np.linspace(0, width, nbins+1)
    idx  = np.digitize(abs_phi, bins) - 1
    
    diffs = []
    for b in range(nbins):
        mask_bin = idx == b
        if not np.any(mask_bin):
            continue
        phi_bin  = phase[sel][mask_bin]
        f_bin    = f_sel[mask_bin]
        neg = (phi_bin < 0); pos = (phi_bin > 0)
        if np.any(neg) and np.any(pos):
            f_neg = np.median(f_bin[neg])
            f_pos = np.median(f_bin[pos])
            diffs.append(np.abs(f_pos - f_neg))

    if len(diffs) == 0:
        return np.nan

    _, depth = _baseline_depth(phase, flux, width)
    return np.median(diffs) / depth

def v_u_kurtosis(phase, flux, width=0.05):
    phase = np.asarray(phase)
    flux  = np.asarray(flux)

    in_tr, oot = _select_windows(phase, flux, width)

    if np.sum(in_tr) < 20:
        return np.nan

    baseline, depth = _baseline_depth(phase, flux, width)
    x = (baseline - flux[in_tr]) / depth
    return kurtosis(x, fisher=False, bias=False)

def ingress_egress_slopes(phase, flux, width=0.05):
    phase = np.asarray(phase)
    flux  = np.asarray(flux)

    ing = (phase >= -width) & (phase < 0)
    egr = (phase > 0) & (phase <= +width)

    m_ing, m_egr = np.nan, np.nan
    if np.sum(ing) >= 5:
        m_ing = np.polyfit(phase[ing], flux[ing], 1)[0]
    if np.sum(egr) >= 5:
        m_egr = np.polyfit(phase[egr], flux[egr], 1)[0]
    return m_ing, m_egr

def metrics_from_folded_lc(fold_lc, width=0.1):
    phase = np.asarray(getattr(fold_lc, "phase").value if hasattr(fold_lc, "phase") else fold_lc.phase)
    flux  = np.asarray(getattr(fold_lc, "flux").value  if hasattr(fold_lc, "flux")  else fold_lc.flux)

    asym = symmetry_index(phase, flux, width=width)
    kurt = v_u_kurtosis(phase, flux, width=width)
    m_ing, m_egr = ingress_egress_slopes(phase, flux, width=width)

    return {
        "asymmetry_index": asym,
        "v_u_kurtosis":    kurt,
        "ingress_slope":   m_ing,
        "egress_slope":    m_egr,
    }

symmetrys  = []
shapes     = []
slopes_in  = []
slopes_out = []

if __name__ == "__main__":
    out_path = Path("data/features_por_koi1.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["kepid", "asymmetry_index", "v_u_kurtosis", "ingress_slope", "egress_slope"]
    write_header = not out_path.exists()

    koi_df = pd.read_csv("data/koi_data1.csv")

    with out_path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        for idx, koi in enumerate(koi_df["kepid"]):
            if koi in koi_df["kepid"]:
                continue
            
            lc = download_light_curve(koi)
            if lc is None:
                print(f"KOI-{koi}: sin curva de luz, se omite")
                continue
            
            features = metrics_from_folded_lc(lc)

            # Escribimos UNA FILA por KOI, sin listas intermedias
            row = {
                "kepid":           int(koi),
                "asymmetry_index": features["asymmetry_index"],
                "v_u_kurtosis":    features["v_u_kurtosis"],
                "ingress_slope":   features["ingress_slope"],
                "egress_slope":    features["egress_slope"],
            }
            writer.writerow(row)
            f.flush()  # opcional: asegura que quede en disco en cada iteración

            print(f"KOI-{koi}, listo → guardado en {out_path}")