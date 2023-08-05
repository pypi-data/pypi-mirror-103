
class Authentication:

    def __init__(self, **kwargs) -> None:
        """
        Authentication credentials to access the twitter api. These should be changed to ecobank twitter app
        and store in Azure Key vault before going to production.

        :param kwargs:
                API_KEY: consumer_key	Your consumer key
                API_SECRET_KEY: consumer_secret	Your consumer secret
                ACCESS_TOKEN: access_token	Your access token
                ACCESS_TOKEN_SECRET: token_secret	Your access token secret
                BEARER_TOKEN: bearer_token	Your bearer token (MANDATORY)
        """

        params = {
            'API_KEY': None,
            'API_SECRET_KEY': None,
            'BEARER_TOKEN': None,
            'ACCESS_TOKEN': None,
            'ACCESS_TOKEN_SECRET': None,
        }

        for kwarg in kwargs:
            if kwarg in params:
                params[kwarg] = kwargs[kwarg]

        self.HEADERS = {
            "Authorization": f"Bearer {params['BEARER_TOKEN']}"
        }
#
# bearer_token=
# 'AAAAAAAAAAAAAAAAAAAAAFfhOgEAAAAA1LIjW8T%2FELDPdGmAsP%2BJxDDWSSs%3DILkgHvU9UT9esus2oV3P485wGJid9LeNFbddzsW19KwY4Rilm4'
