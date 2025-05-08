from model.person import Person
from typing import List, Optional

class NodeN:
    def __init__(self, person: Person):
        self.person = person
        self.children: List['NodeN'] = []

    def add_child(self, child: 'NodeN'):
        self.children.append(child)

    def remove_child_by_id(self, id_to_remove: int):
        self.children = [c for c in self.children if c.person.id != id_to_remove]


class TreeN:
    def __init__(self):
        self.roots: List[NodeN] = []

    def get_all_nodes(self) -> List[NodeN]:
        all_nodes = []

        def collect(node: NodeN):
            all_nodes.append(node)
            for child in node.children:
                collect(child)

        for root in self.roots:
            collect(root)

        return all_nodes

    def find_node_by_id(self, id: int) -> Optional[NodeN]:
        for node in self.get_all_nodes():
            if node.person.id == id:
                return node
        return None

    def create_person(self, person: Person) -> NodeN:
        if self.find_node_by_id(person.id):
            raise ValueError(f"Ya existe una persona con id={person.id}")

        new_node = NodeN(person)

        if person.parent_id is None:
            self.roots.append(new_node)
        else:
            parent = self.find_node_by_id(person.parent_id)
            if parent:
                parent.add_child(new_node)
            else:
                raise ValueError(f"Padre con id={person.parent_id} no encontrado.")

        return new_node

    def get_persons(self) -> List[Person]:
        return [node.person for node in self.get_all_nodes()]

    def update_person(self, id: int, new_person: Person) -> bool:
        node = self.find_node_by_id(id)
        if node:
            node.person = new_person
            return True
        return False

    def delete_person(self, id: int) -> bool:
        for i, root in enumerate(self.roots):
            if root.person.id == id:
                del self.roots[i]
                return True

        for node in self.get_all_nodes():
            for i, child in enumerate(node.children):
                if child.person.id == id:
                    node.remove_child_by_id(id)
                    return True

        return False

    def get_persons_with_adult_daughter(self) -> List[Person]:
        result: List[Person] = []

        for node in self.get_all_nodes():
            for child in node.children:
                if child.person.gender.upper() == "F" and child.person.age >= 18:
                    result.append(node.person)
                    break

        return result

    def filter_by_location_typedoc_gender(self, loc: str, td: str, gr: str) -> List[Person]:
        return [
            p for p in self.get_persons()
            if p.location.code == loc
               and p.typedoc.value.lower() == td.lower()
               and p.gender.lower() == gr.lower()
        ]

    def get_persons_by_location(self, location_code: str) -> List[Person]:
        return [p for p in self.get_persons() if p.location.code == location_code]



