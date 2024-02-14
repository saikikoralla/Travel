from rest_framework_simplejwt.tokens import RefreshToken


class GenerateUserTokens:
    @staticmethod
    def generate_user_tokens(user):
        generated_token = RefreshToken.for_user(user)
        token = {
            'refresh': str(generated_token),
            'access': str(generated_token.access_token)
        }

        return token