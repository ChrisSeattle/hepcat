from django.test import TestCase, TransactionTestCase
from classwork.models import Session  # , Subject, ClassOffer, Location, Profile, Registration, Payment
from datetime import date, timedelta

# Create your tests here.
INITIAL = {
    "name": "May_2020",
    "key_day_date": "2020-04-30",
    "max_day_shift": -2,
    "num_weeks": 5,
    "expire_date": "2020-05-08",
}
# second_sess = {
#     "name": "early_no_skip",
#     "max_day_shift": -2,
#     "num_weeks": 5,
# }
# no_skip = 'tests/db_early_no_skip_session.json'  # max_day_shift=-2, skip_weeks=0, num_weeks=5
# oth_skip = 'tests/db_early1_oth_skip_session.json'  # max_day_shift=-2, skip_weeks=1, flip_last_day=True, num_weeks=5
# second_skips = 3


class SessionDateAfterNoSkip(TransactionTestCase):
    fixtures = ['tests/db_basic.json', 'tests/db_early_no_skip_session.json']

    def create_session(self, **kwargs):
        obj = Session.objects.create(**kwargs)
        # obj.refresh_from_db()
        return obj

    def test_dates_skips_key_date_early_shift(self):
        """ Session with early shift and 1 skip week on the key day. """
        skips, day_adjust, duration = 1, -2, INITIAL['num_weeks']
        key_day = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*2*duration)
        publish = date.fromisoformat(INITIAL['expire_date']) + timedelta(days=7*duration)
        expire = key_day + timedelta(days=8)
        start = key_day + timedelta(days=day_adjust)
        end = key_day + timedelta(days=7*(duration + skips - 1))
        prev_end = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*(2 * duration - 1))
        sess = Session.objects.create(
            name='early_key_skip',
            max_day_shift=day_adjust,
            num_weeks=duration,
            skip_weeks=skips,
            flip_last_day=False,
            )
        self.assertEquals(sess.key_day_date, key_day)
        self.assertEquals(sess.publish_date, publish)
        self.assertEquals(sess.expire_date, expire)
        self.assertEquals(sess.start_date, start)
        self.assertEquals(sess.end_date, end)
        self.assertEquals(sess.prev_session.expire_date, sess.publish_date)
        self.assertLess(sess.prev_session.end_date, sess.start_date)
        self.assertEquals(sess.prev_session.end_date, prev_end)

    def test_dates_skips_key_date_late_shift(self):
        """ Session with late shift and 1 skip week on the key day, flipping last class day. """
        skips, day_adjust, duration = 1, 5, INITIAL['num_weeks']
        key_day = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*2*duration)
        publish = date.fromisoformat(INITIAL['expire_date']) + timedelta(days=7*duration)
        expire = key_day + timedelta(days=8+day_adjust)
        start = key_day
        end = key_day + timedelta(days=7*(duration + skips - 1))
        prev_end = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*(2 * duration - 1))
        sess = Session.objects.create(
            name='late_key_skip',
            max_day_shift=day_adjust,
            num_weeks=duration,
            skip_weeks=skips,
            flip_last_day=True,
            )
        self.assertEquals(sess.key_day_date, key_day)
        self.assertEquals(sess.publish_date, publish)
        self.assertEquals(sess.expire_date, expire)
        self.assertEquals(sess.start_date, start)
        self.assertEquals(sess.end_date, end)
        self.assertEquals(sess.prev_session.expire_date, sess.publish_date)
        self.assertLess(sess.prev_session.end_date, sess.start_date)
        self.assertEquals(sess.prev_session.end_date, prev_end)

    def test_dates_skips_other_date_early_shift(self):
        """ Session with early shift and 1 skip week NOT on the key day, flipping last class day. """
        skips, day_adjust, duration = 1, -2, INITIAL['num_weeks']
        key_day = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*2*duration)
        publish = date.fromisoformat(INITIAL['expire_date']) + timedelta(days=7*duration)
        expire = key_day + timedelta(days=8)
        start = key_day + timedelta(days=day_adjust)
        end = key_day + timedelta(days=7*(duration + skips - 1)+day_adjust)
        prev_end = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*(2 * duration - 1))
        sess = Session.objects.create(
            name='early2_oth_skip',
            max_day_shift=day_adjust,
            num_weeks=duration,
            skip_weeks=skips,
            flip_last_day=True,
            )
        self.assertEquals(sess.key_day_date, key_day)
        self.assertEquals(sess.publish_date, publish)
        self.assertEquals(sess.expire_date, expire)
        self.assertEquals(sess.start_date, start)
        self.assertEquals(sess.end_date, end)
        self.assertEquals(sess.prev_session.expire_date, sess.publish_date)
        self.assertLess(sess.prev_session.end_date, sess.start_date)
        self.assertEquals(sess.prev_session.end_date, prev_end)

    def test_dates_skips_other_date_late_shift(self):
        """ Session with late shift and 1 skip week NOT on the key_day. """
        skips, day_adjust, duration = 1, 5, INITIAL['num_weeks']
        key_day = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*2*duration)
        publish = date.fromisoformat(INITIAL['expire_date']) + timedelta(days=7*duration)
        expire = key_day + timedelta(days=8+day_adjust)
        start = key_day
        end = key_day + timedelta(days=7*(duration + skips - 1)+day_adjust)
        prev_end = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*(2 * duration - 1))
        sess = Session.objects.create(
            name='late_oth_skip',
            max_day_shift=day_adjust,
            num_weeks=duration,
            skip_weeks=skips,
            flip_last_day=False,
            )
        self.assertEquals(sess.key_day_date, key_day)
        self.assertEquals(sess.publish_date, publish)
        self.assertEquals(sess.expire_date, expire)
        self.assertEquals(sess.start_date, start)
        self.assertEquals(sess.end_date, end)
        self.assertEquals(sess.prev_session.expire_date, sess.publish_date)
        self.assertLess(sess.prev_session.end_date, sess.start_date)
        self.assertEquals(sess.prev_session.end_date, prev_end)


