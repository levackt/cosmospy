from unittest.mock import Mock

from cosmospy import Transaction


def test_sign():
    private_key = bytes.fromhex("2afc5a66b30e7521d553ec8e6f7244f906df97477248c30c103d7b3f2c671fef")
    unordered_sign_message = {
        "chain_id": "tendermint_test",
        "account_number": "1",
        "fee": {"gas": "21906", "amount": [{"amount": "0", "denom": ""}]},
        "memo": "",
        "sequence": "0",
        "msgs": [
            {
                "type": "cosmos-sdk/Send",
                "value": {
                    "inputs": [
                        {
                            "address": "secret1lgharzgds89lpshr7q8kcmd2esnxkfpwwekakl",
                            "coins": [{"amount": "1", "denom": "USCRT"}],
                        }
                    ],
                    "outputs": [
                        {
                            "address": "secret1dep39rnnwztpt63jx0htxrkt3lgku2cdp355n6",
                            "coins": [{"amount": "1", "denom": "USCRT"}],
                        }
                    ],
                },
            }
        ],
    }
    dummy_num = 1337
    tx = Transaction(
        privkey=private_key,
        account_num=dummy_num,
        sequence=dummy_num,
        fee=dummy_num,
        gas=dummy_num,
    )
    tx._get_sign_message = Mock(return_value=unordered_sign_message)  # type: ignore

    expected_signature = (
        "+CBgG6yJWT28T9ucjGJ8JglRxdPajuFAOCqpYiY6L5Q3I4P5ulEjP86L1GBdpLkPU+c4KfUTh3xp4y9LBEuqIg=="
    )

    actual_signature = tx._sign()
    assert actual_signature == expected_signature


def test_get_pushable_tx():
    expected_pushable_tx = '{"tx":{"msg":[{"type":"cosmos-sdk/MsgSend","value":{"from_address":"secret1lgharzgds89lpshr7q8kcmd2esnxkfpwwekakl","to_address":"secret1dep39rnnwztpt63jx0htxrkt3lgku2cdp355n6","amount":[{"denom":"uscrt","amount":"387000"}]}}],"fee":{"gas":"37000","amount":[{"denom":"uscrt","amount":"1000"}]},"memo":"","signatures":[{"signature":"Om7Yd13MNvyuxt1ej//x3ywBRYAbD7N8rsReIzXQUeBnlfh5sMFD129DOg2xWxIS/L3T2LNkq7OPo02q3Se2og==","pub_key":{"type":"tendermint/PubKeySecp256k1","value":"A49sjCd3Eul+ZXyof7qO460UaO73otrmySHyTNSLW+Xn"},"account_number":"11335","sequence":"0"}]},"mode":"sync"}'  # noqa: E501

    _tx_total_cost = 388000
    fee = 1000
    amount = _tx_total_cost - fee

    tx = Transaction(
        privkey=bytes.fromhex("26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59"),
        account_num=11335,
        sequence=0,
        fee=fee,
        gas=37000,
        chain_id="enigma-pub-testnet-2",
    )
    tx.add_transfer(recipient="secret1dep39rnnwztpt63jx0htxrkt3lgku2cdp355n6", amount=amount)
    pushable_tx = tx.get_pushable()
    assert pushable_tx == expected_pushable_tx
