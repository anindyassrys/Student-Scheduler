from django.test import TestCase
from view_notes.forms import NotesForm

# form test
class NotesFormTest(TestCase):
    def test_valid_form(self):
        form = NotesForm(data={"judul": "test", "isi": "hanyatest"})
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        form = NotesForm(data={"judul": "", "isi": ""})
        self.assertFalse(form.is_valid())