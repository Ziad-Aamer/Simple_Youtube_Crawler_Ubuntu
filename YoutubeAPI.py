import requests
API_KEY = "AIzaSyA-MLX23j0AkxTt7FGvjYuC2kO3lP_-Ie0"


class YoutubeAPI:

    def __init__(self):
        self.request_url = ""

    def get_playlist_videos(self, playlist_id):

        request_url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails' \
                      '&fields=nextPageToken%2Citems(contentDetails(videoId))'
        parameters = {"playlistId": playlist_id, "key": API_KEY, "maxResults": 50}

        response = requests.get(request_url, params=parameters)
        videos = response.json()['items']
        nxt_page = response.json().get('nextPageToken')

        try:
            while nxt_page is not None:
                parameters = {"playlistId": playlist_id, "key": API_KEY, "maxResults": 50,
                              "pageToken": nxt_page}
                response = requests.get(request_url, params=parameters)
                videos.extend(response.json()['items'])
                nxt_page = response.json().get('nextPageToken')

        except ValueError:
            print(ValueError)
        #print(videos)

        return videos


    def get_videos(self, videos):
        request_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet%2Cstatistics%2CcontentDetails' \
                      '&fields=nextPageToken%2Citems(id%2Csnippet(title%2Cthumbnails(default(url)%2Chigh(url)))' \
                      '%2CcontentDetails(duration)%2Cstatistics(viewCount))'

        videos_list = []
        request_num = (len(videos)+49)/50
        for k in range(0, request_num):
            k *= 50
            videos_ids = ''
            sz = min(k+50, len(videos))

            for i in range(k, sz-1):
                videos_ids += videos[i]['contentDetails']['videoId'] + ','
            videos_ids += videos[sz-1]['contentDetails']['videoId']

            print(videos_ids)
            #videos_ids = 'MH3FlMer5YY,8qIU5vQJHlQ,Q8uFbbSq1W4'
            parameters = {"id": videos_ids, "key": API_KEY, "maxResults": 50}
            response = requests.get(request_url, params=parameters)

            videos_res = response.json().get('items')
            if videos_res is not None:
                videos_list.extend(videos_res)
                #print(videos_res)
            else:
                print("videos_res is None")


        return videos_list

    def get_uploads_id(self, channel_name):
        request_url = 'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&fields=items(contentDetails' \
                      '(relatedPlaylists(uploads)))'
        parameters = {"forUsername": channel_name, "key": API_KEY}

        response = requests.get(request_url, params=parameters)
        uploads_id = response.json()['items'][0]['contentDetails']['relatedPlaylists'].get('uploads')

        return uploads_id
