def update_votes(obj, user, value):
    """
    Updates votes for either a question or answer
    Args:
        obj: Question or Answer model instance
        user: User model instance voting an anwser or question
        value(str): 'U' for an up vote or 'D' for down vote
    """
    obj.votes.update_or_create(user=user, defaults={"value": value}, )
    obj.count_votes()
