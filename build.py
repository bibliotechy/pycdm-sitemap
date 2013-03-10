__author__ = 'cbn'

import datetime
import xml.etree.ElementTree as et
import sys
path.extend(["./pycdm"])
import pycdm


#base = "http://digitalcollections.library.gsu.edu/"
urlbase = sys.argv[1]
path = sys.argv[2]
call = pycdm.Api()
ns = "http://www.sitemaps.org/schemas/sitemap/0.9"


def sitemapUrl(alias):
    url = urlbase
    url += "sitemap/sitemap-"
    url += alias.strip('/') + ".xml"
    return url

def latestDate(itemdate, lastmod):
    y,m,d = itemdate.split("-")
    itemdate = datetime.date(year=int(y),month=int(m), day=int(d))
    if lastmod < itemdate:
        lastmod = itemdate
    return lastmod


def buildSiteIndex():
    collections = call.dmGetCollectionList()
    sitemapindex = et.Element('sitemapindex')
    sitemapindex.set('xmlns', ns)
    for collection in collections:
        lastmod = buildCollectionSitemap(collection)
        buildCollectionIndexInfo(collection, sitemapindex, lastmod)
    return et.ElementTree(sitemapindex)


def buildCollectionIndexInfo(collection, parent, lastmod):
    sitemap  = et.SubElement(parent, 'sitemap')
    loc = et.SubElement(sitemap, 'loc')
    loc.text = sitemapUrl(collection['alias'])
    lastmod = et.SubElement(sitemap, 'lastmod')
    lastmod.text = lastmod
    return sitemap

def buildCollectionSitemap(collection):
    """Man is it ugly, but it does the trick"""
    alias = collection['alias'].strip("/")
    start_record = "1"
    lastmod = datetime.date(1970,1,1)

    items = call.dmQuery(
        alias=alias,fields='dmmodified!dmrecord',sortby="dmmodified", start=start_record,
        string='0', field='', mode='', operator='', sep='', #insert on 0 into searchstrings
        ret='response')

    urlset = et.Element('urlset')
    urlset.set("xmlns",ns)

    while _resultsPager(items, start_record):
        if int(start_record) != 1:
            items = call.dmQuery(
                alias=alias,fields='dmmodified!dmrecord',sortby="dmmodified", start=start_record,
                string='0', field='', mode='', operator='', sep='', #insert on 0 into searchstrings
                ret='response')
        for item in items['records']:

            buildItemEntryInfo(item, alias, urlset)
            if lastmod != datetime.date.today():
                lastmod = latestDate(item['dmmodified'],lastmod)
        start_record = str(int(start_record) + int(items['pager']['maxrecs']))

    et.ElementTree(urlset).write(path + "/sitemap-"+ alias + ".xml")
    return lastmod


def buildItemEntryInfo(item, alias, parent):
    if item:
        url = et.SubElement(parent,'url')
        loc = et.SubElement(url, 'loc')
        loc.text = urlbase + "u?"+ alias + "," + item['dmrecord']
        lastmod = et.SubElement(url, 'lastmod')
        lastmod.text = item['dmmodified']


def _resultsPager(items, start_record):
    return items['pager']['total'] >=  int(start_record)


def main():
    if __name__ == "__main__":
        if len(sys.argv) < 3:
            sys.exit("Usage : python build.py <http://url.org/where/sitemap/appears> <system path where sitemap files stored>")
        buildSiteIndex()
