# thallid-golos - Unofficial Python Library for GOLOS

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
- account_create
- account_update
- custom_json
- comment_options
- change_recovery_account
- delegate_vesting_shares
- account_create_with_delegation
- account_metadata
- delegate_vesting_shares_with_interest

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
curation = 'max'	#or int 2500..10000

b4.post(title, body, author, wif, curation = curation)

# comment
url = 'https://golos.id/thallid/@ksantoprotein/test-1568630110'
b4.post(title, body, author, wif, curation = curation, url = url)

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

b4.transfer(to, amount, asset, from_account, wif, memo = memo)

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

rate = 4500

b4.transfer_to_vesting(to, amount, from_account, wif)
b4.delegate_vesting_shares(to, amount, from_account, wif)
b4.delegate_vesting_shares_with_interest(to, amount, from_account, rate, wif)

b4.withdraw_vesting(from_account, amount, wif)
```

#### Account_create/Account_create_with_delegation
``` python
from tgolosbase.api import Api

b4 = Api()

login = 'test'
password = 'test'
creator = 'ksantoprotein'
wif = '5...'

b4.account_create(login, password, creator, wif)
b4.account_create_with_delegation(login, password, creator, wif)
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

tx = b4.change_recovery_account(account, recovery_account, wif)
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
