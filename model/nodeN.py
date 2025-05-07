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
        self.roots: List[NodeN] = []  # Ahora puede tener varios nodos raíz

    def find_node_by_id(self, id: int) -> Optional[NodeN]:
        def traverse(node: NodeN) -> Optional[NodeN]:
            if node.person.id == id:
                return node
            for child in node.children:
                found = traverse(child)
                if found:
                    return found
            return None

        for root in self.roots:
            found = traverse(root)
            if found:
                return found
        return None

    def create_person(self, person: Person) -> NodeN:
        # Verificamos si ya existe un nodo con ese ID
        if self.find_node_by_id(person.id):
            raise ValueError(f"Ya existe una persona con id={person.id}")

        new_node = NodeN(person)

        if person.parent_id is None:
            self.roots.append(new_node)
        else:
            parent_node = self.find_node_by_id(person.parent_id)
            if parent_node:
                parent_node.add_child(new_node)
            else:
                raise ValueError(f"Padre con id={person.parent_id} no encontrado.")
        return new_node

    def get_persons(self) -> List[Person]:
        result: List[Person] = []

        def traverse(node: NodeN):
            result.append(node.person)
            for child in node.children:
                traverse(child)

        for root in self.roots:
            traverse(root)

        return result

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

        def traverse(parent: NodeN) -> bool:
            for i, child in enumerate(parent.children):
                if child.person.id == id:
                    parent.remove_child_by_id(id)
                    return True
                if traverse(child):
                    return True
            return False

        for root in self.roots:
            if traverse(root):
                return True
        return False

    def get_persons_with_adult_daughter(self) -> List[Person]:
        result: List[Person] = []

        def has_adult_female_child(node: NodeN) -> bool:
            for child in node.children:
                print(
                    f"Evaluando hija: {child.person.name}, edad: {child.person.age}, tipo doc: {child.person.typedoc}, género: {child.person.gender}")
                if child.person.gender == "F" and (
                        child.person.age >= 18 or child.person.typedoc != "RC"
                ):
                    return True
            return False

        def traverse(node: NodeN):
            if has_adult_female_child(node):
                print(f"Agregando a: {node.person.name}")
                result.append(node.person)
            for child in node.children:
                traverse(child)

        for root in self.roots:
            traverse(root)

        return result

    def filter_by_location_typedoc_gender(self, loc: str, td: str, gr: str) -> List[Person]:
        return [
            person for person in self.get_persons()
            if person.location.code == loc
               and person.typedoc.value == td
               and person.gender.lower() == gr.lower()
        ]

    def get_persons_by_location(self, location_code: str) -> List[Person]:
        return [p for p in self.get_persons() if p.location.code == location_code]


