from wagtail.blocks import StructBlock, CharBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock

class GalleryImageWithTextBlock(StructBlock):
    image = ImageChooserBlock(required=True)

    title = CharBlock(max_length=100)

    description = RichTextBlock()

    class Meta:
        icon = "image"
        label = "Image with text"