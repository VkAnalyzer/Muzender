import pytest

from parser import VkParser


def test_get_user_id():
    parser = VkParser()

    user_id = parser.get_user_id('vk.com/id123')
    assert type(user_id) is int
    assert user_id == 123

    user_id = parser.get_user_id('http://vk.com/typikl')
    assert  user_id == 4617715

    user_id = parser.get_user_id('http://vk.com/no_such_user_for_sure')
    assert user_id is None

def test_get_aser_audio():
    parser = VkParser()
    user_id = 4617715
    user_audio = parser.get_users_audio(parser.vk_session, user_id)
    assert type(user_audio[0]) is dict
    assert user_audio[0].get('artist', False)
    assert user_audio[0].get('title', False)
    assert user_audio[0].get('dur', False)
    assert user_audio[0].get('id', False)
    assert user_audio[0].get('url', False)
