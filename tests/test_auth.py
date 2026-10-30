def test_register_and_login(client):
    # Register
    res = client.post('/api/auth/register', json={
        'username': 'new_farmer',
        'password': 'password123',
        'full_name': 'Ramesh Kumar',
        'preferred_language': 'kn'
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['success'] is True
    assert data['data']['user']['username'] == 'new_farmer'

    # Login
    login_res = client.post('/api/auth/login', json={
        'username': 'new_farmer',
        'password': 'password123'
    })
    assert login_res.status_code == 200
    assert login_res.get_json()['success'] is True

def test_login_invalid_password(client, test_farmer):
    res = client.post('/api/auth/login', json={
        'username': 'test_kisan',
        'password': 'wrongpassword'
    })
    assert res.status_code == 401
    assert res.get_json()['success'] is False

def test_farmer_phone_otp_flow(client):
    # Request OTP
    req_res = client.post('/api/auth/farmer/request-otp', json={
        'phone_number': '9845012345'
    })
    assert req_res.status_code == 200
    assert req_res.get_json()['data']['demo_otp'] == '2026'

    # Verify OTP
    v_res = client.post('/api/auth/farmer/verify-otp', json={
        'phone_number': '9845012345',
        'otp': '2026'
    })
    assert v_res.status_code == 200
    data = v_res.get_json()['data']
    assert data['user']['phone_number'] == '9845012345'
    assert data['user']['role'] == 'FARMER'

def test_officer_phone_otp_flow(client):
    # Request OTP for Dr. Lalit Singh Rathod (Dharwad)
    req_res = client.post('/api/admin/request-otp', json={
        'phone_number': '9845012345'
    })
    assert req_res.status_code == 200
    data = req_res.get_json()['data']
    assert 'Dr. Lalit Singh Rathod' in data['officer_name']
    assert data['officer_district'] == 'Dharwad'
    assert data['demo_otp'] == '2026'

    # Verify official OTP
    login_res = client.post('/api/admin/phone-login', json={
        'phone_number': '9845012345',
        'otp': '2026'
    })
    assert login_res.status_code == 200
    admin_data = login_res.get_json()['data']['admin']
    assert admin_data['full_name'] == 'Dr. Lalit Singh Rathod'
    assert admin_data['district'] == 'Dharwad'

    # Check /api/admin/me returns logged in officer
    me_res = client.get('/api/admin/me')
    assert me_res.status_code == 200
    assert me_res.get_json()['data']['admin']['full_name'] == 'Dr. Lalit Singh Rathod'

    # Test logout
    logout_res = client.post('/api/admin/logout')
    assert logout_res.status_code == 200

def test_new_farmer_registration_then_login_flow(client):
    # Step 1: Request Aadhaar OTP for new registration
    new_phone = '9911223344'
    new_aadhaar = '842199887766'
    new_name = 'Basavaraj Hiremath'
    
    otp_req = client.post('/api/identity/generate-otp', json={
        'full_name': new_name,
        'aadhaar_number': new_aadhaar,
        'mobile_number': new_phone,
        'consent': True,
        'preferred_language': 'kn'
    })
    assert otp_req.status_code == 200
    txn_id = otp_req.get_json()['data']['transaction_id']

    # Step 2: Verify Aadhaar OTP
    v_res = client.post('/api/identity/verify-otp', json={
        'transaction_id': txn_id,
        'otp': '2026'
    })
    assert v_res.status_code == 200

    # Step 3: Complete registration and profile creation
    comp_res = client.post('/api/identity/complete-registration', json={
        'transaction_id': txn_id,
        'district': 'Hassan',
        'taluk': 'Channarayapatna',
        'village': 'Nuggehalli',
        'land_acres': 3.5,
        'preferred_language': 'kn'
    })
    assert comp_res.status_code in (200, 201)
    created_user = comp_res.get_json()['data']['user']
    assert created_user['phone_number'] == new_phone

    # Step 4: Login with Phone Number only + OTP
    login_otp_req = client.post('/api/auth/farmer/request-otp', json={
        'phone_number': new_phone
    })
    assert login_otp_req.status_code == 200

    login_v_res = client.post('/api/auth/farmer/verify-otp', json={
        'phone_number': new_phone,
        'otp': '2026'
    })
    assert login_v_res.status_code == 200
    assert login_v_res.get_json()['data']['user']['phone_number'] == new_phone

    # Step 5: Check profile and dashboard return strictly the newly logged in farmer
    status_res = client.get('/api/auth/status')
    assert status_res.status_code == 200
    status_data = status_res.get_json()['data']
    assert status_data['farmer_authenticated'] is True
    assert status_data['farmer']['phone_number'] == new_phone
    assert new_name in status_data['farmer']['full_name']

    profile_res = client.get('/api/profile')
    assert profile_res.status_code == 200
    prof_data = profile_res.get_json()['data']
    assert new_name in prof_data['full_name']
    assert prof_data['phone_number'] == new_phone

    # Step 6: Logout
    logout_res = client.post('/api/auth/logout')
    assert logout_res.status_code == 200


