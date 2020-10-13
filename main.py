import pyrefinebio

s =  pyrefinebio.Sample.get("SRR5445147")

for e in s.experiments:
    print(e.id)