ContentDM Sitemap Builder
=========================

This script will build a [sitemaps.org](http://www.sitemaps.org) compliant sitemap for your ContentDM repository. 
It depends on a fork of @saverkamp's wonderful [pycdm library](http://github.com/saverkamp/pycdm) for working with the ContentDM API in python. 
Pretty sure this is only an option for local run ContentDM instances, and OCLC will restrict wat you can add to 
hosted instances.

Installation
-----------------
On Linux 

* `cd /usr/local/` # or wherever you want to install the scripts
* `git clone https://github.com/bibliotechy/pycdm-sitemap.git`
* `git submodule init`
* `git submodule update`
* `cd pycdm`
* `git checkout master`

then

* `cd /path/to/contentdm6/Website/public_html/`
* `mkdir sitemap`


Usage
-----------------

* `cd /path/to/pycdm-sitemap`
* `./build.py "http://base.url.contentdm.server" --filpath /path/to/contentdm6/Website/public_html/sitemap/`
This will output all of the collection sitemaps and the overall sitemap.xml into you sitemap directory.

We set up a nightly cron job to run this so we always have a fresh sitemap.


What Next
----------------
Check out the code4lib [Robots are our Friends](http://wiki.code4lib.org/index.php/Robots_Are_Our_Friends) page. It
has lots of ideas on how to leverage the sitemaps to improve you repositories presence on "teh googels".
