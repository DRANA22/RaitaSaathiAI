from app.services.calculator_service import AgriculturalCalculatorService

def test_deterministic_calculator_scenario():
    scenario = {
        'crop_name': 'Ragi',
        'land_acres': 2.0,
        'expected_yield_quintals': 15.0,
        'price_per_quintal': 3000.0,
        'seed_cost': 2000,
        'fertilizer_cost': 5000,
        'labour_cost': 8000,
        'irrigation_cost': 1000
    }
    
    res = AgriculturalCalculatorService.calculate_scenario(scenario)
    assert res['total_yield_quintals'] == 30.0 # 2.0 * 15.0
    assert res['gross_revenue'] == 90000.0     # 30.0 * 3000.0
    assert res['total_cost'] == 16000.0        # 2000 + 5000 + 8000 + 1000
    assert res['net_profit'] == 74000.0        # 90000 - 16000
    assert res['roi_percentage'] > 400.0

def test_calculator_comparison():
    scen_a = {
        'crop_name': 'Crop A', 'land_acres': 1.0, 'expected_yield_quintals': 10,
        'price_per_quintal': 1000, 'seed_cost': 2000
    }
    scen_b = {
        'crop_name': 'Crop B', 'land_acres': 1.0, 'expected_yield_quintals': 10,
        'price_per_quintal': 2000, 'seed_cost': 2000
    }
    comp = AgriculturalCalculatorService.compare_scenarios(scen_a, scen_b)
    assert comp['delta']['recommended'] == 'Scenario B'
    assert comp['delta']['profit_difference'] == 10000.0

