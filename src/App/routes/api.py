from App import app
from App.database import query_light_curve, query_by_id

from flask import request, jsonify

@app.route("/light_curve", methods=["GET"])
def light_curve():
    time, flux = query_light_curve (request.args.get("kepid"))

    return jsonify({
        "time": time,
        "flux": flux
    })

@app.route("/system_parameters", methods=["GET"])
def system_parameters ():
    result = query_by_id(request.args.get("kepid"))
    
    planet_radii = result["koi_prad"]
    planet_teff  = result["koi_teq"]

    start_raddii = result["koi_srad_y"]
    start_mass   = result["koi_smass"]
    start_teff   = result["koi_steff_x"]

    return jsonify({
        "planet_radii": float(planet_radii),
        "planet_teff" : float(planet_teff),
        
        "start_raddii": float(start_raddii),
        "start_teff": float(start_teff),
        "start_mass": float(start_mass)
    })