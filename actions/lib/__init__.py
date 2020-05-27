def get_twitter_tokens(config, account):
    default_account = config.get('default_account')

    if not account and not default_account:
        raise Exception("Either the default account should be specified "
            "in the config, or an account parameter must be passed.")

    if not account:
        account = default_account

    for config_account in config['accounts']:
        if config_account['name'] == account:
            consumer_key = config_account['consumer_key']
            consumer_secret = config_account['consumer_secret']
            access_token = config_account['access_token']
            access_token_secret = config_account['access_token_secret']
            break
    else:
        raise Exception("Unable to determine account to use")

    return consumer_key, consumer_secret, access_token, access_token_secret
