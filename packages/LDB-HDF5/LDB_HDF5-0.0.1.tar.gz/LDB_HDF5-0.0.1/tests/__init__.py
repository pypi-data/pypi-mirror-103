import tempfile
import shutil

keep_test_output_files = False


class CleanupMixin(object):
    def setUp(self):
        super(CleanupMixin, self).setUp()
        if keep_test_output_files:
            self.save_dir = "."
        else:
            self.save_dir = tempfile.mkdtemp()

    def tearDown(self):
        if not keep_test_output_files:
            shutil.rmtree(self.save_dir)
        super(CleanupMixin, self).tearDown()
