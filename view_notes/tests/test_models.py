from django.test import TestCase
from view_notes.models import Notes

# models test
class NotesTest(TestCase):

    def create_notes(self, judul="only a test", isi="yes, this is only a test"):
        return Notes.objects.create(judul=judul, isi=isi)

    def test_notes(self):
        w = self.create_notes()
        self.assertTrue(isinstance(w, Notes))
        self.assertEqual(w.__str__(), w.judul)