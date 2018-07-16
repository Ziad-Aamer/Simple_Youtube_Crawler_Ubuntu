"""
this crawler uses Youtube APIs to get info about the videos 
There are 3 types of requests ==> 
1. get videos IDs by playlist id from Youtube API
2. get videos info by videos ids 
3. get channel uploaded videos list id by channel name

//
using these requests we can handle the 2 types of formats:
1. getting videos info using playlist id :
    we first call get vidoes IDs then call get videos info
2. getting videos info using channel name:
    we first get uploaded list id then we do the same steps as 
    format one

//Design
1. we have the YotubeAPI class where we have the requests to the youtube API

2. DatabaseUtis where we interact with the database 

3. the main where we run the program

4. i am using dictionaries to compare between videos_saved in the database and the new ones
 this makes it more efficient to check whether items exist or not

5. as Youtube requests are limited by 50 per requests, i need to recall the api to get the rest of videos
 so i am using list to extend it upon next requests 

6. also handling many cases like the None value return where the views could be private or not available

7. the 2 types of images are saved in the images folder 


// how it works ?
*we need to either provide a list id or channel name as mentioned above, 
when we run all videos info will be saved into DB
*if the update flag was true at the beginning, this means that we already have items saved in DB
and only need to update the list
*the update happens every minute (60 seconds) as follows:
    1. if an item exist in the DB only update the viewsCount
    2. if an item does not exist in DB, then insert it 
    3. if item exist in DB, but does not exist in the new videos list, then it is deleted from the DB

//test
1. install all the required modules and create the database as specified
2. u can test the diffrenet formats by giving the playlist id and the channel name
3. to test the update it is better to create a playlist on youtube, add and delete videos and watch how they
changed and get updated in the database

 
"""
