import logging
import re
from bs4 import BeautifulSoup

from anime_downloader.extractors.base_extractor import BaseExtractor
from anime_downloader.sites import helpers

logger = logging.getLogger(__name__)


class RapidVideo(BaseExtractor):
    def _get_data(self):
        url = self.url + '&q=' + self.quality
        logger.debug('Calling Rapid url: {}'.format(url))
        headers = self.headers
        headers['referer'] = url
        try:
            r = helpers.get(url, headers=headers)
        except Exception as e:
            logger.debug('Exception happened when getting normally')
            logger.debug(e)
            r = helpers.post(url, {
                'cursor.x': 12,
                'cursor.y': 12,
                'block': 1,
            }, headers=headers)
        soup = helpers.soupify(r)

        # TODO: Make these a different function. Can be reused in other classes
        #       too
        src_re = re.compile(r'src: "(.*)"')
        title_re = re.compile(r'"og:title" content="(.*)"')
        image_re = re.compile(r'"og:image" content="(.*)"')

        try:
            stream_url = soup.find_all('source')[0].get('src')
        except IndexError:
            try:
                stream_url = str(src_re.findall(r.text)[0])
            except IndexError:
                stream_url = None

        try:
            title = str(title_re.findall(r.text)[0])
            thumbnail = str(image_re.findall(r.text)[0])
        except Exception as e:
            title = ''
            thumbnail = ''
            logger.debug(e)
            pass

        return {
            'stream_url': stream_url,
            'meta': {
                'title': title,
                'thumbnail': thumbnail,
            },
        }
