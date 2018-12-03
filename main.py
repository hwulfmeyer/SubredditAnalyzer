import praw
import json
import time
import csv
import pprint

config = json.load(open('config.json'))

def removeduplicates():
    data = None

    with open('subreddits.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    data_cleaned = []
    for p in data:
        p = p[0].lower()
        if p not in data_cleaned:
            data_cleaned.append(p)

    data_cleaned.sort()
    with open('nsfwreddit_clean.csv', 'w') as myfile:
        for p in data_cleaned:
            myfile.write(p + "\n")
    return data_cleaned


def getdatasave():
    with open('nsfwreddit_clean.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    reddit = praw.Reddit(client_id=config["reddit"]["clientid"],
                         client_secret=config["reddit"]["clientsecret"],
                         user_agent=config["reddit"]["useragent"],
                         username=config["reddit"]["username"],
                         password=config["reddit"]["password"])
    # subredditname, subscribers, time of oldest post in last 60 in hot, average score past top 60
    for data_subreddit in data:
        subreddit = reddit.subreddit(data_subreddit[0])
        try:
            data_subreddit.append(float(subreddit.subscribers))
            submissions_hot = list(subreddit.hot(limit=60))
            data_subreddit.append(999999999999999.0)
            for submis in submissions_hot:
                if not submis.stickied:
                    if data_subreddit[2] > float(submis.created_utc):
                        data_subreddit[2] = float(submis.created_utc)

            submissions_top = list(subreddit.top(time_filter='month', limit=60))
            data_subreddit.append(0)
            counter = 0
            for submis in submissions_top:
                    counter += 1
                    data_subreddit[3] += float(submis.score)
            if counter != 0:
                data_subreddit[3] /= float(counter)
        except:
            data_subreddit[0] += " ### ERROR" 
            data_subreddit.append(0)
            data_subreddit.append(0)
            data_subreddit.append(0)

    max_subscribers = max([x[1] for x in data])
    max_oldtime = max([x[2] for x in data])
    max_avgscore = max([x[3] for x in data])

    with open('nsfwreddit_data.csv', 'w') as myfile:
        for p in data:
            #p[1] /= max_subscribers
            #p[2] /= max_oldtime
            #p[3] /= max_avgscore
            myfile.write(str(p[0]) + ";" + str(p[1]) + ";" + str(p[2]) + ";" + str(p[3]) + "\n")

    
if __name__ == "__main__":
    removeduplicates()
    getdatasave()

