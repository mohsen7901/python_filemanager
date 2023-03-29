import os
#I used copyfile function from shutil module to copy content of a file to other place 
from shutil import copyfile

if not os.path.exists("py_Recycle_Bin"):
    os.mkdir("py_Recycle_Bin")

class FileManager:
    def find(self, name:str, address:str):
        """
        This method find all files with specified name in the specified address.
        With the help of os.walk function we search all directories and subdirectories
            of specified address and check whether a certain file exist there or not.
            each iterator returns a tuple of root, dirs, and files respectively.
            root is the parent directory that is beeing searched, dirs is a list of all directories,
            and files is a list of all files in this root directory.
        """
        output_list = [] 
        for (root, dirs, files) in os.walk(address):
            if name in files:
                output_list.append(os.path.join(root, name))
        return output_list

    def create_file(self, name:str, address:str):
        """
        This method makes a file with specified name in the specified address.
        if the file already exists nothing is done.
        """
        path = os.path.join(address, name)
        if not os.path.exists(path):
            f = open(path, "w")
            f.close()

    def create_dir(self, name:str, address:str):
        """
        This method creates a directory with specified name in the specified address.
        If directory alreaay exists nothing is done.
        I used makedirs function that makes all directories in the middle from parent dir
        to name if needed.
        for example if desired directory is c:/example/test, and example directory doesn't exist,
        first example is created and then test directory will be made.
        """
        path = os.path.join(address, name)
        os.makedirs(path, exist_ok=True)

    def delete(self, name:str, address:str):
        """
        This method deletes a specified file with name of name in the address.
        If this file does not exist nothing is happen.
        this method don't permenantly remove a file and copies the file to a directory named 
        py_Recycle_Bin in current working directory that can be restored in the future.
        path of deleted file is saved in the deleted_files.txt text file.
        """
        path = os.path.join(address, name)
        if os.path.exists(path):
            with open("deleted_files.txt", "a") as f:
                f.write(f"{path} {name}\n")
            deleted_file_path = os.path.join("py_Recycle_Bin", address)
            os.makedirs(deleted_file_path, exist_ok=True)
            deleted_file = os.path.join(deleted_file_path, name)
            f = open(deleted_file, "w")
            f.close()
            copyfile(path, deleted_file)
            os.remove(path)

    def restore(self, name:str):
        """
        This method restores a deleted file with the name of name from py_Recycle_Bin
        directory.
        If some files with the same name but different directories are deleted continously,
        files will be restored from the last deleted to the first i.e. LIFO (last in first out!)
        """
        with open("deleted_files.txt", "r") as f:
            deleted_files = f.readlines()
        with open("deleted_files.txt", "w") as f:
            line_number = len(deleted_files)
            state_flag = True
            for line in reversed(deleted_files):
                line = line.strip("\n")
                path = line.split()[0]
                file = line.split()[1]
                if file == name:
                    deleted_file_path = os.path.join("py_Recycle_Bin", path)
                    f1 = open(path, "w")
                    f1.close()
                    copyfile(deleted_file_path, path)
                    os.remove(deleted_file_path)
                    state_flag = True
                    break
                else:
                    line_number -= 1
            counter = 1
            for line in deleted_files:
                if counter == line_number and state_flag:
                    continue
                else:
                    f.write(line)
                    counter += 1




# fm = FileManager()

# fm.create_dir('test', '.')
# fm.create_dir('test1', 'test')
# fm.create_dir('test2', 'test/test1/')

# fm.create_file('test.txt', 'test')
# fm.create_file('test.txt', 'test/test1')
# fm.create_file('test.txt', 'test/test1/test2')

# print(fm.find('test.txt', 'test'))

# fm.delete('test.txt', 'test')
# fm.delete('test.txt', 'test/test1/')
# fm.delete('test.txt', 'test/test1/test2')
# fm.restore('test.txt')
# fm.restore('test.txt')

# fm.create_dir("testfolder", "project4")
# fm.create_file("test.py","project4/testfolder/")
# fm.delete("test.py","project4/testfolder/")
# fm.restore("test.py")