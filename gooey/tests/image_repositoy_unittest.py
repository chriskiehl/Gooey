'''
Image Repository acts as a funky dynamic singlton module.
'''
import os
import pytest
import tempfile


def test_variable_names_are_pushed_to_module_scope(expected_attrs):
  '''
  The dynamically initialized Globals() should contain the expected images at runtime
  '''
  from gooey.gui import image_repository
  assert all((attr in image_repository.__dict__) for attr in expected_attrs)


def test_patch_returns_error_on_invalid_dir():
  '''
  patch should explode with a helpful message if it
  cannot find the supplied directory
  '''
  from gooey.gui import image_repository

  with pytest.raises(IOError) as kaboom:
    image_repository.patch_images('foo/bar/not/a/path')

  # our error
  assert ' user supplied' in str(kaboom.value)
  assert 'foo/bar/not/a/path' in str(kaboom.value)


def test_module_scope_is_updated_on_patch(expected_attrs):
  '''
  Patch should update the module's globals() on success
  '''
  from gooey.gui import image_repository
  testing_icons = ('config_icon.png', 'success_icon.png')
  try:
    # setup
    make_user_files(*testing_icons)
    old_icon = image_repository.config_icon
    # load up our new icon(s)
    image_repository.patch_images(tempfile.tempdir)
    new_icon = image_repository.config_icon
    assert old_icon != new_icon
  finally:
    cleanup_temp(*testing_icons)


# helpers
def make_user_files(*filenames):
  for filename in filenames:
    with open(os.path.join(tempfile.gettempdir(), filename), 'w') as f:
      f.write('temp')

def cleanup_temp(*filenames):
  for filename in filenames:
    os.remove(os.path.join(tempfile.gettempdir(), filename))
