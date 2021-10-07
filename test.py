from typing import List
import unittest
import buffait

class Test_size_to_dependency_array(unittest.TestCase):

    def test_simple_constant_size_dependency(self):
        source_code_line = 'int myBuffer[3];'
        m = buffait.buffer_regex.search(source_code_line)
        dependency_array = buffait.BufferNode.size_to_dependency_array(m.group('size'))
        self.assertEqual(len(dependency_array), 1) # expect a single dependency: a constant value of 3
        self.assertEqual(dependency_array, [3])    # the value in the dependency array is simply the integer value 3

    def test_simple_symbolic_size_dependency(self):
        integer_node = buffait.make_nodes_from_line('int j = 3;', [])
        source_code_line = 'int myBuffer[j];'
        m = buffait.buffer_regex.search(source_code_line)
        dependency_array = buffait.BufferNode.size_to_dependency_array(m.group('size'))
        self.assertEqual(len(dependency_array), 1) 
        self.assertEqual(dependency_array[0].name, 'j') 
        self.assertEqual(type(dependency_array[0]), buffait.IntegerNode) 

    def test_complex_dependency(self):
        j_node = buffait.make_nodes_from_line('int j = 3;', [])
        i_node = buffait.make_nodes_from_line('int i = 13;', [j_node])

        source_code_line = 'char character_array[10 + i - 1 + j];'
        m = buffait.buffer_regex.search(source_code_line)
        dependency_array = buffait.BufferNode.size_to_dependency_array(m.group('size'))
        integer_node_dependencies = list(filter(lambda x: type(x) == buffait.IntegerNode, dependency_array))
        constant_dependencies = list(filter(lambda x: type(x) == int, dependency_array))
        self.assertEqual(len(dependency_array), 3)           # 3 total dependencies
        self.assertEqual(len(integer_node_dependencies), 2)  # 2 IntegerNode types
        self.assertEqual(len(constant_dependencies), 1)      # 1 constant integer type
        self.assertEqual(constant_dependencies[0], 9)   # buffer declaration had 2 scalar components: 10 and -1 which add to 9

class Test_create_dependency_array(unittest.TestCase):

    # def test_simple_symbolic_size_dependency(self):
    #     integer_node = buffait.make_nodes_from_line('int j = 3;', [])[0]
    #     source_code_line = 'int myBuffer[j];'
    #     m = buffait.buffer_regex.search(source_code_line)
    #     dependency_array = buffait.BufferNode.create_dependency_array(m.group('size'), [integer_node])
    #     self.assertEqual(len(dependency_array), 1) 
    #     self.assertEqual(dependency_array[0].name, integer_node.name) 
    #     self.assertEqual(type(dependency_array[0]), buffait.IntegerNode) 

    def test_complex_dependency(self):
        dependency_lines_of_code: List[str] = [
            'int j = 3;',
            'int i = 2;',
        ]

        # integer_dependencies = list(
        #     buffait.flat_map(
        #         map(lambda l: buffait.make_nodes_from_line(l), dependency_lines_of_code)
        #     )
        # )
        integer_dependencies = []
        for l in dependency_lines_of_code:
            n = buffait.make_nodes_from_line(l, integer_dependencies)
            integer_dependencies += n

        source_code_line = 'char character_array[10 + i - 1 + j];'
        m = buffait.buffer_regex.search(source_code_line)
        dependency_array = buffait.BufferNode.create_dependency_array(m.group('size'), integer_dependencies)
        integer_node_dependencies = list(filter(lambda x: type(x) == buffait.IntegerNode, dependency_array))
        constant_dependencies = list(filter(lambda x: type(x) == int, dependency_array))

        self.assertEqual(len(dependency_array), 3)           # 3 total dependencies
        self.assertEqual(len(integer_node_dependencies), 2)  # 2 IntegerNode types
        self.assertEqual(len(constant_dependencies), 1)      # 1 constant integer type
        self.assertEqual(constant_dependencies[0], 9)   # buffer declaration had 2 scalar components: 10 and -1 which add to 9


# class TestIntegerNodeCreation(unittest.TestCase):

#     def test_single_integer_node(self):
#         integer_node_list: List[buffait.BufferNode] = buffait.make_nodes_from_line('int my_INT=10;')
#         self.assertIsNotNone(integer_node_list)
#         self.assertEqual(len(integer_node_list), 1)
#         integer_node = integer_node_list[0]
#         self.assertEqual(integer_node.name, 'my_INT')
#         self.assertEqual(len(integer_node.size_dependencies), 1) 
#         self.assertEqual(integer_node.size_dependencies[0], 10) # N.B. it is a string value and IntegerNode, until we 

#     def test_two_integer_nodes(self):
#         integer_list: List[buffait.Node] = buffait.make_nodes_from_line(
#             'int j = 10; int i = 10;')


#         j = integer_list[0]
#         i = integer_list[1]

