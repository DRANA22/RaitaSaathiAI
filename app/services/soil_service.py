"""
Soil Test Report Interpreter against Indian Council of Agricultural Research (ICAR) Standards.
"""
from typing import Dict, Any

class SoilInterpretationService:
    @staticmethod
    def interpret(measurements: Dict[str, Any], crop_name: str = "General") -> Dict[str, Any]:
        results = {}
        missing = []
        action_recommendations = []

        # 1. Soil pH (Acidity / Alkalinity)
        ph = measurements.get('ph')
        if ph is not None:
            if ph < 6.0:
                ph_status = "ACIDIC"
                ph_note = "Soil is acidic. Phosphorus fixation is likely. Consider agricultural lime application."
            elif 6.0 <= ph <= 7.5:
                ph_status = "OPTIMAL / NEUTRAL"
                ph_note = "Soil pH is in the optimal range for maximum nutrient bioavailability."
            else:
                ph_status = "ALKALINE / SALINE"
                ph_note = "Alkaline soil. Zinc and Iron deficiencies may occur. Consider gypsum amendment."
            results['ph'] = {"value": ph, "status": ph_status, "note": ph_note}
        else:
            missing.append("ph")

        # 2. Electrical Conductivity (EC in dS/m)
        ec = measurements.get('ec')
        if ec is not None:
            if ec < 1.0:
                ec_status = "NORMAL (Non-Saline)"
            elif 1.0 <= ec <= 2.0:
                ec_status = "CRITICAL (Mild Salinity)"
            else:
                ec_status = "INJURIOUS (High Salinity)"
            results['ec'] = {"value": ec, "status": ec_status}
        else:
            missing.append("ec")

        # 3. Available Nitrogen (kg/ha)
        n = measurements.get('nitrogen')
        if n is not None:
            if n < 280:
                n_status = "LOW"
                action_recommendations.append("Supplement organic compost or neem-coated urea in split doses.")
            elif 280 <= n <= 560:
                n_status = "MEDIUM"
            else:
                n_status = "HIGH"
            results['nitrogen'] = {"value": n, "unit": "kg/ha", "status": n_status}
        else:
            missing.append("nitrogen")

        # 4. Available Phosphorus (P2O5 kg/ha)
        p = measurements.get('phosphorus')
        if p is not None:
            if p < 10:
                p_status = "LOW"
                action_recommendations.append("Apply Single Super Phosphate (SSP) at root zone prior to sowing.")
            elif 10 <= p <= 25:
                p_status = "MEDIUM"
            else:
                p_status = "HIGH"
            results['phosphorus'] = {"value": p, "unit": "kg/ha", "status": p_status}
        else:
            missing.append("phosphorus")

        # 5. Available Potassium (K2O kg/ha)
        k = measurements.get('potassium')
        if k is not None:
            if k < 110:
                k_status = "LOW"
                action_recommendations.append("Apply Muriate of Potash (MOP) to improve drought and pest resistance.")
            elif 110 <= k <= 280:
                k_status = "MEDIUM"
            else:
                k_status = "HIGH"
            results['potassium'] = {"value": k, "unit": "kg/ha", "status": k_status}
        else:
            missing.append("potassium")

        return {
            "parameters_analyzed": results,
            "missing_parameters": missing,
            "recommendations": action_recommendations,
            "standard_reference": "ICAR - Soil Health Card Guidelines",
            "is_complete": len(missing) == 0
        }

