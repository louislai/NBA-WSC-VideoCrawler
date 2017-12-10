### Requirement

Python 3

### Running instructions

Recommended to use Pycharm to open the project.


1. Get an temporary access token at [here](https://developers.facebook.com/tools/explorer?method=GET&path=10155806904058463%3Ffields%3Dsource%2Ctitle&version=v2.11) and replace the value of the constant `FACEBOOK_ACCESS_TOKEN` in `constants.py`.
2. In `crawler.py`, set the directory where the videos are going to be downloaded to with the variable `OUT_DIR`.

By default, only videos from May 2017 are going to be downloaded.