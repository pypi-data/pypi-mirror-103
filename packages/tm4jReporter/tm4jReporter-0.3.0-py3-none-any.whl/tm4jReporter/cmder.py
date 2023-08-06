#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


from getopt import getopt, GetoptError
import sys
from tm4jReporter.tm4jReporter import Tm4jReporter


def main():
    cmd_args = sys.argv[1:]
    help_text = '\n'.join([
        'tm4j-report --[opt1] [arg1] --[opt2] [arg2] ...',
        '  --url\tJira URL is required',
        '  --user\tJira User is required',
        '  --pass\tJira Password is required',
        '  --project\tJira Project Key is required',
        '  --cycle\tTM4J Cycle Key is optional',
        '  --framework\tTest Framework is required',
        '  \t\trobotframework',
        # '  \tpytest\t\tpytest',
        '  --file\tTest output xml file is required',
        '  --webhook\tPost summary to web url',
        '',
        'example:',
        'tm4j-report --url https://jira.xxx.com --user admin --pass password --project ODO --framework robot --file output.xml',
    ])
    if not cmd_args:
        print(help_text)
        exit(1)
    tm4j_opt = dict()
    try:
        opts, args = getopt(
            args=cmd_args,
            shortopts='',
            longopts=[
                'url=',
                'user=',
                'pass=',
                'project=',
                'cycle=',
                'framework=',
                'file=',
                'webhook=',
            ]
        )
        for k, v in opts:
            tm4j_opt['TM4J_%s' % k.replace('--', '').upper()] = v
    except GetoptError:
        print(help_text)
        exit(1)
    tm4j = Tm4jReporter(
        jira_url=tm4j_opt.get('TM4J_URL'),
        jira_user=tm4j_opt.get('TM4J_USER'),
        jira_pass=tm4j_opt.get('TM4J_PASS'),
        jira_project=tm4j_opt.get('TM4J_PROJECT'),
    )
    if tm4j_opt.get('TM4J_FRAMEWORK') == 'robotframework':
        tm4j.robotframework(
            output_xml_file=tm4j_opt.get('TM4J_FILE'),
            cycle_key=tm4j_opt.get('TM4J_CYCLE'),
            run_env=None
        )
    if tm4j_opt.get('TM4J_WEBHOOK'):
        tm4j.post_webhook(
            output_xml_file=tm4j_opt.get('TM4J_FILE'),
            webhook_url=tm4j_opt.get('TM4J_WEBHOOK')
        )


if __name__ == '__main__':
    print('This is Python scripts')
