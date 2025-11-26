import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 函数执行时间为 {end_time - start_time:.4f} 秒")
        return result
    return wrapper
@timing_decorator
def calculate_sum(a, b):
    print(f"{a} + {b} = {a+b}")

@timing_decorator
def read_and_write_sum(filename_input, filename_output):
    try:
        with open(filename_input, 'r') as file:
            a, b = map(int, file.read().split(','))
            print(f"Извлечь числа из файла：a = {a}, b = {b}")
            result = a + b
            with open(filename_output, 'w') as file1:
                file1.write(str(result))
            print(f"Записать результат в {filename_output}")
    except FileNotFoundError:
        print(f"файл {filename_input} не найден.")
    except Exception as e:
        print(f"Произошла ошибка：{e}")

calculate_sum(7, 2)
read_and_write_sum('input.txt', 'output.txt')