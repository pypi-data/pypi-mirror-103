from coldcms.blocks import blocks
from coldcms.wagtail_customization.mixins import ColdCMSPageMixin
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page


class FAQPage(ColdCMSPageMixin, Page):
    """FAQ model."""

    content = RichTextField(blank=True, default="", verbose_name=_("Content"))
    questions_groups = StreamField(
        [("questions_groups", blocks.QuestionCategoryBlock())],
        blank=True,
        null=True,
        verbose_name=_("Question groups"),
    )

    template = "faq/faq.html"
    show_in_menus_default = True
    search_fields = []
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("content"),
        StreamFieldPanel("questions_groups"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Content")),
            ObjectList(
                Page.promote_panels,
                heading=_("Promote"),
                classname="settings",
            ),
        ]
    )

    class Meta:
        verbose_name = _("FAQ Page")
