from typing import List
import unittest
import buffait

class TestBufferNodeCreation(unittest.TestCase):
    def test_single_buffer_creation(self):
        buffer_list: List[buffait.BufferNode] = buffait.make_nodes_from_line('char bufA[BUFF_SIZE];')
        buffer = buffer_list[0]
        self.assertIsNotNone(buffer_list)
        self.assertEqual(len(buffer_list), 1)
        self.assertEqual(buffer.name, 'bufA')
        self.assertEqual(buffer.size, 'BUFF_SIZE')

    def test_two_nodes_on_one_line(self):
        node_list: List[buffait.Node] = buffait.make_nodes_from_line(
            'int BUFF_SIZE = 10; char bufA[BUFF_SIZE];')
        buffer_list = list(
            filter(lambda x: type(x) == buffait.BufferNode, node_list)
        )

        integer_list = list(
            filter(lambda x: type(x) == buffait.IntegerNode, node_list)
        )


        buffer = buffer_list[0]
        integer = integer_list[0]

        self.assertIsNotNone(buffer_list)
        self.assertEqual(len(buffer_list), 1)

        self.assertIsNotNone(integer_list)
        self.assertEqual(len(integer_list), 1)

        self.assertEqual(buffer.name, 'bufA')
        self.assertEqual(buffer.size, 'BUFF_SIZE')

        self.assertEqual(integer.name, 'BUFF_SIZE')
        self.assertEqual(integer.value, '10')

    def test_two_buffers_on_one_line(self):

        node_list: List[buffait.Node] = buffait.make_nodes_from_line(
            'char bufA[BUFF_SIZE]; char bufB[BUFF_SIZE];')
        buffer_list = list(
            filter(lambda x: type(x) == buffait.BufferNode, node_list)
        )

        self.assertIsNotNone(buffer_list)
        self.assertEqual(len(buffer_list), 2)

        buffer_A = buffer_list[0]
        buffer_B = buffer_list[1]

        self.assertIsNotNone(buffer_A)
        self.assertIsNotNone(buffer_B)

        self.assertEqual(buffer_A.name, 'bufA')
        self.assertEqual(buffer_A.size, 'BUFF_SIZE')

        self.assertEqual(buffer_B.name, 'bufB')
        self.assertEqual(buffer_B.size, 'BUFF_SIZE')


class TestBufferNodeCreation(unittest.TestCase):
    def test_node_linking(self):
        lines_of_source_code: List[str] = [
            'int j = 2;',
            'int i = j;',
            'int myArray[i]'
        ]

        node_list = list(
            buffait.flat_map(
                map(lambda l: buffait.make_nodes_from_line(l), lines_of_source_code)
            )
        )


        self.assertEqual(len(node_list), 3)

        buffer = node_list[2]
        self.assertEqual(buffer.name, 'myArray')
        self.assertEqual(buffer.size, 'i')


        buffait.populate_size_dependencies(buffer, node_list)
        self.assertEqual(buffer.name, 'myArray')
        self.assertEqual(buffer.size, 'i')
        self.assertEqual(buffer.get_actual_size(), 2)

        
# class TestSingleBufferSourceFile(unittest.TestCase):
#     def test_single_buffer_size(self):
#         single_buffer_graph = buffait.make_graph('./tests/single_buffer.c')
#         # self.assertEqual(single_buffer_graph.get_actual_size(), 100)

if __name__ == '__main__':
    unittest.main()
