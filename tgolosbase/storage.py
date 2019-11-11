# -*- coding: utf-8 -*-

chain_id = '782a3039b478c839e4cb0c941ff4eaeb7df40bdd68bd441afd444b9da763de12'		# GOLOS
prefix = 'GLS'
time_format = '%Y-%m-%dT%H:%M:%S'
time_format_utc = '%Y-%m-%dT%H:%M:%S%Z'
expiration = 60

# https://ropox.app/steemjs/api/database_api/get_chain_properties
#create_account_min_golos_fee = 0.030			# GOLOS
#create_account_max_delegation = 33333.333333	# GEST


nodes = [
		'wss://api.golos.blckchnd.com/ws',
		'wss://golos.solox.world/ws',			#'https://golos.solox.world/'
		'wss://golos.lexa.host/ws',
		'wss://denisgolub.name/ws',
		'wss://shafarevich.space/ws',
		]


api_list = {
			"account_by_key": ['get_key_references'],				# yes
			"account_history": ['get_account_history'],				# yes "params": ["account", "from", "limit"]
			"database_api": [
							'get_account_bandwidth',				# 
							'get_account_count',					# yes
							'get_accounts',							# yes ### need for change
							'get_block',							# yes
							'get_block_header',
							'get_chain_properties',					# yes
							'get_config',							# yes
							'get_conversion_requests',
							'get_database_info',					# yes
							'get_dynamic_global_properties',		# yes
							'get_escrow',
							'get_expiring_vesting_delegations',
							'get_hardfork_version',
							'get_next_scheduled_hardfork',
							'get_owner_history',
							'get_potential_signatures',
							'get_proposed_transaction',				#
							'get_recovery_request',
							'get_required_signatures',
							'get_savings_withdraw_from',
							'get_savings_withdraw_to',
							'get_transaction_hex',
							'get_vesting_delegations',
							'get_withdraw_routes',
							'lookup_account_names',					# Возращает данные по заданным аккаунтам видимо дубль get_accounts без репутации
							'lookup_accounts',						# yes in get_all_accounts
							'verify_account_authority',
							'verify_authority'
							],
			"follow": [
							'get_account_reputations',				#
							'get_blog',								# 
							'get_blog_authors',						# 
							'get_blog_entries',						# 
							'get_feed',								# 
							'get_feed_entries',						# 
							'get_follow_count',						#
							'get_followers',						#
							'get_following',						#
							'get_reblogged_by'						# 
						],
			"market_history": [
							'get_market_history',					# "params": ["bucket_seconds" , "start", "end"]
							'get_market_history_buckets',			# yes видимо какие временные интервалы можно использовать
							'get_open_orders',						# yes "params": ["owner"]
							'get_order_book',						# yes "params": ["limit"]
							'get_order_book_extended',				# yes "params": ["limit"]
							'get_recent_trades',					# yes "params": ["limit"]
							'get_ticker',							# yes
							'get_trade_history',					# "params": ["start", "end", "limit"]
							'get_volume'							# yes
							],
			"network_broadcast_api": [
							'broadcast_block',
							'broadcast_transaction',
							'broadcast_transaction_synchronous',
							'broadcast_transaction_with_callback'
							],
			"operation_history": [
							'get_ops_in_block',						# yes
							'get_transaction'
							],
			"social_network": [
							'get_account_votes',
							'get_active_votes',
							'get_all_content_replies',
							'get_content',
							'get_content_replies',
							'get_replies_by_last_update'
							],
			"tags": [
							'get_discussions_by_active',
							'get_discussions_by_author_before_date',
							'get_discussions_by_blog',
							'get_discussions_by_cashout',
							'get_discussions_by_children',
							'get_discussions_by_comments',
							'get_discussions_by_created',
							'get_discussions_by_feed',
							'get_discussions_by_hot',
							'get_discussions_by_payout',
							'get_discussions_by_promoted',
							'get_discussions_by_trending',
							'get_discussions_by_votes',
							'get_languages',
							'get_tags_used_by_author',
							'get_trending_tags'
							],
			"witness_api": [
							'get_active_witnesses',					# yes
							'get_current_median_history_price',		# yes 
							'get_feed_history',						# yes
							'get_miner_queue',
							'get_witness_by_account',				# yes
							'get_witness_count',					# yes
							'get_witness_schedule',					# yes
							'get_witnesses',						#
							'get_witnesses_by_vote',				#
							'lookup_witness_accounts'				# yes хз что это такое то
							],
		}
		
