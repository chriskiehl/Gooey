import os


__author__ = 'Chris'

base_path = os.path.dirname(__file__)
image_dir = os.path.join(base_path, '../images')

alessandro_rei_checkmark = os.path.join(image_dir, "alessandro_rei_checkmark.png")
computer = os.path.join(image_dir, "computer.png")
computer2 = os.path.join(image_dir, "computer2.png")
computer3 = os.path.join(image_dir, "computer3.png")
icon = os.path.join(image_dir, "icon.ico")
images = os.path.join(image_dir, "images.jpg")
loader = os.path.join(image_dir, "loader.gif")
settings2 = os.path.join(image_dir, "settings2.png")
error = os.path.join(image_dir, "error.png")


def _list_images():
  # convenience function to list all images
  # the images directory in a format that can be copied
  # and pasted
  images = (f for f in os.listdir(image_dir))
  stmnts = ('{0} = os.path.join(image_dir, "{1}")'
              .format(os.path.splitext(im)[0], im)
            for im in images)


# _list_images()








