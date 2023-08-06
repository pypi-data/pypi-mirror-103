def dims(arr):
    dim_counter = 1
    prev, curr = arr, arr[0]
    while type(curr) == list:
        dim_counter += 1
        prev = curr
        if len(curr) != 0:
            curr = curr[0]
        else:
            break
    #if apparent innermost nested list does contains further lists, return -1
    #to indicate inconsistent dimensionality
    for i in prev:
        if type(i) == list:
            return -1
    return dim_counter

class ValidCheck:
    
    def __init__(self, array):
        self.array = array

    def is_equal_dim(self):
        print("Checking array dimensions. This may take a while for larger inputs.")
        dim = dims(self.array)
        for i in range(1, len(self.array)):
            curr_dim = dims(self.array[i:])
            if curr_dim != dim:
                print("Input array lacked consistent dimensionality. Exiting")
                return False
        print(f"Input array is {dim} dimensional.")
        return True
    
    def is_ragged(self):
        for sub_arr in self.array[1:]:
            if len(sub_arr) != len(self.array[0]):
                return True
        return False
    
    def base_checker(self):
        if type(self.array) != list:
            print("Input object was not of type 'list'. Exiting")
            return False
        if len(self.array) <= 1:
            print(f"Input array was of length {len(self.array)}. Exiting")
            return False
        if dims(self.array) != 2:
            print("Input array was not two-dimensional. Exiting")
            return False
        if self.is_ragged():
            print("Input array is raggged. Exiting")
            return False
        return True
    
    def run_checks(self, base_check = True, dim_check = False):
        check_val_base, check_val_dim = True, True
        if base_check:
            check_val_base = self.base_checker()
        if check_val_base and dim_check:
            check_val_dim = self.is_equal_dim()
        return check_val_base and check_val_dim