from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime as dt
from dotenv import load_dotenv
import os

# Lists for WTForms
days_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
             "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
months_list = [("1", "Jan"), ("2", "Feb"), ("3", "Mar"), ("4", "Apr"), ("5", "May"), ("6", "June"),
               ("7", "July"), ("8", "Aug"), ("9", "Sep"), ("10", "Oct"), ("11", "Nov"),
               ("12", "Dec")]
years_list = ["1960", "1961", "1962", "1963", "1964", "1965", "1966", "1967", "1968", "1969", "1970", "1971", "1972",
              "1973", "1974", "1975", "1976", "1977", "1978", "1979", "1980", "1981", "1982", "1983", "1984", "1985",
              "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998",
              "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011",
              "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
years_list.reverse()


# WTForms setup
class PlaylistForm(FlaskForm):
    day = SelectField(label='Date: ', choices=days_list)
    month = SelectField(label='Month: ', choices=months_list, default="Month")
    year = SelectField(label='Year: ', choices=years_list, default="Year")
    submit = SubmitField(label='Submit')


# Main class to reference in maim.py
class PlaylistTimemachine:
    def __init__(self, year, month, day):
        self.playlist_id = generate_playlist(year_date=year, month_date=month, day_date=day)


# Main query function for spotify
def generate_playlist(year_date, month_date, day_date):

    # Spotify constants setup
    load_dotenv(".env")
    CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
    CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
    REDIRECT_URI = "http://example.com"
    USERNAME = os.environ["SPOTIFY_USERNAME"]

    if len(month_date) == 1:
        month_date = "0" + month_date
    if len(day_date) == 1:
        day_date = "0" + day_date

    search_date = year_date + "-" + month_date + "-" + day_date

    response = requests.get(f"https://www.billboard.com/charts/hot-100/{search_date}")
    result = response.text

    # Iterate through the html site for both title and artists on Billboard hot 100
    titles_soup = BeautifulSoup(result, "html.parser")
    titles_list_search = titles_soup.find_all(name="li", class_="lrv-u-width-100p")
    titles_soup2 = BeautifulSoup(str(titles_list_search), "html.parser")
    titles_list_search2 = titles_soup2.find_all(name="ul", class_="lrv-a-unstyle-list lrv-u-flex lrv-u-height-100p lrv-u-flex-"
                                                   "direction-column@mobile-max")
    titles_soup3 = BeautifulSoup(str(titles_list_search2), "html.parser")

    titles = titles_soup3.find_all(name="h3", id="title-of-a-story")
    titles_list = []

    for title in titles:
        t = "".join(line.strip() for line in title.getText().split("\n"))
        titles_list.append(t)

    artists_soup = BeautifulSoup(result, "html.parser")
    artists_list_search = artists_soup.find_all(name="li", class_="lrv-u-width-100p")
    artists_soup2 = BeautifulSoup(str(artists_list_search), "html.parser")
    artists_list_search2 = artists_soup2.find_all(name="ul", class_="lrv-a-unstyle-list lrv-u-flex lrv-u-height-100p lrv-u-flex-"
                                                   "direction-column@mobile-max")
    artists_soup3 = BeautifulSoup(str(artists_list_search2), "html.parser")

    artists = artists_soup3.find_all(name="span")
    artists_list = []

    for artist in artists:
        a = "".join(line.strip() for line in artist.getText().split("\n"))
        if not a.isnumeric():
            artists_list.append(a)

    # Spotify API Setup
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=USERNAME,
    )
    )

    # Declaring core variables
    user_id = sp.current_user()["id"]
    titles_list = []
    song_uris = []
    year = "2019"

    # For loop to append titles to title-list
    for title in titles:
        t = "".join(line.strip() for line in title.getText().split("\n"))
        titles_list.append(t)

    # For loop that creates URI's for each song in title_list - tries to except if IndexError occurs
    for index, song in enumerate(titles_list):
        result = sp.search(q=f"track:{song} artist:{artists_list[index]}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            pass

    date_raw = dt.datetime(int(year_date), int(month_date), int(day_date))
    date_string = date_raw.strftime("%B %d, %Y")

    # Create playlist and add each item from the song_uri list to the playlist
    playlist = sp.user_playlist_create(user=user_id, name=f"{date_string} - PlaylistTimemachine", public=False)
    sp.playlist_add_items(playlist_id=f"{playlist['id']}", items=song_uris)
    print(playlist['id'])
    return playlist['id']
