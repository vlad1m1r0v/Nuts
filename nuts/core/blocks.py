from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, BooleanBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock


class StatisticItemBlock(StructBlock):
    value = CharBlock()
    unit = CharBlock()
    label = CharBlock()


class ImageJumbotronBlock(StructBlock):
    background_image = ImageChooserBlock()
    title = CharBlock(max_length=100)
    text = RichTextBlock(editor="minimal")
    show_top_image = BooleanBlock(default=True)

    class Meta:
        icon = "image"
        label = "Image Jumbotron"


class VideoJumbotronBlock(StructBlock):
    video = VideoChooserBlock()

    title = CharBlock(max_length=100)

    text_above_play_button = RichTextBlock(
        required=False,
        editor="minimal"
    )

    text_below_play_button = RichTextBlock(
        required=False,
        editor="minimal"
    )

    class Meta:
        icon = "media"
        label = "Video Jumbotron"
