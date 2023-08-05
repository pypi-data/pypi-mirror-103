#------------------------------------------------------------------------------
# Description    : Qblox instruments build information
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#--------------------------------------------------------------------------
def get_build_info():
    """
    Get build information for Qblox Instruments.

    Parameters
    ----------

    Returns
    ----------
    dict
        Dictionary containing build information (version, date, Git hash and Git dirty indication).

    Raises
    ----------
    """

    return {"version": "0.3.2",
            "date":    "21/04/2021-16:38:33",
            "hash":    "0x94E811E5",
            "dirty":   False}


# Set version
__version__ = get_build_info()["version"]
