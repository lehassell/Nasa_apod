import requests
import shutil
import subprocess
from datetime import date


def nasa_getter(local_date, local_data, local_image):
    """Function to call out to the Nasa pic of the day and save the image as well as the explanation

    """
    url = 'https://api.nasa.gov/planetary/apod?concept_tags=True&api_key=DEMO_KEY&hd=TRUE'
    nasa_apod = requests.get(url, stream=True)
    nasa_pic = nasa_apod.json()
    response = requests.get(nasa_pic['hdurl'], stream=True)

    # I want to check if its an image or other media type.
    if nasa_pic['media_type'] == 'image':
        # Stream out an IO for the picture
        with open(local_image, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        # I then want to log the explanation.  This still has problems with non ascii characters
        nasa_data = open(local_data, 'a')
        nasa_data.write(local_date)
        nasa_data.write("\n")

        try:
            nasa_data.write(nasa_pic['explanation'])
            nasa_data.write("\n")
        except UnicodeEncodeError:
            nasa_data.write("Non ASCII Characters")
            nasa_data.write("\n")
            pass

        nasa_data.close()
        del response
    else:
        print nasa_pic['media_type']

    return()


if __name__ == '__main__':
    # Check the date
    date = str(date.today())
    # Determine the file location
    nasa_dir = "/Users/lehassell/Pictures//Nasa/"
    nasa_data_file = nasa_dir + 'data.txt'
    nasa_img = "/Users/lehassell/Pictures//Nasa/" + date + "_nasa.png"

    # Don't duplicate if its been run before
    if date not in open(nasa_data_file).read():
        nasa_getter(date, nasa_data_file, nasa_img)
    else:
        print 'present'


    # Set the image as background
    place_string = 'tell application "Finder" to set desktop picture to POSIX file "'+ nasa_img +'"'
    subprocess.call(['osascript', '-e', place_string])

