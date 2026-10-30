import re

def validate_username(username: str) -> tuple[bool, str]:
    if not username or len(username.strip()) < 3:
        return False, "Username must be at least 3 characters long."
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username may only contain letters, numbers, and underscores."
    return True, ""

def validate_password(password: str) -> tuple[bool, str]:
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""

def validate_soil_input(data: dict) -> tuple[bool, dict, str]:
    """Validates numeric boundaries for standard ICAR soil test parameters."""
    sanitized = {}
    try:
        if 'ph' in data and data['ph'] is not None:
            ph = float(data['ph'])
            if not (0.0 <= ph <= 14.0):
                return False, {}, "Soil pH must be between 0.0 and 14.0."
            sanitized['ph'] = round(ph, 2)
        else:
            sanitized['ph'] = None

        if 'ec' in data and data['ec'] is not None:
            ec = float(data['ec'])
            if ec < 0:
                return False, {}, "Electrical Conductivity (EC) cannot be negative."
            sanitized['ec'] = round(ec, 2)
        else:
            sanitized['ec'] = None

        for nutrient in ['nitrogen', 'phosphorus', 'potassium', 'organic_carbon']:
            if nutrient in data and data[nutrient] is not None:
                val = float(data[nutrient])
                if val < 0:
                    return False, {}, f"{nutrient.capitalize()} value cannot be negative."
                sanitized[nutrient] = round(val, 2)
            else:
                sanitized[nutrient] = None

        return True, sanitized, ""
    except (ValueError, TypeError):
        return False, {}, "Invalid numeric format provided for soil measurements."

def validate_calculator_scenario(data: dict) -> tuple[bool, dict, str]:
    """Validates inputs for the farming scenario financial engine."""
    required = ['crop_name', 'land_acres', 'expected_yield_quintals', 'price_per_quintal']
    for req in required:
        if req not in data:
            return False, {}, f"Missing required parameter: {req}"
    
    try:
        acres = float(data['land_acres'])
        if acres <= 0:
            return False, {}, "Land area must be greater than zero."
            
        yield_q = float(data['expected_yield_quintals'])
        if yield_q <= 0:
            return False, {}, "Yield must be greater than zero."

        price = float(data['price_per_quintal'])
        if price <= 0:
            return False, {}, "Selling price must be greater than zero."

        sanitized = {
            'crop_name': str(data['crop_name']).strip(),
            'land_acres': acres,
            'expected_yield_quintals': yield_q,
            'price_per_quintal': price,
            'seed_cost': float(data.get('seed_cost', 0) or 0),
            'fertilizer_cost': float(data.get('fertilizer_cost', 0) or 0),
            'pesticide_cost': float(data.get('pesticide_cost', 0) or 0),
            'labour_cost': float(data.get('labour_cost', 0) or 0),
            'irrigation_cost': float(data.get('irrigation_cost', 0) or 0),
            'transport_cost': float(data.get('transport_cost', 0) or 0),
            'other_cost': float(data.get('other_cost', 0) or 0)
        }
        return True, sanitized, ""
    except (ValueError, TypeError) as e:
        return False, {}, f"Invalid numerical value: {str(e)}"

