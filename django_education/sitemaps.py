from django.contrib.sitemaps import Sitemap
from .models import sequence, systeme, competence

class SequenceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return sequence.objects.all()

class SystemeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return systeme.objects.all()

class CompetenceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return competence.objects.all()
