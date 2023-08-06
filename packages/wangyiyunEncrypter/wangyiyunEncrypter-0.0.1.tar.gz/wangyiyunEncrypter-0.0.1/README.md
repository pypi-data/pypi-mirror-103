1. Requirements: execjs 
 
        pip install pyexecjs

2. Call function:

    (1) Import:

        from wangyiyunEncrypter.encrypter import WangyiyunEncrypter
        
    (2) Construct keywords' data to search songs:
     
        encrypted_search_data = WangyiyunEncrypter().construct_search_data(keywords=keywords, limit=limit)

    (3) Construct song's data to get its real url:
        
        encrypted_song_data = WangyiyunEncrypter().construct_song_data(song_id=song_id)
        
    (4) Construct lyric's data to get lyric:
    
        encrypted_lyric_data = WangyiyunEncrypter().construct_lyric_data(song_id=song_id)

    (5) Construct comments' data to get the comments:
    
        encrypted_comments_data = WangyiyunEncrypter().construct_comments_data(pageNo=pageNo, pageSize=pageSize, song_id=song_id)
        
    (6) Params:
        
     - keywords: the song's name or artist's name you want to search for
     - limit: the amounts of the search results you want
     - song_id: the music id
     - pageNo: the order number of the pages of comments
     - pageSize: comments amounts in per page