# Переделка списка апи под формат словаря name:api		
api_total = {}		
for key, value in api_list.items():
	for api in value:
		api_total[api] = key
		
	
# Список транзакций по порядку для каждого БЧ он свой
# https://github.com/GolosChain/golos-js/blob/master/src/auth/serializer/src/ChainTypes.js
op_names = [
	'vote',										# yes
	'comment',									# yes
	'transfer',									# yes
	'transfer_to_vesting',						# yes
	'withdraw_vesting',							# yes
	'limit_order_create',
	'limit_order_cancel',
	'feed_publish',
	'convert',
	'account_create',							# need py
	'account_update',							#
	'witness_update',
	'account_witness_vote',						#
	'account_witness_proxy',					#
	'pow',
	'custom',
	'report_over_production',
	'delete_comment',							#
	'custom_json',								# follow, reblog)
	'comment_options',							#
	'set_withdraw_vesting_route',
	'limit_order_create2',
	'challenge_authority',
	'prove_authority',
	'request_account_recovery',
	'recover_account',
	'change_recovery_account',					# yes
	'escrow_transfer',
	'escrow_dispute',
	'escrow_release',
	'pow2',
	'escrow_approve',
	'transfer_to_savings',
	'transfer_from_savings',
	'cancel_transfer_from_savings',
	'custom_binary',
	'decline_voting_rights',
	'reset_account',
	'set_reset_account',
	'delegate_vesting_shares',					# yes
	'account_create_with_delegation',			# need py
	'account_metadata',							# yes
	'proposal_create',
	'proposal_update',
	'proposal_delete',
	'chain_properties_update',
	'break_free_referral',
	'delegate_vesting_shares_with_interest',	# yes
	'reject_vesting_shares_delegation',
	'fill_convert_request',
	'author_reward',
	'curation_reward',
	'comment_reward',
	'liquidity_reward',
	'interest',
	'fill_vesting_withdraw',
	'fill_order',
	'shutdown_witness',
	'fill_transfer_from_savings',
	'hardfork',
	'comment_payout_update',
	'comment_benefactor_reward',
	'return_vesting_delegation',
	'producer_reward',
	'delegation_reward',
	'auction_window_reward',
]

#: assign operation ids
operations = dict(zip(op_names, range(len(op_names))))

asset_precision = {
					"GOLOS": 3,
					"GESTS": 6,
					"GBG": 3,
					}



rus_d = {
		'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
		'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
		'й': 'ij', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
		'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
		'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'cz', 'ч': 'ch',
		'ш': 'sh', 'щ': 'shch', 'ъ': 'xx', 'ы': 'y', 'ь': 'x',
		'э': 'ye', 'ю': 'yu', 'я': 'ya',

		'А': "A", 'Б': "B", 'В': "V", 'Г': "G", 'Д': "D",
		'Е': "E", 'Ё': "yo", 'Ж': "ZH", 'З': "Z", 'И': "I",
		'Й': "IJ", 'К': "K", 'Л': "L", 'М': "M", 'Н': "N",
		'О': "O", 'П': "P", 'Р': "R", 'С': "S", 'Т': "T",
		'У': "U", 'Ф': "F", 'Х': "KH", 'Ц': "CZ", 'Ч': "CH",
		'Ш': "SH", 'Щ': "SHCH", 'Ъ': "XX", 'Ы': "Y", 'Ь': "X",
		'Э': "YE", 'Ю': "YU", 'Я': "YA",
		' ': "-", '.': "-", ',': "-", ':': "-", ';': "-", 
		'(': "", ')': "", '!': "", '?': "", '"': "", "'": "", '[': "", ']': "", '|': "", '/': "", '_': "", '@': "", '$': "",  
		}

rus_list = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя., '