import json

class RedditPost:
    def __init__(self, post_info):
        post_dict = post_info['data']
        for key, value in post_dict.items():
            setattr(self, key, value)

    def __repr__(self):
        heading = f"{self.title}\nBy: {self.author} in {self.subreddit}"
        body = self.url
        return heading + '\n' + body

class SubredditListing:
    def __init__(self, listing_json):
        self.valid = False
        self.json = listing_json
        try:
            if self.json['kind'] != 'Listing':
                raise NotAListing
            else:
                pass
        except KeyError:
            raise TooManyRequests
        self.posts = list(map(RedditPost, self.json['data']['children']))

    def get_n_posts(self, n=5, ignore_stickies=True, ignore_self=True):
        posts = list()
        for post in self.posts:
            if len(posts) <= n:
                # There's probably a better way to do this...
                if ignore_stickies:
                    if not post.stickied:
                        if ignore_self:
                            if not post.is_self:
                                posts.append(post)
                        else:
                            posts.append(post)
                else:
                    if ignore_self:
                        if not post.is_self:
                            posts.append(post)
                    else:
                        posts.append(post)
            else:
                break
        return posts


if __name__ == "__main__":
    # Ghetto unit test
    with open('test.json', 'r') as test_file:
        test_json = json.loads(test_file.read())
        sl = SubredditListing(test_json)
        for post in sl.posts:
            print(f"{post}")
