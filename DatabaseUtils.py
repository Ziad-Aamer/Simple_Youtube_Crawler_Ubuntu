import pymysql
import urllib

conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="123456", db="youtube_crawler")
cur = conn.cursor()


class DatabaseUtils:

    def insert_video(self, vid):
        views_count = '-1'
        if vid.get('statistics') is not None:
            views_count = vid['statistics'].get('viewCount')

        sql = "INSERT INTO `videos` (`video_url`, `title`, `duration`,`views`,`thumbnail_image`, " \
              "`original_image`) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (vid['id'], vid['snippet']['title'], vid['contentDetails'].get('duration'), views_count,
                          self.save_image(vid['snippet']['thumbnails']['default']['url'], vid['id'] + '_default'),
                          self.save_image(vid['snippet']['thumbnails'].get('high').get('url'),
                                          vid['id'] + '_original')))
        conn.commit()


    def insert_all_videos(self, videos):

        self.delete_table()
        for vid in videos:
            self.insert_video(vid)

        print("All Videos inserted successfully")


    def save_image(self, image_url, image_name):
        image_name = 'images//' + image_name + '.jpg'
        try:
            f = open(image_name, 'wb')
            f.write(urllib.urlopen(image_url).read())
            f.close()
        except ValueError:
            print(ValueError)

        return image_name

    def update_videos(self, videos, new_videos_url, old_videos_url):

        for vid in videos:
            if old_videos_url.get(vid['id']) is not None:
                #only update views
                views_count = '-1'
                if vid.get('statistics') is not None:
                    views_count = vid['statistics'].get('viewCount')

                sql = "UPDATE `videos` SET `views`=%s WHERE video_url=%s"
                cur.execute(sql, (views_count, vid['id']))
                conn.commit()

            else:
                #does not exist in db ==> insert vid
                self.insert_video(vid)
                print(vid['snippet']['title'] + " inserted successfully")

        for key, value in old_videos_url.iteritems():
            if new_videos_url.get(key) is None:
                #it does not exist in new videos list ==> delete form db also
                self.delete_vidoe(key)

        print("All Videos updated successfully")


    def delete_vidoe(self, vid_url):

        sql = "DELETE FROM `videos` where `video_url` = %s"
        cur.execute(sql, vid_url)
        conn.commit()

        print(vid_url + " Deleted")

    def delete_table(self):

        sql = "DELETE FROM `videos`"
        cur.execute(sql)
        conn.commit()

        print("all videos Deleted")

    def retrieve_videos_urls(self):
        sql = "SELECT `video_url` FROM `videos`"
        cur.execute(sql)
        dictt = {}
        for url in cur:
            dictt[url] = True

        return dictt
