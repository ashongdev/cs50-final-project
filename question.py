numbers = []
while True:
    num = input("Num: ")

    if num.lower() == "stop":
        break
    else:
        try:
            numbers.append(int(num))
        except ValueError:
            print("Please enter a valid number")
            pass


def find_average():
    num_length = len(numbers)
    sum_of_num = 0
    for num in numbers:
        sum_of_num += num

    avg = 0
    if len(numbers) > 0:
        avg = sum_of_num / num_length
    else:
        pass

    return avg


def find_largest():
    if len(numbers) > 0:
        largest = numbers[0]

        for num in numbers:
            if num > largest:
                largest = num
        return largest
    else:
        return "List is empty"


def find_smallest():
    if len(numbers) > 0:
        smallest = numbers[0]

        for num in numbers:
            if num < smallest:
                smallest = num
        return smallest
    else:
        return "List is empty"


def count():
    average = find_average()

    above_average = 0
    below_average = 0
    equal_to = 0

    for num in numbers:
        if num > average:
            above_average += 1
        elif num < average:
            below_average += 1
        else:
            equal_to += 1

    print(f"{above_average} number(s) are above average")
    print(f"{below_average} number(s) are below average")
    print(f"{equal_to} number(s) are equal to average")


largest_num = find_largest()
smallest_num = find_smallest()

print(f"Average: {find_average()}")
print(f"Largest Number: {largest_num}")
print(f"Smallest Number: {smallest_num}")

count()

# 1. Asks the user for numbers until they type "stop".
# 2. Finds the largest, smallest, and average of the numbers.
# 3. Also, count how many numbers are above average and how many are below average.
