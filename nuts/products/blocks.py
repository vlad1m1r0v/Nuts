from wagtail.blocks import StructBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock

class ProductImageWithTextBlock(StructBlock):
    image = ImageChooserBlock()
    text = RichTextBlock()

    class Meta:
        icon = "image"
        label = "Image with text block"