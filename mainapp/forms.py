from django import forms

class TweetScrapeForm(forms.Form):
    keywords = forms.CharField(max_length=255)
    num_tweets = forms.IntegerField()
