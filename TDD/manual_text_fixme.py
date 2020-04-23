from fixme import WordCount

wc = WordCount()
wc.add("ALL")
wc.add("All")

# Hay un error en este test.
print(wc.count("All") == wc.count("ALL"))
