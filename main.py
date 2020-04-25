import hashlib
#Hen Biton 206571762
#Tamir Yaresko 315144964
# not allowed to use math
def log2(num):
    ans = 0
    while num != 1:
        num /= 2
        ans += 1
    return ans


# represent every vertex in the merkle tree
class MerkleNode:
    def __init__(self, value, position, left=None, right=None):
        self.value = value
        self.position = position
        self.left_child = left
        self.right_child = right


# tree of nodes
class MerkleTree:
    def __init__(self, list_of_values):
        self.list_of_values = list_of_values
        self.list_of_nodes = []
        self.leaves = []

    # convert the input from user to vertices
    def create_leaves(self):
        count = 0
        for value in self.list_of_values:
            leaf = MerkleNode(value, count % 2)  # 0 is left 1 is right
            self.list_of_nodes.append(leaf)
        self.leaves = self.list_of_nodes.copy()

    # brute force for finding nonce
    def nonce(self, num_of_zeros):
        root_value = self.list_of_nodes[0].value
        i = 0
        while encrypt_hash(str(i) + root_value)[:int(num_of_zeros)] != '0' * int(num_of_zeros):
            i += 1
        return str(i) + " " + encrypt_hash(str(i) + root_value)

    def create_tree(self):
        self.create_leaves()
        while len(self.list_of_nodes) != 1:
            i = 0
            left_children = self.list_of_nodes[0::2]
            right_children = self.list_of_nodes[1::2]
            self.list_of_nodes.clear()
            for l_child, r_child in zip(left_children, right_children):
                self.list_of_nodes.append(MerkleNode(encrypt_hash(l_child.value + r_child.value), i % 2, l_child, r_child))
                i += 1
        return self.list_of_nodes[0]

    # return the required vertices to prove inclusion of given index
    def proof_of_inclusion(self, index):
        parents_position = []
        proof_list = []
        curr_node = self.list_of_nodes[0]
        num_of_leaves = len(self.leaves)
        while num_of_leaves != 1:
            num_of_leaves /= 2
            if index < num_of_leaves:
                proof_list.append(curr_node.right_child)
                curr_node = curr_node.left_child
            else:
                proof_list.append(curr_node.left_child)
                curr_node = curr_node.right_child
        return proof_list


# check if given value is included in merkle tree
def check_inclusion(value, nodes, root):
    values = nodes[1::2]
    print(values)
    positions = nodes[0::2]
    print(positions)
    for curr_val, position in zip(values, positions):
        if position == 'l':
            value = encrypt_hash(curr_val + value)
        else:
            value = encrypt_hash(value + curr_val)
    print(value)
    if value == root:
        return True
    return False


# SHA256 hash
def encrypt_hash(hash_str):
    sha_signature = hashlib.sha256(hash_str.encode()).hexdigest()
    return sha_signature


def main():
    tree = MerkleTree([])
    while True:
        condition = input()
        condition = condition.split()
        if condition[0] == "1":
            data = condition[1:]
            tree = MerkleTree(data)
            tree.create_tree()

        elif condition[0] == "2":
            str_proof = ""
            lis = tree.proof_of_inclusion(int(condition[1]))
            for i in reversed(lis):
                if i.position == 0:
                    str_proof += "l " + i.value + " "
                else:
                    str_proof += "r " + i.value + " "
            print(str_proof)
        elif condition[0] == "3":
            print(check_inclusion(condition[1], condition[3:], condition[2]))
        elif condition[0] == "4":
            print(tree.nonce(condition[1]))
        elif condition[0] == "5":
            exit(0)
        else:
            exit(0)


if __name__ == "__main__":
    main()
