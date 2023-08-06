from pylibsimba.simba import Simbachain
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# from __future__ import annotations
# from pylibsimba.base.wallet_base import WalletBase


def get_simba_instance(url: str, wallet, api_key: str, management_key: str):
    """
    Create an instance of a Simbachain API interaction class
    Automatically takes care of choosing the correct implementation and running initialisation.
    Args:
        url : The API URL
        wallet : The Wallet to use
        api_key : (Optional) The API key
        management_key : (Optional) The Management API key
    Returns:
        An initialised instance of the API interaction class
    Raises:
        NotImplementedError: If the url is unrecognised as a supported endpoint
    """

    if api_key or management_key:
        # .com
        simba_inst = Simbachain(url, wallet)
        if api_key:
            simba_inst.set_api_key(api_key)
        if management_key:
            simba_inst.set_management_key(management_key)
        return simba_inst
    else:
        # SEP
        logging.warning('SEP Support is available via the libsimba.py-platform package.')
        raise NotImplementedError("SEP Support is available via the libsimba.py-platform package.")
