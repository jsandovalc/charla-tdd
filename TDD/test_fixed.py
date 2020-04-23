from fixed import WordCount

def test_count_case():
    wc = WordCount()
    wc.add("ALL")
    wc.add("All")
    assert wc.count("All") == wc.count("ALL")