#         self.assertIsNotNone(integer_list)
#         self.assertEqual(len(integer_list), 2)

#         # j variable
#         self.assertEqual(j.name, 'j')
#         self.assertEqual(len(j.value_dependencies), 1)
#         self.assertEqual(j.value_dependencies[0], 10)

#         # i variable
#         self.assertEqual(i.name, 'i')
#         self.assertEqual(len(i.value_dependencies), 1)
#         self.assertEqual(i.value_dependencies[0], 10)


# class TestBufferNodeCreation(unittest.TestCase):

#     def test_single_buffer_creation(self):
#         buffer_list: List[buffait.BufferNode] = buffait.make_nodes_from_line('char bufA[BUFF_SIZE];')
#         buffer = buffer_list[0]
#         self.assertIsNotNone(buffer_list)
#         self.assertEqual(len(buffer_list), 1)
#         self.assertEqual(buffer.name, 'bufA')
#         self.assertEqual(len(buffer.size_dependencies), 1) 

#         self.assertEqual(buffer.size_dependencies[0], 'BUFF_SIZE') # N.B. it is a string value and IntegerNode, until we 

#     def test_two_nodes_on_one_line(self):
#         node_list: List[buffait.Node] = buffait.make_nodes_from_line(
#             'int BUFF_SIZE = 10; char bufA[BUFF_SIZE];')
#         buffer_list: List[buffait.BufferNode] = list(
#             filter(lambda x: type(x) == buffait.BufferNode, node_list)
#         )

#         integer_list = list(
#             filter(lambda x: type(x) == buffait.IntegerNode, node_list)
#         )

#         buffer = buffer_list[0]
#         integer = integer_list[0]

#         self.assertIsNotNone(buffer_list)
#         self.assertEqual(len(buffer_list), 1)

#         self.assertIsNotNone(integer_list)
#         self.assertEqual(len(integer_list), 1)

#         self.assertEqual(buffer.name, 'bufA')
#         self.assertEqual(len(buffer.size_dependencies), 1)

#         self.assertEqual(integer.name, 'BUFF_SIZE')
#         self.assertEqual(integer.value, '10')

#     def test_two_buffers_on_one_line(self):

#         node_list: List[buffait.Node] = buffait.make_nodes_from_line(
#             'char bufA[BUFF_SIZE]; char bufB[BUFF_SIZE];')
#         buffer_list = list(
#             filter(lambda x: type(x) == buffait.BufferNode, node_list)
#         )

#         self.assertIsNotNone(buffer_list)
#         self.assertEqual(len(buffer_list), 2)

#         buffer_A: buffait.BufferNode = buffer_list[0]
#         buffer_B: buffait.BufferNode = buffer_list[1]

#         self.assertIsNotNone(buffer_A)
#         self.assertIsNotNone(buffer_B)

#         self.assertEqual(buffer_A.name, 'bufA')
#         self.assertEqual(len(buffer_A.size_dependencies), 1)
#         self.assertEqual(buffer_A.size_dependencies[0].name, 'BUFF_SIZE')

#         self.assertEqual(buffer_B.name, 'bufB')
#         self.assertEqual(len(buffer_B.size_dependencies), 1)
#         self.assertEqual(buffer_B.size_dependencies[0].name, 'BUFF_SIZE')

# class Test_make_buffer_trees(unittest.TestCase):

#     def test_complex_buffer_expression(self):

#         lines_of_source_code: List[str] = [
#             'int j = 3;',
#             'int i = 0;',
#             'char character_array[10 + i - 1 + j];'
#         ]

#         trees: List[buffait.BufferNode] = buffait.make_buffer_trees(lines_of_source_code)
#         self.assertEqual(len(trees), 1)
#         root = trees[0]
#         self.assertEqual(root.name, 'character_array')
#         self.assertEqual(len(root.size_dependencies), 3)
#         self.assertEqual(root.size_dependencies[0], 3)

#         integer_node_dependencies = list(filter(lambda x: type(x) == buffait.IntegerNode), root.size_dependencies)
#         constant_dependencies = list(filter(lambda x: type(x) == int), root.size_dependencies)

#         self.assertEqual(len(integer_node_dependencies), 2)  # 2 IntegerNode types
#         self.assertEqual(len(constant_dependencies), 1)      # 1 constant integer type
#         self.assertEqual(len(constant_dependencies[0]), 9)   # buffer declaration had 2 scalar components: 10 and -1 which add to 9
#         self.assertEqual(root.get_actual_size(), 12)  

        
# class TestSingleBufferSourceFile(unittest.TestCase):
#     def test_single_buffer_size(self):
#         single_buffer_graph = buffait.make_graph('./tests/single_buffer.c')
#         # self.assertEqual(single_buffer_graph.get_actual_size(), 100)

if __name__ == '__main__':
    unittest.main()
