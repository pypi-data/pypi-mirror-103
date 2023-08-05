import tldextract



def parse(record):
    tld_extractor = tldextract.TLDExtract(cache_file='tld_lists.txt')
    ext = tld_extractor(record)
    return ext