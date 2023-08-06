# little-shelf
Synchronized dictionaries using [Greg Little][0]'s `shelf` CRDT.

Changes/patches can be distributed to peers through any channel. See the
[understory][1]'s [Braid][2] implementation as an example of real world usage.

# Install

    pip install little-shelf

# Use

    >>> import littleshelf
    >>> alice = littleshelf.LittleShelf()
    >>> bob = littleshelf.LittleShelf()
    >>> patch = alice.set(ham="spam")
    >>> patch
    [{'ham': ['spam', 0]}, 0]
    >>> alice
    {'ham': 'spam'}
    >>> alice == bob
    False
    >>> bob.merge(patch)
    >>> alice == bob
    True
    >>> bob.get("ham") == bob["ham"] == "spam"
    True

[0]: //glittle.org
[1]: //github.com/angelogladding/understory/blob/main/understory/web/braid.py
[2]: //braid.org
