import uuid
from typing import Any, Dict


def issue_to_v2(i: Dict[str, Any]) -> Dict[str, Any]:
    """
    Helper function to turn v1 issues into v2. Pretty similar formats
    Some keys were removed, visible became mandatory
    modifies the dict in place, redundant return
    """
    if "id" in i:
        del i["id"]
    if "issueId" in i:
        del i["issueId"]
    if "visible" not in i:
        i["visible"] = True
    return i


def make_issue(
    word: str,
    start: int,
    end: int,
    issue_type: str,
    score,
    simpleDescription: str,
    description="",
    suggestions=[],
    subCategory="",
    learnMore="",
    paragraph=False,
    header="",
    metaDict={},
    accept_all_changes=False,
    debug=False,
    segment=None,
    visible=True,
):
    """
    reference:
    https://qordoba.atlassian.net/wiki/spaces/HOME/pages/840368141/Content-AI

    Note on duplicate value issueId / id: the platform switched this key at some point
    But I don't trust being able to delete things, so I will just duplicate it, and one day during a refactor
    we can remove it :grimace:
    """
    _uuid = str(uuid.uuid4())
    if not description:
        description = f'"{word}" is correlated with {issue_type} language.'

    issue = {
        "issueId": _uuid,
        "id": _uuid,
        "issueType": issue_type,
        "from": start,
        "until": end,
        "score": score,
        "suggestions": suggestions,
        "description": description,
        "simpleDescription": simpleDescription,
        "meta": {"paragraph": paragraph},
        "visible": visible,
    }

    if subCategory:
        issue["meta"]["subCategory"] = subCategory

    if learnMore:
        issue["meta"]["learnMore"] = learnMore

    if header:
        issue["meta"]["header"] = header

    if accept_all_changes:
        issue["meta"]["acceptAllChanges"] = accept_all_changes

    if debug:
        # log warnings if meta_dict overwrites issue["meta"]
        common = [value for value in metaDict.keys() if value in issue["meta"]]
        for c in common:
            if metaDict[c] != issue["meta"][c]:
                print(
                    f"Meta_dict {c}:{metaDict[c]} is overwriting issue meta {c}:{issue['meta'][c]}"
                )

        if segment is not None:
            suggestion = suggestions[0] if len(suggestions) else ""
            issue["new_segment"] = segment[:start] + suggestion + segment[end:]

    issue["meta"].update(metaDict)

    return issue


def make_issue_v2(*args, **kwargs):
    return issue_to_v2(make_issue(*args, **kwargs))
