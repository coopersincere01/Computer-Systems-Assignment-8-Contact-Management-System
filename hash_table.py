class Contact:
    """Stores a contact's name and phone number."""

    def __init__(self, name: str, number: str):
        self.name = name
        self.number = number

    def __str__(self) -> str:
        return f"{self.name}: {self.number}"


class Node:
    """Stores one contact and links to the next node after a collision."""

    def __init__(self, key: str, value: Contact):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """Stores contacts in a fixed-size list using separate chaining."""

    def __init__(self, size: int):
        if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
            raise ValueError("Hash table size must be a positive integer")

        self.size = size
        self.data = [None] * size

    def hash_function(self, key: str) -> int:
        total = 0

        for char in key:
            total += ord(char)

        return total % self.size

    def insert(self, key: str, number: str) -> None:
        index = self.hash_function(key)
        current = self.data[index]

        if current is None:
            self.data[index] = Node(key, Contact(key, number))
            return

        while current is not None:
            if current.key == key:
                current.value.number = number
                return

            if current.next is None:
                current.next = Node(key, Contact(key, number))
                return

            current = current.next

    def search(self, key: str):
        index = self.hash_function(key)
        current = self.data[index]

        while current is not None:
            if current.key == key:
                return current.value

            current = current.next

        return None

    def print_table(self) -> None:
        for index in range(self.size):
            current = self.data[index]

            if current is None:
                print(f"Index {index}: Empty")
            else:
                contacts = []

                while current is not None:
                    contacts.append(f"- {current.value}")
                    current = current.next

                print(f"Index {index}: {' '.join(contacts)}")


# Test the Contact and Node classes
if __name__ == "__main__":

    print("CONTACT AND NODE TESTS")

    contact_1 = Contact("Riley", "123-456-7890")
    node_1 = Node(contact_1.name, contact_1)

    assert str(contact_1) == "Riley: 123-456-7890"
    assert node_1.key == "Riley"
    assert node_1.value is contact_1
    assert node_1.next is None

    print(contact_1)
    print(node_1.key)
    print(node_1.value)
    print(node_1.next)

    # Test an empty hash table
    print("\nEMPTY TABLE")

    table = HashTable(10)

    assert table.size == 10
    assert len(table.data) == 10
    assert table.search("Chris") is None

    table.print_table()

    # Test inserting and searching for contacts
    print("\nINSERT AND SEARCH TESTS")

    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")

    assert str(table.search("John")) == "John: 909-876-1234"
    assert str(table.search("Rebecca")) == "Rebecca: 111-555-0002"

    print("Search result:", table.search("John"))
    table.print_table()

    # Test collision handling
    print("\nCOLLISION TEST")

    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")

    assert table.hash_function("Amy") == table.hash_function("May") == 5
    assert str(table.search("Amy")) == "Amy: 111-222-3333"
    assert str(table.search("May")) == "May: 222-333-1111"
    assert table.data[5].next is not None

    print("Amy index:", table.hash_function("Amy"))
    print("May index:", table.hash_function("May"))

    table.print_table()

    # Test updating an existing contact
    print("\nDUPLICATE CONTACT TEST")

    old_rebecca = table.search("Rebecca")

    table.insert("Rebecca", "999-444-9999")

    assert table.search("Rebecca") is old_rebecca
    assert table.search("Rebecca").number == "999-444-9999"

    print("Updated Rebecca:", table.search("Rebecca"))

    # Test updating a contact inside a collision chain
    old_may = table.search("May")

    table.insert("May", "333-444-5555")

    assert table.search("May") is old_may
    assert table.search("May").number == "333-444-5555"
    assert table.data[5].next.next is None

    print("Updated May:", table.search("May"))

    table.print_table()

    # Test searching for a contact that does not exist
    print("\nMISSING CONTACT TEST")

    assert table.search("Chris") is None

    print(table.search("Chris"))

    print("\nAll tests passed!")

# DESIGN MEMO
#
# I chose a hash table for this contact management system because the main
# task is finding a phone number when someone enters a contact's name.
# With a regular list, the program might have to check each contact until
# it finds the right one. That takes more time as the contact list grows.
# A hash table uses the name to calculate an index, so it can usually go
# directly to the area where the contact is stored. This gives searches
# an average time complexity of O(1), which makes sense for a phonebook.
#
# My hash function adds the Unicode values of the letters in a name and
# uses the remainder after dividing by the table size. Sometimes two
# different names end up at the same index. For example, Amy and May both
# go to index 5 in a table with ten slots. I handled these collisions
# with separate chaining. Each position can hold a linked list of nodes,
# so both contacts can be stored and searched without losing information.
# If a name is entered again, my insert method updates the number instead
# of adding another copy of the contact.
#
# An engineer might choose a hash table instead of a list when fast
# searches and updates matter more than keeping items in order. A balanced
# search tree would be more useful if the program often needed sorted
# names or a range of names. Hash tables also use extra memory, and too
# many collisions can slow searches down. For this assignment, the simple
# hash function is enough to demonstrate the idea, although a larger
# real-world system would benefit from a better hash function and resizing.    