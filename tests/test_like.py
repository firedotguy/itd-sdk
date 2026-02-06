from itd import ITDClient
from itd.models.post import LikePostResponse
from itd.exceptions import NotFound
import unittest
from . import settings

class TestLike(unittest.TestCase):
    def test_like(self):
        c = ITDClient(None, settings.cookies)

        post = c.create_post("post_for_test_like")

        self.assertEqual(c.like_post(post.id), LikePostResponse(liked=True, likesCount=1)) # Лайк на пост без лайка
        self.assertEqual(c.like_post(post.id), LikePostResponse(liked=True, likesCount=1)) # Лайк на пост с уже поставленным лайком

        self.assertEqual(c.delete_like_post(post.id), LikePostResponse(liked=False, likesCount=0)) # Убрать лайк с поста с уже поставленным лайком
        self.assertEqual(c.delete_like_post(post.id), LikePostResponse(liked=False, likesCount=0)) # Убрать лайк с поста без лайков

        c.delete_post(str(post.id))

        self.assertRaises(NotFound, c.like_post, post.id) # лайк на удалённый пост
        self.assertRaises(NotFound, c.delete_like_post, post.id) # Убрать лайк с удалённого поста


if __name__ == "__main__":
    unittest.main()
