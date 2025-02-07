import unittest
from unittest.mock import patch, MagicMock
from presentation.cli import AITuberCLI


class TestCLI(unittest.TestCase):
    @patch("presentation.cli.AITuber")
    @patch("builtins.input", return_value="test_video_id")
    def test_run(self, mock_input, MockAITuber):
        mock_aituber = MockAITuber.return_value
        cli = AITuberCLI()
        cli.run()
        mock_aituber.start.assert_called_once_with("test_video_id")


if __name__ == "__main__":
    unittest.main()
