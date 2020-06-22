from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import json
import time


class MyHandler(FileSystemEventHandler):

    def on_modified(self, event):
        folderToTrack = "/Users/admin/Desktop/myFolder"
        miscDestination = "/Users/admin/Desktop/newFolder/misc"

        for filename in os.listdir(folderToTrack):
            if filename != '.DS_Store':

                with open('destinations.json') as jsonfile:
                    destinations = json.load(jsonfile)

                    # Get file name and file extension
                    fileName, fileExtension = os.path.splitext(filename)
                    print("extension: " + fileExtension)
                    src = folderToTrack + "/" + filename

                    if fileExtension in destinations:
                        newDestination = destinations[fileExtension] + filename
                    else:
                        newDestination = None

                    if (newDestination):
                        os.rename(src, newDestination)
                    else:
                        os.rename(src, miscDestination + "/" + filename)


if __name__ == "__main__":
    eventHandler = MyHandler()
    observer = Observer()
    folderToTrack = "/Users/admin/Desktop/myFolder"
    observer.schedule(eventHandler, folderToTrack, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
