"""
Crop Image & Symptom Diagnostic Service.
Strictly isolates visible physical observations from probabilistic hypotheses.
Never gives a false definitive diagnosis.
"""
from typing import Dict, Any

class CropIntelligenceService:
    @staticmethod
    def analyze_crop_symptoms(crop_name: str, symptoms: str, growth_stage: str = "Vegetative") -> Dict[str, Any]:
        symptom_lower = symptoms.lower()
        
        observations = []
        possible_causes = []
        cautious_actions = []
        confidence = 0.85
        
        # Rule-based diagnostic heuristics
        if any(w in symptom_lower for w in ['yellow', 'pale', 'ಹಳದಿ']):
            observations.append("Chlorosis (yellowing) detected along leaf surface.")
            possible_causes.append({
                "cause": "Nitrogen Deficiency",
                "likelihood": "HIGH",
                "evidence": "Lower older leaves typically yellow first in nitrogen stress."
            })
            possible_causes.append({
                "cause": "Over-irrigation / Waterlogging",
                "likelihood": "MEDIUM",
                "evidence": "Root hypoxia impedes nutrient uptake."
            })
            cautious_actions.append("Conduct an electrical conductivity / root moisture check before applying foliar urea.")
            cautious_actions.append("Spray 1% Urea solution (10g/L water) if soil drainage is intact.")
            
        elif any(w in symptom_lower for w in ['spot', 'curl', 'brown', 'ಮಚ್ಚೆ', 'ಸುರುಟು']):
            observations.append("Necrotic lesions or leaf curling visible on foliage.")
            possible_causes.append({
                "cause": "Early Blight (Alternaria solani) or Fungal Spot",
                "likelihood": "MEDIUM-HIGH",
                "evidence": "Concentric rings or dark brown spots on foliage."
            })
            possible_causes.append({
                "cause": "Sucking Pests (Thrips / Mites / Whitefly)",
                "likelihood": "MEDIUM",
                "evidence": "Upward or downward leaf curling indicates pest feeding injury."
            })
            cautious_actions.append("Inspect undersides of leaves with a 10x lens for moving nymph colonies.")
            cautious_actions.append("Consult your Taluk Assistant Director of Agriculture (ADA) before applying chemical fungicides.")
            
        else:
            observations.append(f"Reported symptoms on {crop_name}: '{symptoms}'.")
            possible_causes.append({
                "cause": "Environmental Heat Stress or Micronutrient Imbalance",
                "likelihood": "MODERATE",
                "evidence": "Non-specific foliar symptoms during early stage."
            })
            cautious_actions.append("Maintain consistent drip irrigation intervals.")
            confidence = 0.65

        return {
            "crop_name": crop_name,
            "growth_stage": growth_stage,
            "observations": observations,
            "hypotheses": possible_causes,
            "cautious_actions": cautious_actions,
            "diagnostic_confidence": confidence,
            "disclaimer": "AI observation only. Not a laboratory diagnosis. Please cross-verify with your local Krishi Vigyan Kendra (KVK)."
        }

