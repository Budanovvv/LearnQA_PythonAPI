def test_phrase_len():
    phrase = input("Set a phrase: ")
    assert len(phrase) <= 15, f"Phrase is more than 15 characters, it is {len(phrase)} characters long"
