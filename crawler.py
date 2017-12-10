import calendar
import facebook
import requests
import cv2
from constants import *
import datetime
from os import path, remove
from tqdm import tqdm

out_dir = "/Users/louis/Downloads/wsc"

class Crawler:

    # By default retrieve videos from Jan 2017
    def __init__(self, out_dir, since=(2017, 1)):
        self.graph = facebook.GraphAPI(FACEBOOK_ACCESS_TOKEN)
        self.out_dir = out_dir
        self.since = since

    def is_wsc_video(vid_file_path):
        cap = cv2.VideoCapture(vid_file_path)
        _, frame = cap.read()

        # Heuristic: WSC video starts with a white flash
        return cv2.norm(frame - 255.) == 0

    def create_range_args(self, year_month):
        year, month = year_month

        start_day, end_day = calendar.monthrange(year, month)
        since = (year, month, start_day)
        until = (year, month, end_day)

        return {
            'since': '%s-%s-%s' % since,
            'until': '%s-%s-%s' % until
        }

    def crawl(self):
        now = datetime.datetime.now()
        end_year, end_month = now.year, now.month

        all_year_months = []
        cur_year = self.since[0]
        cur_month = self.since[1]
        while cur_year < end_year or cur_month < end_month:
            all_year_months.append((cur_year, cur_month))

            cur_month += 1
            if cur_month > 12:
                cur_month = 1
                cur_year += 1

        pbar = tqdm(total=len(all_year_months))

        print('Retrieving video urls')
        vid_ids = []
        for year_month in all_year_months:
            vid_ids += self.retrieve_videos_details_year_month(year_month)
            pbar.update()
        pbar.close()

        print('Downloading videos')
        pbar = tqdm(total=len(vid_ids))
        for vid_id in vid_ids:
            self.retrieve_video(vid_id)
            pbar.update()
        pbar.close()

    def retrieve_videos_details_year_month(self, year_month):
        range_args = self.create_range_args(year_month)
        videos = self.graph.request(path='%s/videos/uploaded' % NBA_FACEBOOK_PAGE_ID, args=range_args, method='GET')

        video_ids = []
        while True:
            try:
                # Perform some action on each post in the collection we receive from
                # Facebook.
                for video in videos['data']:
                    video_ids.append(video['id'])

                # Attempt to make a request to the next page of data, if it exists.
                videos = requests.get(videos['paging']['next']).json()
            except KeyError:
                # When there are no more pages (['paging']['next']), break from the
                # loop and end the script.
                break
        return video_ids

    def retrieve_video(self, vid_id):
        video = self.graph.request(path='%s?fields=source,title' % vid_id, method='GET')
        r = requests.get(video['source'])
        video_path = path.join(self.out_dir, '%s.mp4' % video['title'].replace(" ", ""))
        with open(video_path, 'wb') as f:
            f.write(r.content)

        # Remove if not wsc video
        if not self.is_wsc_video(video_path):
            try:
                remove(video_path)
            except OSError:
                pass



crawler = Crawler(out_dir=out_dir, since=(2017, 5))
crawler.crawl()