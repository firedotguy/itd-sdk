from time import sleep

import pytest

from itd.post import Post
from itd.exceptions import NotFound


@pytest.fixture(autouse=True)
def _rate_limit():
    yield
    sleep(0.5)


@pytest.fixture(scope="module")
def owned_post(client):
    post = Post.new('тест комментарии', client=client)
    yield post
    try:
        post.delete(client)
    except NotFound:
        pass


@pytest.fixture
def comments(redis_post):
    redis_post.comments.clear()
    redis_post.comments._total = None
    redis_post.comments.has_more = True
    return redis_post.comments


def test_comments_load(comments):
    comments.load(3)
    assert len(comments) == 3


def test_comments_load_all(comments):
    comments.load_all()
    assert len(comments) == comments.total
    assert not comments.has_more


def test_comments_has_more(comments):
    assert comments.has_more
    comments.load(1)
    assert comments.has_more


def test_comments_refresh(comments):
    comments.load(5)
    comments.refresh(2)
    assert len(comments) == 2

BIG_POST_ID = '001d549a-dd4d-43c1-8cc7-aeab20e8ee85'
BIG_COMMENT_ID = '970f5b0f-bbf7-493c-a24c-223c44e2cd52'


@pytest.fixture(scope="module")
def big_post(client):
    post = Post(BIG_POST_ID, client)
    post.refresh(client)
    return post


def test_big_post_load_all_comments(big_post):
    big_post.comments.clear()
    big_post.comments.has_more = True
    big_post.comments.load_all()
    assert len(big_post.comments) == big_post.comments_count
    assert not big_post.comments.has_more


def test_big_post_no_duplicate_comments(big_post):
    ids = [c.id for c in big_post.comments]
    assert len(ids) == len(set(ids))


def test_big_comment_load_all_replies(big_post):
    comment = next(c for c in big_post.comments if str(c.id) == BIG_COMMENT_ID)
    comment.replies.clear()
    comment.replies.has_more = True
    comment.replies.load_all()
    assert len(comment.replies) == comment.replies_count


def test_big_comment_no_duplicate_replies(big_post):
    comment = next(c for c in big_post.comments if str(c.id) == BIG_COMMENT_ID)
    ids = [r.id for r in comment.replies]
    assert len(ids) == len(set(ids))
