import os
import sys

sys.path.insert(0, "/home/bojan/dev/privatno/git/timezonedb")

from timezonedb import TimezoneDBAPI

api = TimezoneDBAPI(api_key="YPX6FVA7ISOC")

print("TEST list_time_zone")
res = api.list_time_zone(
    response_format="json",
)
print(res)
res = api.list_time_zone(
    response_format="json",
    country="NZ",
)
print(res)


print("TEST get_time_zone")
res = api.get_time_zone(
    response_format="json",
    by="position",
    lat="40.689247",
    lng="-74.044502",
)
print(res)
res = api.get_time_zone(
    response_format="json",
    by="city",
    city="chicago",
    country="US",
)
print(res)

print("TEST convert_time_zone")
res = api.convert_time_zone(
    response_format="json",
    from_zone="America/Los_Angeles",
    to_zone="Australia/Sydney",
)
print(res)
