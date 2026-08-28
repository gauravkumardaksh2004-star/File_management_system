from pathlib import Path
import os
print('for create file press 1:  \n for read file press 2:  \n for update file press 3:  \n for delete file press 4:  \n')

Number = int(input('enter no. of operation:     ')  )   
try:
    def file_creation():
        name = input('enter file name:  ')
        path = Path(name)
        if not path.exists():

            with open(path,'x') as fs:
                print(f'your file {path} is created') 
        else:
            print(f'file {path} already exist') 
except Exception as err :
    print(f'your have and error - {err}')  

try:
    def file_reading():
        name = input('enter file name which you wants to read:  ')
        path = Path(name)
        if path.exists():
            with open(path, 'r') as fs:
                content = fs.read()
                print (f'your file content is :\n {content}') 
        else:
            print('file not exist')                      
except Exception as err:
    print(f'you have an error - {err}')
try:
    def file_updating():
        choice = int(input('enter 1 for Rename file:   \n enter 2 for update on a existing file:     \n enter 3 for create and overwrite data on a existing or a new file:     '))
        name = input('enter file name:  ')
        if choice ==1:
            newname = input('enter new name for your file:  ')
            new_path = Path(newname)
            path = Path(name)
            if not new_path.exists():
                path.rename(new_path)
                print('your file name is successfully changed')
            else:
                print('file already exist')    


        elif choice == 2:
            path = Path(name)
            
            data = input('enter data for update: \n ')
            if path.exists():
                with open(path, 'a') as fs:
                    add = fs.write('\n'+data)
                    print(f'your data is successfully added to the existing file {path}')
            else:
                print('file not exist')        
        elif choice == 3:
            path = Path(name)
            
            data = input('enter data for update: \n ')
            with open(name, 'w') as fs:
                add= fs.write('\n'+data)       
            print(f'your data us updated in file {name}')
except Exception as err:
    print(f'error is cached: {err}')
try:
    def file_deleting():
        name = input('enter file name for delete: ')
        path = Path(name)
        if path.exists():
            path.unlink()
            print('your file is successfully deleted')
        else:
            print("file not found!")            
except Exception as err:
    print(f'error is {err}')



if Number==1:
    file_creation()

elif Number == 2:
    file_reading()

elif Number == 3:
    file_updating()

elif Number == 4:
    file_deleting()

else:
    print('enter valid input - 1,2,3,4 only')                