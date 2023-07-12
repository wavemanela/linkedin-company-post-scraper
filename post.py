from datetime import datetime

class Post():
    def __init__(self, update):
        self.update = update

    def get_id(self):
        try:
            return int(self.update['id'].split(':')[1])
        except:
            return 0

        return 
    
    def get_date(self):
        id = self.get_id()
        if id == 0:
            return datetime.utcfromtimestamp(0)
        binary = bin(id)[2:]
        binary_timestamp = binary[:41]
        decimal_timestamp = int(binary_timestamp, 2)
        timestamp_sec = decimal_timestamp / 1000
        return datetime.utcfromtimestamp(timestamp_sec)
    
    def get_link(self):
        try:
            return self.update['permalink']
        except:
            return "" 
    
    def get_text(self):
        try:
            return self.update['value']['com.linkedin.voyager.feed.render.UpdateV2']['commentary']['text']['text']
        except:
            return ""
    
    def get_num_shares(self):
        try:
            return self.update['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts']['numShares']
        except:
            return 0
    
    def get_num_likes(self):
        try:
            data = self.update['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts']['reactionTypeCounts']
        except:
            return 0
        likes = None

        for item in data:
            if item['reactionType'] == 'LIKE':
                likes = item['count']
                break
        
        return likes
    
    def get_num_empathy(self):
        try:
            data = self.update['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts']['reactionTypeCounts']
        except:
            return 0
        empathy = None

        for item in data:
            if item['reactionType'] == 'EMPATHY':
                empathy = item['count']
                break
        
        return empathy
    
    def get_num_appreciation(self):
        try:
            data = self.update['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts']['reactionTypeCounts']
        except:
            return 0
        appreciations = None

        for item in data:
            if item['reactionType'] == 'APPRECIATION':
                appreciations = item['count']
                break
        
        return appreciations
    
    def get_num_praise(self):
        try:
            data = self.update['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts']['reactionTypeCounts']
        except:
            return 0
        praises = None

        for item in data:
            if item['reactionType'] == 'PRAISE':
                praises = item['count']
                break
        
        return praises
    
    def get_num_interest(self):
        try:
            data = self.update['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts']['reactionTypeCounts']
        except:
            return 0
        interests = None

        for item in data:
            if item['reactionType'] == 'INTEREST':
                interests = item['count']
                break
        
        return interests
    