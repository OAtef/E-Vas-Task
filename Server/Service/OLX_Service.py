from Server.Model.OLX import Ads


def create_olx_post(**data):
    listing = Ads.objects(link=data['link']).first()
    if listing is None:
        ad = Ads(link=data['link'],
                 price=data['price'],
                 title=data['title'],
                 condition=data['condition'],
                 description=data['description'],
                 advertiser_name=data['advertiser_name'],
                 location=data['location'],
                 mobile=data['mobile']
                 )
        ad.save()
    else:
        ad = listing
    return ad


def get_all_posts():
    all = Ads.objects().all()
    list_of_adds = []
    for ad in all:
        list_of_adds.append(ad.to_json())
    return list_of_adds


def get_with_limit(size=20):
    listing = Ads.objects[:size]
    list_of_adds = []
    for ad in listing:
        list_of_adds.append(ad.to_json())
    return list_of_adds

