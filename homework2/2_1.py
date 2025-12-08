def is_palindrome(s):
    string = ''.join(char for char in s if char.isalnum()).lower()
    reversed_s = string[::-1]
    return string == reversed_s
test_strings = [
    "racecar",           # 简单回文
    "A man a plan a canal Panama",  # 经典回文（忽略空格和大小写）
    "hello",             # 非回文
    "12321",             # 数字回文
    "Was it a car or a cat I saw?" # 复杂回文 
]

for test in test_strings:
    result = is_palindrome(test)
    print(f"'{test}' -> {result}")