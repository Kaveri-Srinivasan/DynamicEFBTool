from django.contrib.auth.tokens import PasswordResetTokenGenerator

class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + user.Email + str(timestamp) 
                    )

custom_password_reset_token_generator = CustomPasswordResetTokenGenerator()