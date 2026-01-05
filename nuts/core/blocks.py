from wagtail.blocks import StructBlock, CharBlock

class StatisticItemBlock(StructBlock):
    value = CharBlock()
    unit = CharBlock()
    label = CharBlock()