import os
import tempfile
import unittest
from attic.testsuite import AtticTestCase
from attic.xattr import is_enabled, getxattr, setxattr, listxattr

@unittest.skipUnless(is_enabled(), 'xattr not enabled on filesystem')
class XattrTestCase(AtticTestCase):

    def setUp(self):
        self.tmpfile = tempfile.NamedTemporaryFile()
        self.symlink = os.path.join(os.path.dirname(self.tmpfile.name), 'symlink')
        os.symlink(self.tmpfile.name, self.symlink)

    def tearDown(self):
        os.unlink(self.symlink)

    def test(self):
        self.assert_equal(listxattr(self.tmpfile.name), [])
        self.assert_equal(listxattr(self.tmpfile.fileno()), [])
        self.assert_equal(listxattr(self.symlink), [])
        setxattr(self.tmpfile.name, 'user.foo', b'bar')
        setxattr(self.tmpfile.fileno(), 'user.bar', b'foo')
        self.assert_equal(set(listxattr(self.tmpfile.name)), set(['user.foo', 'user.bar']))
        self.assert_equal(set(listxattr(self.tmpfile.fileno())), set(['user.foo', 'user.bar']))
        self.assert_equal(set(listxattr(self.symlink)), set(['user.foo', 'user.bar']))
        self.assert_equal(listxattr(self.symlink, follow_symlinks=False), [])
        self.assert_equal(getxattr(self.tmpfile.name, 'user.foo'), b'bar')
        self.assert_equal(getxattr(self.tmpfile.fileno(), 'user.foo'), b'bar')
        self.assert_equal(getxattr(self.symlink, 'user.foo'), b'bar')
