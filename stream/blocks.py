from django.db.models.fields import CharField
from wagtail.core import blocks
from wagtail.core.blocks.base import Block
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    titulo = blocks.CharBlock(required=True,help_text="Añade tu titulo")
    text = blocks.TextBlock(required=True,help_text="Añade tu texto aqui")

    class Meta:
        template = "stream/title_text.html" 
        icon = "edit"
        label = "Titulo y texto"   
class CardBlock(blocks.StructBlock):
    titulo = blocks.CharBlock(required=True,help_text="Añade tu titulo")
    cards = blocks.ListBlock(
        blocks.StructBlock([
            ("image",ImageChooserBlock(required=True)),
            ("titulo",blocks.CharBlock(required=True,max_length=40)),
            ("texto",blocks.TextBlock(required=True,max_length=200)),
            ("boton_page",blocks.PageChooserBlock(required=False)),
            ("boton_url",blocks.URLBlock(required=False,help_text="link"))
        ])
    )

    class Meta:
        template = "stream/card_block.html"
        icon = "edit"
        label = "Card Block"


class RichTextBlock(blocks.RichTextBlock):

    class Meta:
        template = "stream/richtext_block.html"
        icon = "edit"
        label = "Full RichText"

class SimpleRichTextBlock(blocks.RichTextBlock):

    def __init__(self,required = True,help_text =None,editor='default',features=None,**kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            "link"
        ]

    class Meta:#
        template = "stream/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"

class CTABlock(blocks.StructBlock):
    titulo = blocks.CharBlock(required=True,max_length=60)
    texto = blocks.RichTextBlock(required=True,features=['bold','italic'])
    boton_page = blocks.PageChooserBlock(required=False)
    boton_url = blocks.URLBlock(required=False)
    boton_texto = blocks.CharBlock(required=True,default="Leer más",max_length=200)

    class Meta:
        template = "stream/cta_block.html"
        icon = "placeholder"
        label = "Llamada de accion"
