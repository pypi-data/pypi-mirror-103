from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.utils import generate_mnemonic
from web3.auto import w3

from pylibsimba.base.wallet_base import WalletBase
from pylibsimba.exceptions import WalletNotFoundException


class Wallet(WalletBase):
    def unlock_wallet(self, passkey):
        pass

    def generate_wallet(self, mnemonic: str = None):
        bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)

        if not mnemonic:
            mnemonic = generate_mnemonic(language="english", strength=128)

        # Get Ethereum BIP44HDWallet from mnemonic
        bip44_hdwallet.from_mnemonic(
            mnemonic=mnemonic,
            language="english",
            # passphrase=PASSPHRASE
        )
        # Clean default BIP44 derivation indexes/paths
        bip44_hdwallet.clean_derivation()

        # print("Mnemonic:", bip44_hdwallet.mnemonic())
        self.wallet = bip44_hdwallet

    def delete_wallet(self):
        """
        Remove the current wallet. Not actually stored on disk, so just set to None
        """
        self.wallet = None

    def wallet_exists(self):
        """
        Does a wallet currently exist?
        """
        return self.wallet is not None

    def sign(self, payload: dict):
        """
        Sign the payload with the wallet

        Args:
            payload : an object
        Returns:
            Returns the signed transaction
        """
        if not self.wallet_exists():
            raise WalletNotFoundException("No wallet generated!")

        transaction_template = {
            'to': bytes.fromhex(payload['to'][2:]),
            'value': 0,
            'gas': payload['gas'],
            'gasPrice': payload['gasPrice'],
            'data': bytes.fromhex(payload['data'][2:]),
            'nonce': payload['nonce'],
        }
        private_key = self.wallet.private_key()
        signed = w3.eth.account.sign_transaction(transaction_template, private_key)
        return signed.rawTransaction.hex()

    def get_address(self):
        """
        The address associated with this wallet
        """
        if not self.wallet_exists():
            raise WalletNotFoundException("No wallet generated!")

        return self.wallet.address()
