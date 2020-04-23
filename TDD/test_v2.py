from fixed import WordCount


def test_count_case():
    """WordCount.case() retorna el conteo correcto para una palabra sin
    importar mayúsculas.

    """
    wc = WordCount()
    wc.add("All")
    wc.add("ALL")

    assert (wc.count("All"), wc.count("ALL")) == (2, 2)
