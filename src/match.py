from typing import List


def match(method:List[str]=["distance","tag"], threshold:float=100.0)->bool:
    # try to match in distance and get a score
    # try to match in tag(including name) and get a score
    # score if over certain threshold, then pass and tagged as match
    return True

def match_distance()->float:
    return 0.0

def match_tag()->float:
    return 0.0