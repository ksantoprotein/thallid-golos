# thallid-golos - Python Library for GOLOS

Thallid-Golos библиотека для блокчейна Golos


# Installation

https://github.com/ksantoprotein/thallid-golos.git

# Documentation

### Поддерживает broadcast следующих операций
- vote
- comment
- transfer
- transfer_to_vesting
- withdraw_vesting
- set_withdraw_vesting_route
- account_create
- account_update
- account_witness_vote
- account_witness_proxy
- custom_json
- comment_options
- change_recovery_account
- delegate_vesting_shares
- account_create_with_delegation
- account_metadata
- delegate_vesting_shares_with_interest
- claim
- donate
- transfer_to_tip
- transfer_from_tip
- create_invite
- claim_invite
- account_create_with_invite


Используется broadcast_transaction_synchronous и функция возвращает tx транзакции добавляя в нее номер блока и trx_id

![](https://i.imgur.com/OrR7Bj9.png)


# Usage examples

#### Vote
``` python
from tgolosbase.api import Api

b4 = Api()

url = 'https://golos.id/solox/@ddd-005/top-week-received-vesting-shares-golos-15-09-2019'
voters = ['ksantoprotein']
weight = 10000		#100%
wif = '5...'

b4.vote(url, weight, voters, wif)

```

#### Post/Comment
``` python
from tgolosbase.api import Api

b4 = Api()

title = 'test'
body = 'test'
author = 'ksantoprotein'
wif = '5...'

b4.post(title, body, author, wif)

# comment
url = 'https://golos.id/thallid/@ksantoprotein/test-1568630110'
b4.post(title, body, author, wif, url=url)

# differ optional
# category = ''
# permlink = ''
# tags = []
# beneficiaries = 'login:10000'
```

#### Transfer/Transfers
``` python
from tgolosbase.api import Api

b4 = Api()

to = 'thallid'
amount = '0.001'
asset = 'GOLOS'
memo = 'test'
from_account = 'ksantoprotein'
wif = '5...'

b4.transfer(to, amount, asset, from_account, wif, memo=memo)

# [to, amount, asset, memo]
raw_ops = [[to, amount, 'GOLOS', 'test GOLOS'], [to, amount, 'GBG', 'test GBG']]

b4.transfers(raw_ops, from_account, wif)
```

#### Transfer_to_vesting/Withdraw_vesting/Delegate_vesting_shares/Delegate_vesting_shares_with_interest
``` python
from tgolosbase.api import Api

b4 = Api()

to = 'thallid'
amount = '1.000'
from_account = 'ksantoprotein'
wif = '5...'

rate = 2500

b4.transfer_to_vesting(to, amount, from_account, wif)
b4.delegate_vesting_shares(to, amount, from_account, wif)
b4.delegate_vesting_shares_with_interest(to, amount, from_account, rate, wif)

b4.withdraw_vesting(from_account, amount, wif)
```

#### Account_create/Account_create_with_delegation/Account_create_with_invite
``` python
from tgolosbase.api import Api

b4 = Api()

login = 'test'
password = 'test'
creator = 'ksantoprotein'
wif = '5...'
invite = '5...'

b4.account_create(login, password, creator, wif)
b4.account_create_with_delegation(login, password, creator, wif)
b4.account_create_with_invite(invite, login, password, creator, wif)
```

#### Account_update_password
``` python
from tgolosbase.api import Api

b4 = Api()

account = 'ksantoprotein'
password = 'test'
wif = '5...'		#owner

b4.account_update_password(account, password, wif)
```

#### Change_recovery_account
``` python
from tgolosbase.api import Api

b4 = Api()

recovery_account = 'ksantoprotein'
account = 'toto-cosmos'
wif = '5..'			#owner

b4.change_recovery_account(account, recovery_account, wif)
```

#### Account_metadata
``` python
from tgolosbase.api import Api

b4 = Api()

account = 'ksantoprotein'
json_metadata = {"profile": {
		"profile_image": 'av_543.gif',
		"name": 'ProName',
		"about": 'VolSU',
		"gender": 'male',
		"location": 'Volgograd',
		"website": 'https://golos.id/@sci-populi',
		"pinnedPosts": [],
		}}
wif = '5...'		#posting

b4.account_metadata(account, json_metadata,  wif)
```

#### Set_withdraw_vesting_route
``` python
from tgolosbase.api import Api

b4 = Api()

from_account = 'thallid'
to_account = 'ksantoprotein'
wif = '5..'			#active

b4.set_withdraw_vesting_route(from_account, to_account, wif)

# differ optional
# to_vest = True
```

#### Account_witness_vote/Account_witness_proxy
``` python
from tgolosbase.api import Api

b4 = Api()

account = 'thallid'
witness = 'ksantoprotein'
proxy = 'ksantoprotein'
wif = '5..'			#active

b4.account_witness_vote(account, witness, wif)
b4.account_witness_proxy(account, proxy, wif)
```

#### Transfer_to_tip/Transfer_from_tip
``` python
from tgolosbase.api import Api

b4 = Api()

initiator = 'ksantoprotein'
receiver = 'thallid'
amount = 1.000
wif = '5..'			#active

b4.transfer_to_tip(initiator, receiver, amount, wif)
b4.transfer_from_tip(initiator, receiver, amount, wif)
```

#### Create_invite/Claim_invite
``` python
from tgolosbase.api import Api

b4 = Api()

initiator = 'ksantoprotein'
receiver = 'thallid'
amount = 100.000
wif = '5..'			#active
public_invite_key = 'GLS...'
private_invite_key = '5...'

b4.create_invite(initiator, amount, public_invite_key, wif)
b4.claim_invite(initiator, receiver, private_invite_key, wif)
```

#### Claim/Donate
``` python
from tgolosbase.api import Api

b4 = Api()

initiator = 'ksantoprotein'
receiver = 'thallid'
amount = 100.000
wif = '5..'			#posting
public_invite_key = 'GLS...'
private_invite_key = '5...'

b4.claim(initiator, receiver, wif)
b4.donate(initiator, receiver, amount, wif)

# differ optional
#balance = amount
#memo = {"app": ..., "version": ..., "target": ..., "comment": ...}
```
