from darcyforchheimer import calculate_coefficients


def test_calculate_coefficients():
    assert calculate_coefficients([1, 2, 3], [2, 4, 9], 0.0015, 1.225, 1.81e-5) == (
        30047493.484888732,
        773.3619867907446,
    )
