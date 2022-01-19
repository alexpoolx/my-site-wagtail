from django.db import models
from django.shortcuts import redirect, render
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin,route
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core.models import Page
from wagtail.search.models import Query


from stream import blocks


class BlogAuthorsOrderable(Orderable):
    """"""

    page = ParentalKey("articulos.ArticulosDetallePage", related_name="articulo_authors")
    author = models.ForeignKey(
        "articulos.ArticuloAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]


class ArticuloAuthor(models.Model):
    """"""

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],
            heading="Name and Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links"
        )
    ]

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = "Articulo Author"
        verbose_name_plural = "Articulo Authors"


register_snippet(ArticuloAuthor)


class ArticulosListPage(RoutablePageMixin,Page):
    """"""

    template = "articulos/articulos_list_page.html"
    ajax_template= "articulos/articulos_list_page_ajax.html"
    max_count = 1
    subpage_type = [""]
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Sobrescribe el título predeterminado',
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = ArticulosDetallePage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_posts, 2)
        page = request.GET.get("page")
        try: 
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context["posts"] = posts
        context["categories"] = ArticulosCategoria.objects.all()
        return context

    
    def search(request):
        search_query = request.GET.get('query', None)
        page = request.GET.get('page', 1)

        # Search
        if search_query:
            search_results = Page.objects.live().search(search_query)
            query = Query.get(search_query)

            # Record hit
            query.add_hit()
        else:
            search_results = Page.objects.none()

        # Pagination
        paginator = Paginator(search_results, 10)
        try:
            search_results = paginator.page(page)
        except PageNotAnInteger:
            search_results = paginator.page(1)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)

        return TemplateResponse(request, 'search/search.html', {
            'search_query': search_query,
            'search_results': search_results,
        })
    

    @route(r'^latest/?$', name="latest_posts")
    def latest_blog_posts_only_shows_last_5(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][:1]
        context["latest_posts"] = ArticulosDetallePage.objects.live().public()[:1]
        return render(request, "articulos/articulos_last.html", context)

class ArticulosCategoria(models.Model):
    """"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='Indentifica la categoria',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Articulo Categoria"
        verbose_name_plural = "Articulo Categorias"
        ordering = ["name"]

    def __str__(self):
        return self.name


register_snippet(ArticulosCategoria)


class ArticulosDetallePage(Page):

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )
    articulo_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    categories = ParentalManyToManyField("articulos.ArticulosCategoria", blank=True)
    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("articulo_image"),
         MultiFieldPanel(
            [
                InlinePanel("articulo_authors", label="Author", min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
         MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        ),
        StreamFieldPanel("content"),
    ]


