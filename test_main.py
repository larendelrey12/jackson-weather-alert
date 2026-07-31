import unittest

import main


class WeatherAlertTests(unittest.TestCase):
    def test_should_send_alert_for_rain_related_conditions(self):
        self.assertTrue(main.should_send_alert("light rain"))
        self.assertTrue(main.should_send_alert("clear sky", "thunderstorm"))
        self.assertFalse(main.should_send_alert("clear sky", "few clouds"))


if __name__ == "__main__":
    unittest.main()
