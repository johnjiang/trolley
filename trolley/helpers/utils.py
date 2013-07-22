import logging

logger = logging.getLogger(__name__)

## Doesn't do anything fancy, just wraps it in a select statement so we don't have to

def select_first_text(elem, selector):
    try:
        return elem.select(selector)[0].text.strip()
    except Exception, e:
        print e
        return None


def select_first_attribute(elem, selector, attr):
    try:
        return elem.select(selector)[0][attr]
    except Exception, e:
        print e
        return None
