from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import json
import time
import shutil


class MyHandler(FileSystemEventHandler):

    # Called when a file appears in the watched folder
    def on_modified(self, event):
        # time.sleep(10)

        folderToTrack = "/Users/admin/Downloads"
        otherDestination = "/Users/admin/Documents/SortedDownloads/other-files/"

        for filename in os.listdir(folderToTrack):
            if filename != '.DS_Store':

                with open('destinations.json') as jsonfile:
                    destinations = json.load(jsonfile)

                    # Get file name and file extension
                    fileName, fileExtension = os.path.splitext(filename)

                    # Need this
                    if (fileExtension == ".crdownload"):
                        print("HERE!")
                        break

                    print("extension: " + fileExtension)
                    print("name: " + filename)
                    src = folderToTrack + "/" + filename

                    # Convert fileExtension to lowercase to handle differences
                    lowerCaseExtension = fileExtension.lower()

                    if lowerCaseExtension in destinations:
                        newDestination = destinations[lowerCaseExtension] + filename
                    else:
                        newDestination = None

                    if (newDestination):
                        if not os.path.exists(destinations[lowerCaseExtension]):
                            os.makedirs(destinations[lowerCaseExtension])

                        shutil.move(src, newDestination)
                    else:
                        if not os.path.exists(otherDestination):
                            os.makedirs(otherDestination)

                        shutil.move(src, otherDestination + filename)


if __name__ == "__main__":
    eventHandler = MyHandler()
    observer = Observer()
    folderToTrack = "/Users/admin/Downloads"
    observer.schedule(eventHandler, folderToTrack, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
