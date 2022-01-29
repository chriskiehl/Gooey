

def runValidator(f, value) -> bool:
    """
    Attempt to run the user supplied validation function

    Fall back to False in the even of any errors
    """
    try:
        return f(value)
    except:
        return False



