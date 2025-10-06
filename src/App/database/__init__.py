import numpy  as np
import pandas as pd

from astropy.io import fits

CSV_PATH  = "src/App/database/tables/predicted_results.csv"

DROP_COLS = [
    "kepler_name", "koi_fpflag_nt", "koi_fpflag_ss", "koi_fpflag_co",
    "koi_period_err1", "koi_period_err2", "koi_time0bk_err1", "koi_time0bk_err2",
    "koi_time0_err1", "koi_time0_err2", "koi_impact_err1", "koi_impact_err2",
    "koi_duration_err1", "koi_duration_err2", "koi_ingress", "koi_ingress_err1",
    "koi_ingress_err2", "koi_depth_err1", "koi_depth_err2", "koi_steff_err1",
    "koi_steff_err2", "koi_srad_err1", "koi_srad_err2", "koi_time0bk",
    "loc_rowid", "kepoi_name", "koi_quarters", 'koi_slogg_err1', "koi_slogg_err2"
    "ra", "dec", "koi_slogg_err2", "koi_slogg", "ra", "koi_kepmag"
]

def load_and_clean_df() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)

    # Eliminar columnas innecesarias
    cols_to_drop = [c for c in DROP_COLS if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)

    # Eliminar espacios en blanco en todas las celdas
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Asegurarse de que 'kepid' sea un entero
    if "kepid" in df.columns:
        df["kepid"] = pd.to_numeric(df["kepid"], errors="coerce").astype("Int64")

    # Filtrar por 'koi_disposition' si está presente
    if "koi_disposition" in df.columns:
        df = df[df["koi_disposition"] != "CANDIDATE"]
        df["koi_disposition"] = df["koi_disposition"].map({"FALSE POSITIVE": 0, "CONFIRMED": 1}).fillna(df["koi_disposition"])

    # Eliminar filas completamente vacías
    df = df.dropna(how="all")
    return df

def query_rows (n:int):
    df = load_and_clean_df()
    return df.head(n)

def query_by_id (id:int):
    df = load_and_clean_df()
        
    result = df[df["kepid"] == int(id)]
    
    if result.shape[0] == 0:
        raise ValueError(f"No se encontró ningún registro con kepid = {id}.")
    elif result.shape[0] > 1:
        raise ValueError(f"Se encontraron múltiples registros con kepid = {id}.")
    
    return result.iloc[0]

def query_light_curve (id:int):
    filename = f"KIC-{id}.fits"
    with fits.open(f"src\App\database\light_curves\{filename}") as hdul:
        data = hdul[1].data
        time = np.array(data["TIME"], dtype=float)
        flux = np.array(data["FLUX"], dtype=float)

        mask = np.isfinite(time) & np.isfinite(flux)
        time = time[mask]
        flux = flux[mask]

    return time.tolist(), flux.tolist()