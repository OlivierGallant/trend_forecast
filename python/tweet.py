class Tweet:
    def __init__(self, user, user_id, content, date, comments, reposts, likes):
        self.user = user
        self.user_id = user_id
        self.content = content
        self.comments = comments
        self.reposts = reposts
        self.likes = likes
        self.date = date
        self.date_list = self.reformat_date(date)

        self.year = self.date_list[0]
        self.month = self.date_list[1]
        self.day = self.date_list[2]
        self.hour = self.date_list[3]
        self.minute = self.date_list[4]
        self.second = self.date_list[5]

        self.delta_tweet = 0

    def reformat_date(self, date): 
        date = date.replace('-', ',')
        date = date.replace('T', ',')
        date = date.replace(':', ',') 
        date = date.replace('.', ',')
        date = date.replace('Z', '')
        return date.split(',')

    def get_content(self): return self.content
    
    def get_user(self): return self.user

    def get_user_id(self): return self.user_id
    def get_date(self): return self.date

    def get_comments(self): return self.comments

    def get_reposts(self): return self.reposts

    def get_likes(self): return self.likes

    def get_year(self): return self.year

    def get_month(self): return self.month
    
    def get_day(self): return self.day

    def get_hour(self): return self.hour

    def get_minute(self): return self.minute

    def get_second(self): return self.second
    
    def get_delta_tweet(self): return self.delta_tweet
    
    def print_tweet(self): return ([self.content, self.user, self.date, self.comments, self.reposts, self.likes])

    def set_delta_tweet(self, value): self.delta_tweet = value
