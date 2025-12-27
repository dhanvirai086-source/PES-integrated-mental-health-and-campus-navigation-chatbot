'''def process_data(data_list, callback):
    for item in data_list:
        print(callback(item))
def square_num(n):
    return n * n
def double_num(n):
    return n * 2
numbers = [1, 5, 9, 12]
print("Using square_num callback:")
process_data(numbers, square_num)
print("\nUsing double_num callback:")
process_data(numbers, double_num)'''

'''def custom_sort(items, key_callback):
    return sorted(items, key=key_callback)
def sort_by_price(item):
    return item[1]    
def sort_by_quantity(item):
    return -item[2] 
store_items = [('apple', 0.5, 10),('banana', 0.2, 20),('cherry', 2.0, 5),('date', 1.5, 8)]
print("Sorted by price (low → high):")
print(custom_sort(store_items, sort_by_price))

print("\nSorted by quantity (high → low):")
print(custom_sort(store_items, sort_by_quantity))'''

def make_power_of(n):
    def x(4):
        return x**n
print(x())    
    
    
     