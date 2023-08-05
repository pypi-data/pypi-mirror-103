import requests
from authentication import Authentication
from typing import List, Optional, Dict


class Users:

    def __init__(self, bearer_token: str) -> None:
        self.auth = Authentication(BEARER_TOKEN=bearer_token)
        self.headers = self.auth.HEADERS
        self.base_url = "https://api.twitter.com/2/users"

    def get_users_by_usernames(self, usernames: List) -> Dict:
        """
        This method returns details about a user by username.
        :param usernames: List of comma separated twitter usernames eg. [adomako_bismark, bizmaercq]
        :return: Dictionary of user details
        """
        usernames = ','.join(usernames)
        user_fields = "created_at,description,entities,id,location,name,pinned_tweet_id," \
                      "profile_image_url,protected,public_metrics,url,username,verified,withheld"
        tweet_fields = "attachments,author_id,context_annotations,conversation_id,created_at," \
                       "entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,organic_metrics," \
                       "possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,source,text,withheld"
        params = {
            "usernames": usernames,
            "user.fields": user_fields,
            "tweet.fields": tweet_fields,
        }
        url = f"{self.base_url}/by"
        try:
            response = requests.request("GET", url=url, headers=self.headers, params=params)
        except requests.exceptions as e:
            print(e)
        else:
            return response.json()

    def get_users_by_ids(self, userid: List[str]) -> Dict:
        """
        This method returns details about up to 100 users by ID.
        :param userid: List of comma separated twitter usernames eg. [234854410, 234854434]
        :return:Dictionary of user details
        """
        userid = ','.join(userid)
        user_fields = "created_at,description,entities,id,location,name,pinned_tweet_id," \
                      "profile_image_url,protected,public_metrics,url,username,verified,withheld"
        tweet_fields = "attachments,author_id,context_annotations,conversation_id,created_at," \
                       "entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,organic_metrics," \
                       "possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,source,text,withheld"
        params = {
            'ids': userid,
            'user.fields': user_fields,
            'tweet.fields': tweet_fields,
        }
        url = self.base_url

        try:
            response = requests.request("GET", url=url, headers=self.headers, params=params)
        except requests.exceptions as e:
            print(e)
        else:
            return response.json()

    def user_mentions(self, username: str, **kwargs: Optional) -> List:
        """
        Returns the most recent Tweets mentioning a single user specified by the requested user ID.
        :param username: user's handle to get mentions.
        :param kwargs:

                    pagination_token:str -> This parameter is used to move forwards or backwards through pages of
                    results, based on the value of the next_token or previous_token in the response.
                    The value used with the parameter is pulled directly from the response provided by the API,
                    and should not be modified.

                    start_time:Datetime -> YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339). The oldest or earliest UTC
                    timestamp from which the Tweets will be provided. Only the 3200 most recent Tweets are available.
                     Timestamp is in second granularity and is inclusive
                     (i.e. 12:00:01 includes the first second of the minute).
                     Minimum allowable time is 2010-11-06T00:00:00Z

                    end_time:Datetime, -> YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339). The oldest or earliest UTC timestamp
                     from which the Tweets will be provided. Only the 3200 most recent Tweets are available.
                     Timestamp is in second granularity and is inclusive
                     (i.e. 12:00:01 includes the first second of the minute).
                     Minimum allowable time is 2010-11-06T00:00:00Z

                    since_id:int ->Returns results with an ID greater than (that is, more recent than) the specified ID.
                    Only the 3200 most recent Tweets are available. The result will exclude the since_id. If the limit
                    of Tweets has occurred since the since_id, the since_id will be forced to the oldest ID available.

                    until_id: int -> Returns results with an ID less less than (that is, older than) the specified ID.
                    Only the 3200 most recent Tweets are available. The result will exclude the until_id. If the limit
                    of Tweets has occurred since the until_id, the until_id will be forced to the most
                    recent ID available.

        :return: Dictionary of user mention details
        """

        # Get userid for user handle provided
        user_details = self.get_users_by_usernames([username])
        if 'errors' in user_details:
            return user_details['errors']
        userid = user_details['data'][0]['id']

        tweet_fields = "attachments,author_id,context_annotations,conversation_id,created_at," \
                       "entities,geo,id,in_reply_to_user_id,lang," \
                       "possibly_sensitive,public_metrics,referenced_tweets," \
                       "reply_settings,source,text,withheld"
        user_fields = "created_at,description,entities,id,location,name,pinned_tweet_id," \
                      "profile_image_url,protected,public_metrics,url,username,verified,withheld"
        place_fields = "contained_within,country,country_code,full_name,geo,id,name,place_type"
        media_fields = "duration_ms,height,media_key,non_public_metrics,organic_metrics,preview_image_url," \
                       "promoted_metrics,public_metrics,type,url,width"
        expansions = "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id," \
                     "referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id"
        params = {
            'max_results': 100,
            'tweet.fields': tweet_fields,
            'user.fields': user_fields,
            'place.fields': place_fields,
            'media.fields': media_fields,
            'pagination_token': None,
            'expansions': expansions,
            'end_time': None,
            'start_time': None,
            'since_id': None,
            'until_id': None,
        }

        for kwarg in kwargs:
            if kwarg in params:
                params[kwarg] = kwargs[kwarg]
            else:
                return [{
                    'keyword_argument_error': f"The key word argument '{kwarg}' specified is not acceptable"
                }]

        url = f"{self.base_url}/{userid}/mentions"

        try:
            response = requests.request("GET", url=url, headers=self.headers, params=params)
        except requests.exceptions as e:
            print(e)
        else:
            data: List = []
            data += response.json()['data'] if 'data' in response.json() else []
            while 'next_token' in response.json()['meta']:
                params['pagination_token'] = response.json()['meta']['next_token']
                response = requests.request("GET", url=url, headers=self.headers, params=params)
                data += response.json()['data']
            return data


if __name__ == "__main__":
    from pprint import pprint
    users = Users(bearer_token='AAAAAAAAAAAAAAAAAAAAAFfhOgEAAAAA1LIjW8T%2FELDPdG'
                               'mAsP%2BJxDDWSSs%3DILkgHvU9UT9esus2oV3P485wGJid9LeNFbddzsW19KwY4Rilm4')
    pprint(users.user_mentions('ecobank'))
    # pprint(users.get_users_by_usernames(['adomako_bismark']))
