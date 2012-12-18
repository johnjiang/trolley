from __future__ import unicode_literals

# Scrapy settings for trolley project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'trolley'

SPIDER_MODULES = ['trolley.spiders']
NEWSPIDER_MODULE = 'trolley.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'trolley (+http://www.yourdomain.com)'
