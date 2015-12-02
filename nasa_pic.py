import requests
import shutil
from datetime import date


def nasa_getter(local_date, local_data, local_image):
    """Function to call out to the Nasa pic of the day and save the image as well as the explanation for later.
       Nasa photo of the day surprisingly does not always have pictures, they can be videos.  This throws an
       exception for a key error.

       Parameters:
           local_date(str) :  Today's date
           local_data(str): Location of text file for explanation
           local_image(str): Location to save image data to

    """
    url = 'https://api.nasa.gov/planetary/apod?concept_tags=True&api_key=DEMO_KEY&hd=TRUE'
    nasa_apod = requests.get(url, stream=True)
    nasa_pic = nasa_apod.json()
    try:
        response = requests.get(nasa_pic['hdurl'], stream=True)
        nasa_data = open(local_data, 'a')
        nasa_data.write(local_date)
        nasa_data.write("\n")
        nasa_data.write(nasa_pic['explanation'])
        nasa_data.write("\n")
        nasa_data.close()
        with open(local_image, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    except KeyError:
        print "No image"

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

