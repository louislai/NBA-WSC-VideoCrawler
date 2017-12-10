import numpy as np
import facebook
import requests
import cv2
from constants import *

def isWSCVideo(vid_file_path):
    cap = cv2.VideoCapture(vid_file_path)
    _, frame = cap.read()
    cv2.imwrite('/Users/louis/Downloads/test.png', frame)

    # Heuristic: WSC video starts with a white flash
    return cv2.norm(frame - 255.) == 0

print(isWSCVideo('/Users/louis/Downloads/wsc.mp4'))

# def process_vid_obj(vid):
#     print(vid)
#
# graph = facebook.GraphAPI(FACEBOOK_ACCESS_TOKEN)
# videos = graph.get_connections(NBA_FACEBOOK_PAGE_ID, 'videos')
#
# # Wrap this block in a while loop so we can keep paginating requests until
# # finished.
# while True:
#     try:
#         # Perform some action on each post in the collection we receive from
#         # Facebook.
#         [process_vid_obj(video) for video in videos['data']]
#         # Attempt to make a request to the next page of data, if it exists.
#         videos = requests.get(videos['paging']['next']).json()
#     except KeyError:
#         # When there are no more pages (['paging']['next']), break from the
#         # loop and end the script.
#         break
