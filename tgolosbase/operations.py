# -*- coding: utf-8 -*-

#Permission = authority, 
from .types import *

# Сериализатор
# https://github.com/GolosChain/golos-js/blob/master/src/auth/serializer/src/operations.js

type_op = {
	"vote":								[['voter', String], ['author', String], ['permlink', String], ['weight', Int16]],
	"comment":							[['parent_author', String], ['parent_permlink', String], ['author', String], ['permlink', String], 
										['title', String], ['body', String], ['json_metadata', String]],
	"transfer":							[['from', String], ['to', String], ['amount', Amount], ['memo', String]],
	"transfer_to_vesting":				[['from', String], ['to', String], ['amount', Amount]],
	"withdraw_vesting":					[['account', String], ['vesting_shares', Amount]],
	#"set_withdraw_vesting_route":		[['from_account', String], ['to_account', String], ['percent', Uint16], ['auto_vest', Bool]],
	"account_create":					[['fee', Amount], ['creator', String], ['new_account_name', String], 
										['owner', Permission], ['active', Permission], ['posting', Permission], ['memo_key', PublicKey], 
										['json_metadata', String]],
											
	"account_update":					[['account', String], ['owner', Optional_Permission], ['active', Optional_Permission], 
											['posting', Optional_Permission], ['memo_key', PublicKey], ['json_metadata', String]],
											
	#"account_witness_vote":			[['account', String], ['witness', String], ['approve', Bool]],
	#"account_witness_proxy":			[['account', String], ['proxy', String]],
	#"delete_comment":					[['author', String], ['permlink', String]],
	"custom_json": 						[['required_auths', ArrayString], ['required_posting_auths', ArrayString], 
											['id', String], ['json', String]],
											
	"comment_options":					[['author', String], ['permlink', String], ['max_accepted_payout', Amount], 
											['percent_steem_dollars', Uint16], ['allow_votes', Bool], ['allow_curation_rewards', Bool],
											['extensions', ExtensionsComment]],
	"change_recovery_account":			[['account_to_recover', String], ['new_recovery_account', String], ['extensions', Set]],
	"delegate_vesting_shares":			[['delegator', String], ['delegatee', String], ['vesting_shares', Amount]],
	"account_create_with_delegation":	[['fee', Amount], ['delegation', Amount], ['creator', String], ['new_account_name', String], 
											['owner', Permission], ['active', Permission], ['posting', Permission], ['memo_key', PublicKey], 
											['json_metadata', String], ['extensions', Set]],
	"account_metadata": 				[['account', String], ['json_metadata', String]],
	"delegate_vesting_shares_with_interest":	
										[['delegator', String], ['delegatee', String], ['vesting_shares', Amount],
										['interest_rate', Uint16], ['extensions', Set]],

			}
