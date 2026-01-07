from wagtail.blocks import StructBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock

class CustomerInfoBlock(StructBlock):
    image = ImageChooserBlock()
    description =  RichTextBlock()

    class Meta:
        icon = "image"
        label = "Customer info block"