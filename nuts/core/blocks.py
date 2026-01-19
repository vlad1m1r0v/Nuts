from django.core.exceptions import ValidationError

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
    text = RichTextBlock(required=False)
    show_top_image = BooleanBlock(default=True, required=False)

    class Meta:
        icon = "image"
        label = "Image jumbotron"


class VideoJumbotronBlock(StructBlock):
    video = VideoChooserBlock()

    title = CharBlock(max_length=100)

    text_above_play_button = RichTextBlock(
        required=False,
        
    )

    text_below_play_button = RichTextBlock(
        required=False,
        
    )

    def clean(self, value):
        cleaned = super().clean(value)

        text_above = cleaned.get("text_above_play_button")
        text_below = cleaned.get("text_below_play_button")

        if not text_above and not text_below:
            raise ValidationError(
                "One of there fields must be filled: text above play button or text below play button."
            )

        return cleaned

    class Meta:
        icon = "media"
        label = "Video jumbotron"
