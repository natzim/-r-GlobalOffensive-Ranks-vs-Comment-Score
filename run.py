"""
/r/GlobalOffensive rank vs comment score

Author: Nat Zimmermann /u/NatNoBrains
"""
import praw
from getpass import getpass
from collections import OrderedDict

import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

RANKS = [
    "Silver I",
    "Silver II",
    "Silver III",
    "Silver IV",
    "Silver Elite",
    "Silver Elite Master",
    "Gold Nova I",
    "Gold Nova II",
    "Gold Nova III",
    "Gold Nova Master",
    "Master Guardian I",
    "Master Guardian II",
    "Master Guardian Elite",
    "Distinguished Master Guardian",
    "Legendary Eagle",
    "Legendary Eagle Master",
    "Supreme Master First Class",
    "The Global Elite"
]

r = praw.Reddit(user_agent="/r/GlobalOffensive rank vs comment score by /u/NatNoBrains")

r.login(input("Username: "), getpass("Password: "))

print("Working...")

posts = r.get_subreddit("GlobalOffensive").get_hot(limit=None)

data = OrderedDict()

for rank in RANKS:
    data[rank] = []

for post in posts:
    for comment in post.comments:
        try:
            score = comment.score
            flair = comment.author_flair_text

            if flair in RANKS:
                data[flair].append(score)

        except AttributeError:
            pass

for rank in data:
    if (len(data[rank]) > 0):
        data[rank] = sum(data[rank]) / len(data[rank])
    else:
        data[rank] = 0

graph = Data([
    Bar(
        x=list(data.keys()),
        y=list(data.values())
    )
])

layout = Layout(
    title="/r/GlobalOffensive Rank vs Comment Score",
    xaxis=XAxis(
        title="Rank"
    ),
    yaxis=YAxis(
        title="Average Comment Score"
    )
)

fig = Figure(data=graph, layout=layout)

plot_url = py.plot(fig, filename='rank-vs-comment-score')

print(plot_url)
