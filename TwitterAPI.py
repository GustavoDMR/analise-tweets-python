from tkinter import *

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import Twitter_Credentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# TWITTER CLIENT #


class TwitterClient:
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets


class TwitterAuthenticator:

    @staticmethod
    def authenticate_twitter_app():
        auth = OAuthHandler(input3.get(), input4.get())
        auth.set_access_token(input1.get(), input2.get())
        return auth


class TweetAnalyzer:

    """"
    Funçao para análise e classificação de tweets
    """

    @staticmethod
    def tweets_to_data_frame(tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


tela1 = Tk()

ACCESS_TOKEN = StringVar()
ACCESS_TOKEN_SECRET = StringVar()
CONSUMER_KEY = StringVar()
CONSUMER_SECRET = StringVar()


def botaocoleta():
    ACCESS_TOKEN.set(input1.get())
    ACCESS_TOKEN_SECRET.set(input2.get())
    CONSUMER_KEY.set(input3.get())
    CONSUMER_SECRET.set(input4.get())
    pesquisa = input5.get()

    print(pesquisa)

    if __name__ == '__main__':
        twitter_client = TwitterClient()
        tweet_analyzer = TweetAnalyzer()

        api = twitter_client.get_twitter_client_api()

        tweets_user = api.user_timeline(screen_name=input5.get(), count=200)

        df = tweet_analyzer.tweets_to_data_frame(tweets_user)

        time_likes = pd.Series(data=df['likes'].values, index=df['date'])
        time_likes.plot(figsize=(12, 8), color='r')
        plt.legend(time_likes, ['Likes', 'Dates'])
        plt.show()


def mousebtnesquerdo(evento):

    tela1.title('Coleta de Tweets ' + 'x: ' + str(evento.x) + ' y: ' + str(evento.y))


FundoTela1 = PhotoImage(file='fundo.png')
LabelFundo = Label(tela1, image=FundoTela1)
LabelFundo.place(x=0, y=0)


label1 = Label(tela1, text='Acess Token:', font="Arial 15 bold", bg='white')
label2 = Label(tela1, text='Acess Token Secret:', font="Arial 15 bold", bg='white')
label3 = Label(tela1, text='Consumer Key:', font="Arial 15 bold", bg='white')
label4 = Label(tela1, text='Consumer Key Secret:', font="Arial 15 bold", bg='white')
label5 = Label(tela1, text='Perfil:', font="Arial 15 bold", bg='white')
input1 = Entry(tela1)
input2 = Entry(tela1)
input3 = Entry(tela1)
input4 = Entry(tela1)
input5 = Entry(tela1)
botao1 = Button(tela1, text='Gerar gráfico', command=botaocoleta, font='Arial 15 bold',
                bg='#60A9DC', fg='white', borderwidth=0)

label1.place(width=138, height=20, x=180, y=143)
input1.place(width=200, height=20, x=320, y=143)
label2.place(width=206, height=20, x=112, y=183)
input2.place(width=200, height=20, x=320, y=183)
label3.place(width=156, height=20, x=162, y=223)
input3.place(width=200, height=20, x=320, y=223)
label4.place(width=220, height=20, x=98, y=263)
input4.place(width=200, height=20, x=320, y=263)
label5.place(width=100, height=20, x=235, y=303)
input5.place(width=200, height=20, x=320, y=303)
botao1.place(width=145, height=40, x=260, y=400)
tela1.geometry('653x643+392+0')


tela1.title('Coleta de Tweets')
tela1.iconbitmap(default='twicone.ico')
tela1.wm_resizable(width=False, height=False)


tela1.bind('<Button-1>', mousebtnesquerdo)
tela1.mainloop()
