from cloudwatch_sns_to_slack import handler

def test_get_channel():
    assert(handler.get_channel() == 'test_channel')
