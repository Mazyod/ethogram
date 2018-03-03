"""
A bunch of utility methods to help in processing ugly inputs
"""

class Util:
    @classmethod
    def min_max_from_seq(cls, string):
        try:
            nums = [int(s) for s in string.split(" ")]
            return (min(nums), max(nums))
        except ValueError:
            return (0, 0)

    @classmethod
    def time_ago(cls, timestamp):
        s = int(timestamp)
        days, remainder = divmod(s, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        if days >= 1:
            return str(days) + "d"
        if hours >= 1:
            return str(hours) + "h"
        if minutes >= 1:
            return str(minutes) + "m"
            
        return str(seconds) + "s"
