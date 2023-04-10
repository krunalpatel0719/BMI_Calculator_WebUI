

import pytest
from flask_testing import TestCase
from app import app, bmi_class

class AppTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_underweight_category(self):
        bmi = bmi_class()
        assert bmi.bmi_category(16) == "underweight"
    def test_normalweight_category(self):
        bmi = bmi_class()
        assert bmi.bmi_category(20) == "of normal weight"
    def test_overweight_category(self):
        bmi = bmi_class()
        assert bmi.bmi_category(27) == "overweight"
    def test_obese_category(self):
        bmi = bmi_class()
        assert bmi.bmi_category(35) == "obese"
    def test_invalid_weight(self):
        bmi = bmi_class()
        with pytest.raises(ValueError) as exc_info:
            bmi.calculate_bmi('5 7', 0)
        assert str(exc_info.value) == "Weight must be non-zero"

    def test_invalid_feet(self):
        bmi = bmi_class()
        with pytest.raises(ValueError) as exc_info:
            bmi.calculate_bmi('0 7', 150)
        assert str(exc_info.value) == "Height must be non-zero"

    def test_invalid_inches(self):
        bmi = bmi_class()
        with pytest.raises(ValueError) as exc_info:
            bmi.calculate_bmi('5 12', 150)
        assert str(exc_info.value) == "Height in inches must be less than 12"

    def test_invalid_positive_height(self):
        bmi = bmi_class()
        with pytest.raises(ValueError) as exc_info:
            bmi.calculate_bmi('-5 -7', 150)
        assert str(exc_info.value) == "Height must be positive"

    def test_invalid_positive_weight(self):
        bmi = bmi_class()
        with pytest.raises(ValueError) as exc_info:
            bmi.calculate_bmi('5 7', -150)
        assert str(exc_info.value) == "Weight must be positive"

    def test_calculate_bmi(self):
        bmi = bmi_class()
        assert bmi.calculate_bmi('5 7', 150) == "Your BMI is: 24.06 and you are of normal weight"

    # Test cases using EPC technique
    def test_bmi_below_normal_lower(self):
        bmi = bmi_class()
        assert bmi.calculate_bmi('5 6', 111.28) == "Your BMI is: 18.39 and you are underweight"

    def test_bmi_below_normal_upper(self):
        bmi = bmi_class()
        assert bmi.calculate_bmi('5 6', 111.29) == "Your BMI is: 18.40 and you are underweight"

    def test_bmi_route(self):
        response = self.client.get('/bmi')
        self.assert200(response)
        self.assert_template_used('input_form.html')

    def test_bmi_route_post(self):
        response = self.client.post('/bmi', data={'height': '5 7', 'weight': 150})
        self.assert200(response)
        self.assert_template_used('result.html')
        assert b'Your BMI is: 24.06 and you are of normal weight' in response.data






# def test_bmi_above_normal_lower(monkeypatch):
#     monkeypatch.setattr('builtins.input', lambda prompt: '5 7\n' if 'height' in prompt else '130\n')
#     bmi = bmi_class()
#     assert bmi.calculate_bmi() == "Your BMI is: 25.24 and you are of normal weight"

# def test_bmi_above_normal_upper(monkeypatch):
#     monkeypatch.setattr('builtins.input', lambda prompt: '5 7\n' if 'height' in prompt else '250\n')
#     bmi = bmi_class()
#     assert bmi.calculate_bmi() == "Your BMI is: 24.90 and you are of normal weight"