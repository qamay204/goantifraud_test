import helium
import unittest
import time

TEST_DATA = {
    'valid_credentials': {
        'log': 'moisieievtest@gmail.com',
        'pass': '123456789'
        },
    'invalid_credentials': {
            'log': 'sometest@gmail.com',
            'pass': '123456789'
            }
    }
helium.Config.implicit_wait_secs = 5


class GoAntiLogIn(unittest.TestCase):

    def test_valid_credentials(self):
        driver = helium.start_chrome('https://goantifraud.com/manager', headless=True)
        helium.write(TEST_DATA['valid_credentials']['log'], into='login')
        helium.write(TEST_DATA['valid_credentials']['pass'], into='password')
        helium.press(helium.ENTER)
        check = helium.Text('AndriiTest').value
        helium.kill_browser()
        self.assertEqual(check, 'AndriiTest')

    def test_invalid_credentials(self):
        driver = helium.start_chrome('https://goantifraud.com/manager', headless=True)
        helium.write(TEST_DATA['invalid_credentials']['log'], into='login')
        helium.write(TEST_DATA['invalid_credentials']['pass'], into='password')
        helium.press(helium.ENTER)
        check = helium.Text('Login or password is incorrect').value
        helium.kill_browser()
        self.assertEqual(check, 'Login or password is incorrect')

    def test_recover_pass_with_valid_user(self):
        driver = helium.start_chrome('https://goantifraud.com/manager', headless=True)
        helium.click('Forgot your password?')
        helium.write(TEST_DATA['valid_credentials']['log'], into='login')
        helium.click('SEND')
        time.sleep(0.5)
        validation_msg_list = helium.find_all(helium.S(".error.error_show"))
        helium.kill_browser()
        self.assertEqual(len(validation_msg_list), 1)

    def test_recover_pass_with_invalid_user(self):
        driver = helium.start_chrome('https://goantifraud.com/manager', headless=True)
        helium.click('Forgot your password?')
        helium.write(TEST_DATA['invalid_credentials']['log'], into='login')
        helium.click('SEND')
        time.sleep(0.5)
        validation_msg_list = helium.find_all(helium.S(".error.error_show"))
        helium.kill_browser()
        self.assertEqual(len(validation_msg_list), 2)


if __name__ == '__main__':
    unittest.main()