class SessionDateAfterEarlyOtherSkip(SessionDateAfterNoSkip):
    fixtures = ['tests/db_basic.json', 'tests/db_early1_oth_skip_session.json']


# class SessionDateAfterEarlyOtherSkip(TransactionTestCase):
#     fixtures = ['tests/db_basic.json', 'tests/db_early1_oth_skip_session.json']

#     def create_session(self, **kwargs):
#         obj = Session.objects.create(**kwargs)
#         # obj.refresh_from_db()
#         return obj

#     def test_dates_skips_key_date_early_shift(self):
#         """ Session with early shift and 1 skip week on the key day. """
#         skips, day_adjust, duration = 1, -2, INITIAL['num_weeks']
#         key_day = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*2*duration)
#         publish = date.fromisoformat(INITIAL['expire_date']) + timedelta(days=7*duration)
#         expire = key_day + timedelta(days=8)
#         start = key_day + timedelta(days=day_adjust)
#         end = key_day + timedelta(days=7*(duration + skips - 1))
#         prev_end = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*(2 * duration - 1))
#         sess = Session.objects.create(
#             name='early_key_skip',
#             max_day_shift=day_adjust,
#             num_weeks=duration,
#             skip_weeks=skips,
#             flip_last_day=False,
#             )
#         self.assertEquals(sess.key_day_date, key_day)
#         self.assertEquals(sess.publish_date, publish)
#         self.assertEquals(sess.expire_date, expire)
#         self.assertEquals(sess.start_date, start)
#         self.assertEquals(sess.end_date, end)
#         self.assertEquals(sess.prev_session.expire_date, sess.publish_date)
#         self.assertLess(sess.prev_session.end_date, sess.start_date)
#         self.assertEquals(sess.prev_session.end_date, prev_end)

