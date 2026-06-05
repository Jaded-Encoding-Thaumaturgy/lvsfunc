from lvsfunc.color import RGBColor


def test_rgb_color() -> None:
    """Test the RGBColor enum."""

    assert RGBColor.RED == (1.0, 0.0, 0.0)
    assert RGBColor.GREEN == (0.0, 1.0, 0.0)
    assert RGBColor.BLUE == (0.0, 0.0, 1.0)
