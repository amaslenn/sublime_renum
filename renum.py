# -*- coding: utf-8 -*-

import sublime, sublime_plugin

class renum(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings('ReNum.sublime-settings')

        index = settings.get("start_index", 0)
        pattern = settings.get("search_pattern", '/\*\d+\*/')

        # get all matches...
        num = len(self.view.find_all(pattern))
        if not num:
            sublime.status_message("Nothing found for `{}`".format(pattern))
            return
        # ... to keep leading zeros
        fmt = "/*{}:0>{}{}*/".format('{', len(str(num - 1)), '}')
        # ^ I don't know how to use {} not as special characters

        start_pos = 0
        while True:
            matched_region = self.view.find(pattern, start_pos)
            if not matched_region:
                break
            self.view.replace(edit, matched_region, fmt.format(index))
            index += 1

            # repeat search to get new Region
            matched_region = self.view.find(pattern, start_pos)

            # start new search from the end of changed region
            start_pos = matched_region.b

        sublime.status_message("Indexes updated: {}".format(index))