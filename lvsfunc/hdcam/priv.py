from warnings import warn

__all__: list[str] = [
    '_warn_hdcam',
    'hdcam_productions'
]


def _warn_hdcam() -> None:
    warn(
        "lvsfunc.hdcam: These are all experimental functions and will almost certainly be deprecated in the future! "
        "Please report any issues you find in the #dev channel in the JET discord!"
    )


# Set of HDCAM productions, kept for no reason other than for people to grab sources to test these funcs on.
# This should be moved to some kind of wiki or something, honestly.
hdcam_productions = {
    "Hayate no Gotoku",
    "Zettai Karen Children",
    "One Piece",
    "Heartcatch! Precure",
    "Joshiraku",
    "Kyousougiga",
    "Heavy Object",
    "Selector Infected WIXOSS",
    "DATE A LIVE"
}
