import os
import sys
from pathlib import PurePosixPath
from re import search
from urllib.parse import unquote, urlparse

import googlemaps
from dotenv import load_dotenv

from constants import Constants
from utils.file_utils import file_utils


class GoogleCollectPlacesData:
    gmaps = None
    place = None
    language = None

    places = []
    reviews = []

    TRAINED_MODEL_BUCKET = os.environ.get('TRAINED_MODEL_BUCKET')

    @staticmethod
    def config():
        if GoogleCollectPlacesData.gmaps is None:
            load_dotenv()
            GOOGLE_MAP_API_KEY = os.environ.get('GOOGLE_MAP_API_KEY')
            GoogleCollectPlacesData.gmaps = googlemaps.Client(key=GOOGLE_MAP_API_KEY)

            # Look for files relative to the directory we are running from
            os.chdir(os.path.dirname(__file__))

        return GoogleCollectPlacesData.gmaps

    @classmethod
    def processCollectPlaces(self, place, language="en"):
        try:
            GoogleCollectPlacesData.place = place
            GoogleCollectPlacesData.language = language

            self.__textSearch(self, pageToken=None)

            placekeys = GoogleCollectPlacesData.places[0].keys()
            file_name = f'places-{GoogleCollectPlacesData.place}.csv'
            file_utils.saveFile(keys=placekeys, values=GoogleCollectPlacesData.places,
                                path_name=''.join(["datas/places/", str(file_name)]),
                                file_name=file_name,
                                file_storage_name=self.TRAINED_MODEL_BUCKET)

            reviewkeys = GoogleCollectPlacesData.reviews[0].keys()
            file_name = f'reviews-{GoogleCollectPlacesData.place}.csv'
            file_utils.saveFile(keys=reviewkeys, values=GoogleCollectPlacesData.reviews,
                                path_name=''.join(["datas/reviews/", str(file_name)]),
                                file_name=file_name,
                                file_storage_name=self.TRAINED_MODEL_BUCKET)

        except Exception as error:
            print("Error to process collect places: " + error)

        finally:
            print("Process collect places finished.")

    def __textSearch(self, pageToken):
        print("Find places nearby for " + GoogleCollectPlacesData.place)

        response = self.gmaps.places(
            query="things to do in " + GoogleCollectPlacesData.place,
            page_token=pageToken,
            language=GoogleCollectPlacesData.language
        )

        self.__buildPlaces(self, textSearchResults=response['results'])

        if ('next_page_token' in response):
            print('Getting next page...')
            pageToken = response['next_page_token']
            self.__textSearch(self, pageToken=pageToken)

    def __getGeocodeLocation(self, place):
        print('Getting place location...')
        response = self.gmaps.geocode(address=place)
        location = response[0]['geometry']['location']
        return location

    def __buildPlaces(self, textSearchResults):
        print('building places...')
        for textSearchResult in textSearchResults:
            place_id = textSearchResult.pop('place_id', None)

            placeDetailsResult = self.gmaps.place(
                place_id=place_id,
                fields=Constants.PLACES_DETAIL_FIELD,
                language=GoogleCollectPlacesData.language
            )['result']
            if (
                    search(GoogleCollectPlacesData.place, placeDetailsResult['formatted_address'])
                    and (not (set(placeDetailsResult['types']).isdisjoint(Constants.PLACES_TYPE))
            )):

                if ('reviews' in placeDetailsResult):
                    self.__buildReviews(self, placeDetailsResult=placeDetailsResult, place_id=place_id)

                weekday_text = None
                if ('opening_hours' in placeDetailsResult):
                    weekday_text = placeDetailsResult.pop('opening_hours').pop('weekday_text', None)

                place = {
                    "place_id": place_id,
                    "name": placeDetailsResult.pop('name', None),
                    "formatted_address": placeDetailsResult.pop('formatted_address', None),
                    "formatted_phone_number": placeDetailsResult.pop('formatted_phone_number', None),
                    "opening_hours": weekday_text,
                    "rating": placeDetailsResult.pop('rating', None),
                    "user_ratings_total": placeDetailsResult.pop('user_ratings_total', None),
                    "types": placeDetailsResult.pop('types', None),
                    "url": placeDetailsResult.pop('url', None)
                }
                GoogleCollectPlacesData.places.append(place)

    def __buildReviews(self, placeDetailsResult, place_id):
        print('building reviews for placeId: ' + place_id)
        for review in placeDetailsResult['reviews']:
            user_review = {
                "user_id": PurePosixPath(
                    unquote(
                        urlparse(
                            review['author_url']
                        ).path
                    )
                ).parts[3],
                "place_id": place_id,
                "rating": review['rating'],
                "text": review['text'],
                "time": review['time']
            }
            GoogleCollectPlacesData.reviews.append(user_review)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Please input a place name to search.')

    language = sys.argv[2] if len(sys.argv) == 3 else "en"

    collector = GoogleCollectPlacesData()
    collector.config()
    collector.processCollectPlaces(place=sys.argv[1], language=language)
