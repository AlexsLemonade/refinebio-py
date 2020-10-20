import pyrefinebio

ds = pyrefinebio.Dataset.get("9baf18b5-b2f5-4b80-8327-dcc1b1f13284")

ds.process()

print(ds.is_processing)
print(ds.check())