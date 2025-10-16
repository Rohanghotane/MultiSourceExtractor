import instaloader
import pandas as pd

def scrape_instagram_post(shortcode):
    L = instaloader.Instaloader(download=False, save_metadata=False, compress_json=False)
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    likes = post.likes
    comments = post.comments
    comment_list = []
    for c in post.get_comments():
        comment_list.append({"Commenter": c.owner_username, "Comment": c.text})
    df_comments = pd.DataFrame(comment_list)
    return {"likes": likes, "comments_count": comments, "comments_df": df_comments}
