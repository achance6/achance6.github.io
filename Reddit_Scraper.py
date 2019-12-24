import urllib3
from bs4 import BeautifulSoup
import matplotlib
import numpy as np
from apscheduler.schedulers.background import BlockingScheduler
import matplotlib.pyplot as plot
from time import gmtime, strftime

def make_plot(labels=None, occurrences=None):
    if labels is None:
        labels = [""]
    if occurrences is None:
        occurrences = [0]

    x = np.arange(len(labels))  # the label locations
    colors = np.arange(0.125, 1.125, 0.125)
    width = 0.30  # the width of the bars
    fig, ax = matplotlib.pyplot.subplots()
    rects = ax.bar(x, occurrences, width, label='Occurrences',
                    color=('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'black'))

    set_labels(ax, labels, occurrences, x)
    label_bar_heights(rects, ax)
    ax.tick_params(axis='x', which='major', labelsize=8)
    fig.tight_layout(rect=(0, .15, 1, 1))
    plot.xticks(rotation=40)

    return matplotlib.pyplot


def set_labels(ax, labels, occurrences, x):
    """Add some text for labels, title and custom x-axis tick labels, etc."""
    ax.set_ylabel('# Occurrences (Updated Twice Daily)')
    ax.set_xlabel('Subreddits')
    ax.set_title('Top 8 subreddits with # Occurrences on Reddit Frontpage')
    ax.set_xticks(x)
    plot.yticks(np.arange(min(occurrences), max(occurrences) + 1, 1.0))
    ax.set_xticklabels(labels)


def label_bar_heights(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height - 0.0125),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def get_sorted_subs_dict(subs, posts):
    """Given a list of subs, updates posts and returns the subs occurrences keyed to each sub sorted"""
    for sub_object in subs:
        if sub_object.string is not None:
            if sub_object.string not in posts.keys():
                posts[sub_object.string] = 1
            else:
                posts[sub_object.string] += 1
    # Sorts subs by their occurrences in descending order
    sorted_sub_occurrences = dict(sorted(posts.items(), key=lambda kv: (kv[1], kv[0])), reverse=True)
    return sorted_sub_occurrences


def get_sub_objects_from_front_page():
    """Scrape the subs from the front page of reddit"""
    url = "https://www.reddit.com/r/all/"
    our_url = urllib3.PoolManager().request('GET', url).data
    soup = BeautifulSoup(our_url, "lxml")
    subs = soup.select('a[data-click-id="subreddit"]')
    return subs


def main():
    file = open("C:/Users/Ayden Chance/Desktop/achance6.github.io/Data.txt", 'r')
    if input("Read last data?") != 'n':
        for line in file:
            inp = line
        inp = inp[32:]
        print(inp)
        posts = eval(inp)
    else:
        posts = {}
    subs = get_sub_objects_from_front_page()
    sorted_subs = get_sorted_subs_dict(subs, posts)
    sub_occurrence_plot = make_plot(list(sorted_subs.keys())[-9:-1], list(sorted_subs.values())[-9:-1])
    sub_occurrence_plot.savefig('C:/Users/Ayden Chance/Desktop/achance6.github.io/graph.png')
    append_file = open("C:/Users/Ayden Chance/Desktop/achance6.github.io/Data.txt", 'a')
    append_file.write(strftime("%a, %d %b %Y %H:%M:%S +0000: ", gmtime()) + str(sorted_subs) + '\n')
    append_file.close()
    file.close()


if __name__ == "__main__":
    main()
    #scheduler = BlockingScheduler()
    #scheduler.add_job(main, 'interval', hours=12)
    #scheduler.start()
