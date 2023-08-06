from .http import HTTPHandler
from .objects import *


class Client:
    def __init__(self, auth):
        self.auth = auth
        self.http = HTTPHandler(auth)

    def lookup_beatmap(self, checksum=None, filename=None, id=None):
        return Beatmap(self.http.get(Path.beatmap_lookup(), checksum=checksum, filename=filename, id=id))

    def get_user_beatmap_score(self, beatmap, user, mode=None, mods=None):
        return BeatmapUserScore(self.http.get(Path.user_beatmap_score(beatmap, user), mode=mode, mods=mods))

    def get_beatmap_scores(self, beatmap, mode=None, mods=None, type=None):
        return BeatmapScores(self.http.get(Path.beatmap_scores(beatmap), mode=mode, mods=mods, type=type))

    def get_beatmap(self, beatmap):
        return Beatmap(self.http.get(Path.beatmap(beatmap)))

    def get_beatmapset_discussion_posts(self, beatmapset_discussion_id=None, limit=None, page=None, sort=None, user=None, with_deleted=None):
        # TODO: Change is supposed to occur on the response given back from the server, make sure to change it when that happens.
        resp = self.http.get(Path.beatmapset_discussion_posts(), beatmapset_discussion_id=beatmapset_discussion_id,
                             limit=limit, page=page, sort=sort, user=user, with_deleted=with_deleted)
        return {
            'beatmapsets': BeatmapsetCompact(resp['beatmapsets']),
            'cursor': Cursor(resp['cursor']),
            'posts': [BeatmapsetDiscussionPost(post) for post in resp['posts']],
            'users': UserCompact(resp['users'])
        }

    def get_beatmapset_discussion_votes(self, beatmapset_discussion_id=None, limit=None, page=None, receiver=None, score=None, sort=None, user=None, with_deleted=None):
        # TODO: Change is supposed to occur on the response given back from the server, make sure to change it when that happens.
        resp = self.http.get(Path.beatmapset_discussion_votes(), beatmapset_discussion_id=beatmapset_discussion_id,
                             limit=limit, receiver=receiver, score=score, page=page, sort=sort, user=user, with_deleted=with_deleted)
        return {
            'cursor': Cursor(resp['cursor']),
            'discussions': BeatmapsetDiscussion(resp['discussions']),
            'users': UserCompact(resp['users']),
            'votes': [BeatmapsetDiscussionVote(vote) for vote in resp['votes']]
        }

    def get_beatmapset_discussions(self, beatmap_id=None, beatmapset_id=None, beatmapset_status=None, limit=None, message_type=None, only_unresolved=None, page=None, sort=None, user=None, with_deleted=None):
        # TODO: Change is supposed to occur on the response given back from the server, make sure to change it when that happens.
        resp = self.http.get(Path.beatmapset_discussions(), beatmap_id=beatmap_id, beatmapset_id=beatmapset_id,
                             beatmapset_status=beatmapset_status, limit=limit, message_type=message_type,
                             only_unresolved=only_unresolved, page=page, sort=sort, user=user, with_deleted=with_deleted)
        return {
            'beatmaps': [Beatmap(beatmap) for beatmap in resp['beatmaps']],
            'cursor': Cursor(resp['cursor']),
            'discussions': [BeatmapsetDiscussion(disc) for disc in resp['discussions']],
            'included_discussions': [BeatmapsetDiscussion(disc) for disc in resp['included_discussions']],
            'reviews_config_max_blocks': resp['reviews_config_max_blocks'],
            'users': [UserCompact(user) for user in resp['users']]
        }

    def create_new_pm(self, target_id, message, is_action):
        data = {'target_id': target_id, 'message': message, 'is_action': is_action}
        resp = self.http.post(Path.create_new_pm(), data=data)
        return {
            'new_channel_id': resp['new_channel_id'],
            'presence': [ChatChannel(channel) for channel in resp['presence']],
            'message': ChatMessage(resp['message'])
        }

    def get_updates(self, since, channel_id=None, limit=None):
        resp = self.http.post(Path.get_updates(), since=since, channel_id=channel_id, limit=limit)
        return {
            'presence': [ChatChannel(channel) for channel in resp['presence']],
            'messages': [ChatMessage(msg) for msg in resp['messages']]
        }

    def get_channel_messages(self, channel_id, limit=None, since=None, until=None):
        return [ChatMessage(msg) for msg in self.http.post(Path.get_channel_messages(channel_id), limit=limit, since=since, until=until)]

    def send_message_to_channel(self, channel_id, message, is_action):
        data = {'message': message, 'is_action': is_action}
        return ChatMessage(self.http.post(Path.send_message_to_channel(channel_id), data=data))

    def join_channel(self, channel, user):
        return ChatChannel(self.http.put(Path.join_channel(channel, user)))

    def leave_channel(self, channel, user):
        self.http.delete(Path.leave_channel(channel, user))

    def mark_channel_as_read(self, channel, message, channel_id, message_id):
        self.http.put(Path.mark_channel_as_read(channel, message), channel_id=channel_id, message_id=message_id)

    def get_channel_list(self):
        return [ChatChannel(channel) for channel in self.http.get(Path.get_channel_list())]

    def create_channel(self, type, target_id=None):
        data = {'type': type, 'target_id': target_id}
        return ChatChannel(self.http.post(Path.create_channel(), data=data))

    def get_channel(self, channel):
        resp = self.http.get(Path.get_channel(channel))
        return {
            'channel': ChatChannel(resp['channel']),
            'users': UserCompact(resp['users']),
        }

    def get_comments(self, commentable_type=None, commentable_id=None, cursor=None, parent_id=None, sort=None):
        return CommentBundle(self.http.get(Path.get_comments(), commentable_type=commentable_type, commentable_id=commentable_id,
                                           cursor=cursor, parent_id=parent_id, sort=sort))

    def post_comment(self, commentable_id=None, commentable_type=None, message=None, parent_id=None):
        return CommentBundle(self.http.post(Path.post_new_comment(), commentable_id=commentable_id, commentable_type=commentable_type,
                                            message=message, parent_id=parent_id))

    def get_comment(self, comment):
        return CommentBundle(self.http.get(Path.get_comment(comment)))

    def edit_comment(self, comment, message=None):
        return CommentBundle(self.http.patch(Path.edit_comment(comment), message=message))

    def delete_comment(self, comment):
        return CommentBundle(self.http.delete(Path.delete_comment(comment)))

    def add_comment_vote(self, comment):
        return CommentBundle(self.http.post(Path.add_comment_vote(comment)))

    def remove_comment_vote(self, comment):
        return CommentBundle(self.http.delete(Path.remove_comment_vote(comment)))

    def reply_topic(self, topic, body):
        data = {'body': body}
        return ForumPost(self.http.post(Path.reply_topic(topic), data=data))

    def create_topic(self, body, forum_id, title, with_poll=None, hide_results=None, length_days=None, max_options=None, poll_options=None, poll_title=None, vote_change=None):
        data = {'body': body, 'forum_id': forum_id, 'title': title, 'with_poll': with_poll}
        if with_poll:
            if poll_options is None or poll_title is None:
                raise TypeError("poll_options and poll_title are required since the topic has a poll.")
            data.update({'forum_topic_poll': {
                'hide_results': hide_results,'length_days': length_days,
                'max_options': max_options, 'poll_options': poll_options,
                'poll_title': poll_title, 'vote_change': vote_change
            }})
        resp = self.http.post(Path.create_topic(), data=data)
        return {
            'topic': ForumTopic(resp['topic']),
            'post': ForumPost(resp['post'])
        }

    def get_topic_and_posts(self, topic, cursor=None, sort=None, limit=None, start=None, end=None):
        resp = self.http.get(Path.get_topic_and_posts(topic), cursor=cursor, sort=sort, limit=limit, start=start, end=end)
        return {
            'cursor': Cursor(resp['cursor']),
            'search': resp['search'],
            'posts': [ForumPost(post) for post in resp['posts']],
            'topic': ForumTopic(resp['topic'])
        }

    def edit_topic(self, topic, topic_title):
        data = {'forum_topic': {'topic_title': topic_title}}
        return ForumTopic(self.http.patch(Path.edit_topic(topic), data=data))

    def edit_post(self, post, body):
        data = {'body': body}
        return ForumPost(self.http.patch(Path.edit_post(post), data=data))

    def search(self, mode=None, query=None, page=None):
        resp = self.http.get(Path.search(), mode=mode, query=query, page=page)
        return {
            'user': {'results': resp['user']['data'], 'total': resp['user']['total']} if mode is None or mode is 'all' or mode is 'user' else None,
            'wiki_page': {'results': resp['wiki_page']['data'], 'total': resp['wiki_page']['total']} if mode is None or mode is 'all' or mode is 'wiki_page' else None
        }

    def get_user_highscore(self, room, playlist, user):
        # Doesn't say response type
        return self.http.get(Path.get_user_high_score(room, playlist, user))

    def get_scores(self, room, playlist, limit=None, sort=None, cursor=None):
        # Doesn't say response type
        return self.http.get(Path.get_scores(room, playlist), limit=limit, sort=sort, cursor=cursor)

    def get_score(self, room, playlist, score):
        # Doesn't sat response type
        return self.http.get(Path.get_score(room, playlist, score))

    def get_notification(self, max_id=None):
        resp = self.http.get(Path.get_notifications(), max_id=max_id)
        return {
            'has_more': resp['has_more'],
            'notifications': [Notification(notif) for notif in resp['notifications']],
            'unread_count': resp['unread_count'],
            'notification_endpoint': resp['notification_endpoint'],
        }

    def mark_notifications_read(self, ids):
        data = {'ids': ids}
        self.http.post(Path.mark_notifications_as_read(), data=data)

    def revoke_current_token(self):
        self.http.delete(Path.revoke_current_token())

    def get_ranking(self, mode, type, country=None, cursor=None, filter=None, spotlight=None, variant=None):
        return Rankings(self.http.get(Path.get_ranking(mode, type), country=country, cursor=cursor, filter=filter,
                                      spotlight=spotlight, variant=variant))

    def get_spotlights(self):
        return Spotlights(self.http.get(Path.get_spotlights()))

    def get_own_data(self, mode):
        return User(self.http.get(Path.get_own_data(mode)))

    def get_user_kudosu(self, user, limit=None, offset=None):
        return [KudosuHistory(kud) for kud in self.http.get(Path.get_user_kudosu(user), limit=limit, offset=offset)]

    def get_user_scores(self, user, type, include_fails=None, mode=None, limit=None, offset=None):
        return [Score(score) for score in self.http.get(Path.get_user_scores(user, type), include_fails=include_fails, mode=mode, limit=limit, offset=offset)]

    def get_user_beatmaps(self, user, type, limit=None, offset=None):
        return [Beatmapset(bm) for bm in self.http.get(Path.get_user_beatmaps(user, type), limit=limit, offset=offset)]

    def get_user_recent_activity(self, user, limit=None, offset=None):
        return [Event(event) for event in self.http.get(Path.get_user_recent_activity(user), limit=limit, offset=offset)]

    def get_user(self, user, mode='', key=None):
        return User(self.http.get(Path.get_user(user, mode), key=key))

    def get_users(self, ids):
        return [UserCompact(user) for user in self.http.get(Path.get_users(), ids=ids)]

    def get_wiki_page(self, locale, path, page):
        return WikiPage(self.http.get(Path.get_wiki_page(locale, path), page=page))

