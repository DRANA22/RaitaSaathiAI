"""
Deterministic Agricultural Financial Calculator.
Computes yield, revenue, variable costs, gross margins, and sensitivity variations.
All calculations are pure Python math without LLM estimation.
"""
from typing import Dict, Any

class AgriculturalCalculatorService:
    @staticmethod
    def calculate_scenario(scenario: Dict[str, Any]) -> Dict[str, Any]:
        acres = float(scenario['land_acres'])
        yield_per_acre = float(scenario['expected_yield_quintals'])
        price_per_quintal = float(scenario['price_per_quintal'])
        
        # Total output
        total_yield_quintals = round(acres * yield_per_acre, 2)
        gross_revenue = round(total_yield_quintals * price_per_quintal, 2)
        
        # Operational expenses
        seed = float(scenario.get('seed_cost', 0))
        fert = float(scenario.get('fertilizer_cost', 0))
        pest = float(scenario.get('pesticide_cost', 0))
        labour = float(scenario.get('labour_cost', 0))
        irrigation = float(scenario.get('irrigation_cost', 0))
        transport = float(scenario.get('transport_cost', 0))
        other = float(scenario.get('other_cost', 0))
        
        total_variable_cost = round(seed + fert + pest + labour + irrigation + transport + other, 2)
        cost_per_acre = round(total_variable_cost / acres, 2) if acres > 0 else 0
        
        # Net outcomes
        net_profit = round(gross_revenue - total_variable_cost, 2)
        net_profit_per_acre = round(net_profit / acres, 2) if acres > 0 else 0
        roi_percentage = round((net_profit / total_variable_cost) * 100, 2) if total_variable_cost > 0 else 0.0

        # Deterministic 10% sensitivity tests (+/- 10% price and yield shifts)
        sensitivity = {
            "price_drop_10pct_profit": round((gross_revenue * 0.90) - total_variable_cost, 2),
            "price_rise_10pct_profit": round((gross_revenue * 1.10) - total_variable_cost, 2),
            "yield_drop_10pct_profit": round(((total_yield_quintals * 0.90) * price_per_quintal) - total_variable_cost, 2),
            "yield_rise_10pct_profit": round(((total_yield_quintals * 1.10) * price_per_quintal) - total_variable_cost, 2)
        }

        return {
            "crop_name": scenario['crop_name'],
            "land_acres": acres,
            "yield_per_acre_quintals": yield_per_acre,
            "total_yield_quintals": total_yield_quintals,
            "price_per_quintal": price_per_quintal,
            "cost_breakdown": {
                "seeds": seed,
                "fertilizer": fert,
                "pesticides": pest,
                "labour": labour,
                "irrigation": irrigation,
                "transport": transport,
                "other": other
            },
            "total_cost": total_variable_cost,
            "cost_per_acre": cost_per_acre,
            "gross_revenue": gross_revenue,
            "net_profit": net_profit,
            "net_profit_per_acre": net_profit_per_acre,
            "roi_percentage": roi_percentage,
            "sensitivity": sensitivity
        }

    @classmethod
    def compare_scenarios(cls, scenario_a: Dict[str, Any], scenario_b: Dict[str, Any]) -> Dict[str, Any]:
        res_a = cls.calculate_scenario(scenario_a)
        res_b = cls.calculate_scenario(scenario_b)
        
        diff_profit = round(res_b['net_profit'] - res_a['net_profit'], 2)
        diff_cost = round(res_b['total_cost'] - res_a['total_cost'], 2)
        diff_roi = round(res_b['roi_percentage'] - res_a['roi_percentage'], 2)

        higher_profit_scenario = "Scenario B" if diff_profit > 0 else ("Scenario A" if diff_profit < 0 else "Tie")
        
        return {
            "scenario_a": res_a,
            "scenario_b": res_b,
            "delta": {
                "profit_difference": diff_profit,
                "cost_difference": diff_cost,
                "roi_difference": diff_roi,
                "recommended": higher_profit_scenario
            }
        }

