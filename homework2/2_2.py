def filter_strings(filter_func, string_array):
    return [s for s in string_array if filter_func(s)]

filter_out_spaces = lambda s: ' ' not in s
filter_out_starting_with_a = lambda s: not s.startswith('a')
filter_out_shorter_than_five = lambda s: len(s) >= 5

strings = ["one egg", "dog", "adventure", "ant", "alpha", "bug", "emotional", "delta"]

no_spaces = filter_strings(filter_out_spaces, strings)
not_starting_with_a = filter_strings(filter_out_starting_with_a, strings)
longer_than_or_equal_five = filter_strings(filter_out_shorter_than_five, strings)

print("Strings without spaces:", no_spaces)
print("Strings not starting with 'a':", not_starting_with_a)
print("Strings longer than or equal to 5 characters:", longer_than_or_equal_five)