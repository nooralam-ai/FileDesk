from pathlib import Path
import os
def createfile():
    try:
        name=input("please tell your file name :-")
        path=Path(name)
        if not path.exists():
            with open(path, "w") as fs:
                data=input("what you want to write:-")
                fs.write(data)
            print("file created successfully")
        else:
            print("Error file name already exists")
    except Exception as err:
        print(f"an error occured as {err}")
def readfile():
    try:
        name=input("please tell your file name:-")
        path=Path(name)
        if path.exists():
            with open(path, "r") as fs:
                content=fs.read()
                print(content)
        else:
            print("error no file such exists:")  
    except Exception as err:
        print(f"an error occured as {err}")     
def updatefile():
    try:
        name=input("tell your file name:-")
        path=Path(name)
        if path.exists():
            print("operations")
            print("1. Renaming the file")
            print("2. Appending the content")
            print("3. Overiting the file")
            choice=int(input("Enter your option:-"))
            if choice==1:
                new_name=input("tell your new file name:-")
                new_path=Path(new_name)
                if not new_path.exists():
                    path.rename(new_path)
                    print("renamed successfully")
                else:
                    print("file already exists")
            elif choice==2:
                with open(path,"a") as fs:
                    data=input("what do you want to append:-")
                    fs.write("\n"+data)
                print("succssfully appended")
            elif choice==3:
                with open(path, "w") as fs:
                    data=input("what do you weant to overwrite:-")
                    fs.write("\n"+data)
                print("successfully overwritten")
    except Exception as err:
        print(f"an error occurred as{err}")
def deletefile():
    try:
        name=input("please tell your file name:-")
        path=Path(name)
        if path.exists():
            path.unlink()
            print("file deleted succesfully")
        else:
            print("no file such exists")
    except Exception as err:
        print(f"an error occured as{err}")
print("press 1 for creating a file.")
print("press 2 for reading a file.")
print("press 3 for updating a file.")
print("press 4 for deleting a file.")

a=int(input("\n Tell your response: "))
if a==1:
    createfile()
if a==2:
    readfile()
if a==3:
    updatefile()
if a==4:
    deletefile()
