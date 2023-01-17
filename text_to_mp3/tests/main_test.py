import os
from unittest import TestCase, main
from text_to_mp3.main import get_some_word, text_to_mp3


class TextToMp3(TestCase):

    def test_empty_file_name(self):
        with self.assertRaises(ValueError) as err:
            text_to_mp3("text", "")
        self.assertEqual("The file_name should not be an empty string", err.exception.args[0])

    def test_wrong_file_name(self):
        with self.assertRaises(FileNotFoundError) as err:
            text_to_mp3("text", ".\\mp3\\ccc\\test.mp3")
        self.assertEqual("No such file or directory", err.exception.args[0])

    def test_correct_file_name(self):
        file_name = ".\\test.mp3"
        self.assertEqual(text_to_mp3("text", file_name), True)

        os.remove(file_name)


class GetSomeWordTest(TestCase):

    def test_empty_url(self):
        with self.assertRaises(ValueError) as err:
            get_some_word("")
        self.assertEqual("The URL should not be an empty string", err.exception.args[0])

    def test_wrong_url(self):
        with self.assertRaises(ValueError) as err:
            get_some_word("test_url")
        self.assertEqual("Invalid URL: No scheme supplied.", err.exception.args[0])

    def test_correct_url(self):

        self.assertEqual(len(get_some_word("http://start-deutsch.ru/quiz/api/get_random_words?count=4")), 4)


if __name__ == "__main__":
    main()
