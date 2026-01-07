from wagtail.blocks import StructBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock

class PaymentAndDeliveryInfoSectionBlock(StructBlock):
    image = ImageChooserBlock()
    description =  RichTextBlock()

    class Meta:
        icon = "image"
        label = "Payment and delivery info section block"