from urlparse import urlparse
import re, urllib2, string

pat_url = re.compile(r'<a[^<>]+href="?((?:http|/)[^<>"\s]*)"?[^<>]*>', re.IGNORECASE)
pat_events_url = re.compile(r'<a[^<>]+href="?((?:http|/)[^<>"\s]*)"?[^<>]*>.*?(?:event|calendar|calander|discover).*?</a', re.IGNORECASE)

def get_base_url(url):
    o = urlparse(url)
    return '%s://%s' % (o.scheme, o.netloc)

def set_base_url(base_url, url):
    if url[:4].lower() != 'http':
        return base_url + url
    return url

def fetch_page(url):
    try:
        f = urllib2.urlopen(url, timeout=15)
        s = f.read()
        f.close()
    except:
        s = ''
    return s.strip()

def fetch_event_urls(events_url, base_url):
    if events_url:
        # Add domain part if not in url
        events_url = set_base_url(base_url, events_url)
            
        # Now fetch this events page and search for urls to test if they are events or not
        s = fetch_page(events_url)
        return pat_url.findall(s)
    return []

def get_event_urls(url_event):
    # Get cleaned up url first for pattern matching below
    # Remove all digits and lower case
    clean_url_event = url_event.rstrip('/').encode('utf-8').translate(None, string.digits).lower()
    clean_url_event_split = clean_url_event.rsplit('/', 1)[0].lower()
    
    e_urls = []
    base_url = get_base_url(url_event).lower()
    
    # Fetch base page to find the base events pages
    s = fetch_page(base_url)
    events_urls = pat_events_url.findall(s)
    found_needed = False
    
    for events_url in list(set(events_urls)):
        urls = fetch_event_urls(events_url, base_url)
        
        for url in list(set(urls)):
            if url:
                url = set_base_url(base_url, url)
                    
                # Check if url pattern matches, then most likely its an event
                # First remove all digits from url
                clean_url = url.rstrip('/').encode('utf-8').translate(None, string.digits)
                    
                # Then check if the url pattern matches the original event url pattern
                if clean_url_event == clean_url.lower():
                    if url != url_event and not url in e_urls:
                        e_urls.append(url)
                elif clean_url_event_split != base_url and clean_url_event_split == clean_url.rsplit('/', 1)[0].lower():
                    # Now try to see if its a url formatted for SEO
                    # (like http://www.eventbrite.com/e/sausalito-art-festival-2014-tickets-11831764125)
                    if url != url_event and not url in e_urls:
                        e_urls.append(url)
                    
                # If we have ten, we are done
                if len(e_urls) >= 10:
                    found_needed = True
                    break
            
        if found_needed:
            break
    
    return e_urls
