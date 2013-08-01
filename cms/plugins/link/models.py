from cms.utils.compat.dj import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin, Page


@python_2_unicode_compatible
class Link(CMSPlugin):
    """
    A link to an other page or to an external website
    """

    name = models.CharField(_("name"), max_length=256)
    url = models.URLField(_("link"), blank=True, null=True)
    page_link = models.ForeignKey(Page, verbose_name=_("page"), blank=True, null=True, help_text=_("A link to a page has priority over a text link."))
    mailto = models.EmailField(_("mailto"), blank=True, null=True, help_text=_("An email adress has priority over a text link."))
    target = models.CharField(_("target"), blank=True, max_length=100, choices=((
        ("", _("same window")),
        ("_blank", _("new window")),
        ("_parent", _("parent window")),
        ("_top", _("topmost frame")),
    )))

    def link(self):
        """
        Returns the link with highest priority among the model fields
        """
        if self.mailto:
            return u"mailto:%s" % self.mailto
        elif self.url:
            return self.url
        elif self.page_link:
            return self.page_link.get_absolute_url()
        else:
            return ""

    def __str__(self):
        return self.name

    search_fields = ('name',)
