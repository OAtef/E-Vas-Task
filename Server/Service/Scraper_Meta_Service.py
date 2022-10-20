from Server.Model.Scraper_Meta import MetaInfo


def create_info(**data):
    info = MetaInfo.objects(meta_info_name=data['meta_info_name']).first()
    if info is None:
        new_info = MetaInfo(meta_info_name=data['meta_info_name'],
                            meta_info_value=data['meta_info_value']
                            )
        new_info.save()
    else:
        info.meta_info_value = data['meta_info_value']
        info.save()
        new_info = info
    return new_info


def get_info(meta_info_name):
    return MetaInfo.objects(meta_info_name=meta_info_name).first()


def get_all_infos():
    all_infos = MetaInfo.objects().all()
    list_of_infos = []
    for info in all_infos:
        list_of_infos.append(info.to_json())
    return list_of_infos
