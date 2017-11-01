#! /usr/bin/env python3
"""
Generate One Time Pad files, or serve the pads up using a CherryPy server.
"""
from jinja2 import DictLoader, Environment
import secrets
import cherrypy


# CherryPy config
CONFIG = {'global': {'server.socket_port': 8080}}

# The characters available for the One Time Pad
OTP_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# The number of characters in each group, separated by spaces
GROUP_SIZE = 5
# The groups in each row of a message, separated by newlines
GROUP_COUNT = 20
# The number of rows per message
ROW_COUNT = 4
# The number of messages per page
MESSAGE_COUNT = 9


def generate_row(group_count=GROUP_COUNT, group_size=GROUP_SIZE):
    """
    Generate a string of random characters, groups in this string are separated by spaces.

    Example:
        NLJDS KW9JG 30AZJ J0XQ4 IRP0Z L6YQT AB7AO RY5XG
    """
    groups = []
    for _ in range(group_count):
        groups.append(''.join([secrets.choice(OTP_CHARS) for _ in range(group_size)]))
    return ' '.join(groups)


def generate_message(row_count=ROW_COUNT, group_count=GROUP_COUNT, group_size=GROUP_SIZE):
    """
    Combine several rows into a single message.
    """
    return '\n'.join(generate_row(group_count, group_size) for _ in range(ROW_COUNT))


class Root(object):

    @cherrypy.expose
    def one_time_pad(self):
        """
        Put all messages into the page
        """
        messages = (generate_message() for _ in range(MESSAGE_COUNT))
        template = env.get_template('one_time_pad')
        return template.render(messages=messages)


# This is the only page.  Links are shortened to make manual typing easier.
templates = {'one_time_pad': '''
<title>One Time Pad - Unique, just for you</title>
<style>
/* Remove decoration from links so they are readable when printed */
a { text-decoration: none; }
</style>
[[ for num, message in messages|enumerate(1) ]]
<pre>Message [- num -]</pre>
<pre>
[- message -]
</pre>
[[ endfor ]]

Print this page and distribute the copies (along with the <a href="https://lrnsr.co/aY6m">One Time Pad Cheat Sheet
https://lrnsr.co/aY6m</a>) to all members of your group that you trust to receive your encrypted messages.  Every
person must have their OWN copy of this "One Time Pad" to encrypt and decrypt messages.
<br>
<b>Use each message ONLY ONCE.</b>  Cut off and burn each message from this paper as it is used.
<br>
If you want more One Time Pads, simply <a href=".">go here to refresh the page:
https://learningselfreliance.com/one_time_pad</a>.  The server will generate a unique page just for you. This page
is not stored on the server, and cannot be retrieved once you close this window!
<br>
To learn how to use this page, please visit: <a href="https://lrnsr.co/H7Za">https://lrnsr.co/H7Za</a>
''',
}

env = Environment(
    loader=DictLoader(templates),
    autoescape=True,
    block_start_string='[[',
    block_end_string=']]',
    comment_start_string='[#',
    comment_end_string='#]',
    variable_start_string='[-',
    variable_end_string='-]',
)

env.filters['enumerate'] = enumerate

if __name__ == '__main__':
    # Start cherrypy server
    cherrypy.quickstart(cherrypy.Application(Root()), '/', config=CONFIG)
