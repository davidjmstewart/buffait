import unittest
import buffait

class TestSingleBufferSourceFile(unittest.TestCase):
    def test_single_buffer_graph(self):
        single_buffer_graph = buffait.make_graph('./tests/single_buffer.c')
        self.assertEqual(single_buffer_graph.get_actual_size(), 100)

if __name__ == '__main__':
    unittest.main()