#     def test_dates_skips_key_date_late_shift(self):
#         """ Session with late shift and 1 skip week on the key day, flipping last class day. """
#         skips, day_adjust, duration = 1, 5, INITIAL['num_weeks']
#         key_day = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*2*duration)
#         publish = date.fromisoformat(INITIAL['expire_date']) + timedelta(days=7*duration)
#         expire = key_day + timedelta(days=8+day_adjust)
#         start = key_day
#         end = key_day + timedelta(days=7*(duration + skips - 1))
#         prev_end = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*(2 * duration - 1))
#         sess = Session.objects.create(
#             name='late_key_skip',
#             max_day_shift=day_adjust,
#             num_weeks=duration,
#             skip_weeks=skips,
#             flip_last_day=True,
#             )
#         self.assertEquals(sess.key_day_date, key_day)
#         self.assertEquals(sess.publish_date, publish)
#         self.assertEquals(sess.expire_date, expire)
#         self.assertEquals(sess.start_date, start)
#         self.assertEquals(sess.end_date, end)
#         self.assertEquals(sess.prev_session.expire_date, sess.publish_date)
#         self.assertLess(sess.prev_session.end_date, sess.start_date)
#         self.assertEquals(sess.prev_session.end_date, prev_end)

#     def test_dates_skips_other_date_early_shift(self):
#         """ Session with early shift and 1 skip week NOT on the key day, flipping last class day. """
#         skips, day_adjust, duration = 1, -2, INITIAL['num_weeks']
#         key_day = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*2*duration)
#         publish = date.fromisoformat(INITIAL['expire_date']) + timedelta(days=7*duration)
#         expire = key_day + timedelta(days=8)
#         start = key_day + timedelta(days=day_adjust)
#         end = key_day + timedelta(days=7*(duration + skips - 1)+day_adjust)
#         prev_end = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*(2 * duration - 1))
#         sess = Session.objects.create(
#             name='early2_oth_skip',
#             max_day_shift=day_adjust,
#             num_weeks=duration,
#             skip_weeks=skips,
#             flip_last_day=True,
#             )
#         self.assertEquals(sess.key_day_date, key_day)
#         self.assertEquals(sess.publish_date, publish)
#         self.assertEquals(sess.expire_date, expire)
#         self.assertEquals(sess.start_date, start)
#         self.assertEquals(sess.end_date, end)
#         self.assertEquals(sess.prev_session.expire_date, sess.publish_date)
#         self.assertLess(sess.prev_session.end_date, sess.start_date)
#         self.assertEquals(sess.prev_session.end_date, prev_end)

#     def test_dates_skips_other_date_late_shift(self):
#         """ Session with late shift and 1 skip week NOT on the key_day. """
#         skips, day_adjust, duration = 1, 5, INITIAL['num_weeks']
#         key_day = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*2*duration)
#         publish = date.fromisoformat(INITIAL['expire_date']) + timedelta(days=7*duration)
#         expire = key_day + timedelta(days=8+day_adjust)
#         start = key_day
#         end = key_day + timedelta(days=7*(duration + skips - 1)+day_adjust)
#         prev_end = date.fromisoformat(INITIAL['key_day_date']) + timedelta(days=7*(2 * duration - 1))
#         sess = Session.objects.create(
#             name='late_oth_skip',
#             max_day_shift=day_adjust,
#             num_weeks=duration,
#             skip_weeks=skips,
#             flip_last_day=False,
#             )
#         self.assertEquals(sess.key_day_date, key_day)
#         self.assertEquals(sess.publish_date, publish)
#         self.assertEquals(sess.expire_date, expire)
#         self.assertEquals(sess.start_date, start)
#         self.assertEquals(sess.end_date, end)
#         self.assertEquals(sess.prev_session.expire_date, sess.publish_date)
#         self.assertLess(sess.prev_session.end_date, sess.start_date)
#         self.assertEquals(sess.prev_session.end_date, prev_end)


# end class SessionDateTests

# end of test.py file
