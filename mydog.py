#!/usr/bin/env python
# encoding: utf-8
"""
Tweet an absurd joke.
"""
from __future__ import print_function
import argparse
import sys
import twitter
import webbrowser
import yaml
from wordnik import swagger, WordsApi


def load_yaml(filename):
    """
    File should contain:
    consumer_key: TODO_ENTER_YOURS
    consumer_secret: TODO_ENTER_YOURS
    access_token: TODO_ENTER_YOURS
    access_token_secret: TODO_ENTER_YOURS
    wordnik_api_key: TODO_ENTER_YOURS
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {
            'access_token', 'access_token',
            'consumer_key', 'consumer_secret'}:
        sys.exit("Twitter credentials missing from YAML: " + filename)
    if not data.viewkeys() >= {
            'wordnik_api_key'}:
        sys.exit("Wordnik credentials missing from YAML: " + filename)
    return data


def tweet_it(string, credentials):
    """ Tweet string using credentials """
    if len(string) <= 0:
        return

    # Create and authorise an app with (read and) write access at:
    # https://dev.twitter.com/apps/new
    # Store credentials in YAML file
    t = twitter.Twitter(auth=twitter.OAuth(
        credentials['access_token'],
        credentials['access_token_secret'],
        credentials['consumer_key'],
        credentials['consumer_secret']))

    print("TWEETING THIS:\n", string)

    if args.test:
        print("(Test mode, not actually tweeting)")
    else:
        result = t.statuses.update(status=string)
        url = "http://twitter.com/" + \
            result['user']['screen_name'] + "/status/" + result['id_str']
        print("Tweeted:\n" + url)
        if not args.no_web:
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def get_random_word_from_wordnik(part_of_speech):
    """ Get a random word from Wordnik """
    word = words_api.getRandomWord(includePartOfSpeech=part_of_speech)
    word = word.word
    print("Random " + part_of_speech + ": " + word)
    return word


def mydog():
    """ Create an absurd joke """
    print("Get words from Wordnik...")
    noun = get_random_word_from_wordnik("noun")
    verb = get_random_word_from_wordnik("verb-intransitive")
    adjective = get_random_word_from_wordnik("adjective")
    output = '"My dog\'s got no {0}."\n"How does he {1}?"\n"{2}!"'.format(
        noun, verb, adjective.capitalize())
    print()
    print(output)
    print()
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tweet an absurd joke.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        default='/Users/hugo/Dropbox/bin/data/mydog.yaml',
        help="YAML file location containing Twitter keys and secrets")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    parser.add_argument(
        '-x', '--test', action='store_true',
        help="Test mode: go through the motions but don't tweet anything")
    args = parser.parse_args()

    credentials = load_yaml(args.yaml)
    wordnik_client = swagger.ApiClient(credentials['wordnik_api_key'],
                                       'http://api.wordnik.com/v4')
    words_api = WordsApi.WordsApi(wordnik_client)

    tweet = mydog()

    tweet_it(tweet, credentials)

# End of file
