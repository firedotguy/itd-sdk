class NoCookie(Exception):
    def __str__(self):
        return 'No cookie for refresh-token required action'

class NoAuthData(Exception):
    def __str__(self):
        return 'No auth data. Provide token or cookies'

class InvalidCookie(Exception):
    def __str__(self):
        return f'Invalid cookie data'

class InvalidToken(Exception):
    def __str__(self):
        return f'Invalid access token'


class SamePassword(Exception):
    def __str__(self):
        return 'Old and new password must not equals'

class InvalidOldPassword(Exception):
    def __str__(self):
        return 'Old password is incorrect'

class UserNotFound(Exception):
    def __str__(self):
        return 'User not found'

class UserBanned(Exception):
    def __str__(self):
        return 'User banned'

class InvalidProfileData(Exception):
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
    def __str__(self):
        return f'Invalid update profile data {self.name}: "{self.value}"'

class PendingRequestExists(Exception):
    def __str__(self):
        return 'Pending verifiaction request already exists'