def is_owner(obj, username):
    """
    Checks if model instance belongs to a user
    Args:
        obj: A model instance
        username(str): User's username
    Returns:
        boolean: True is model instance belongs to user else False
    """
    if obj.user.username == username:
        return True
    return False
